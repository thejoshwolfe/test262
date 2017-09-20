import yaml
import os
import sys

def cli():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("-c", "--check", action="store_true",
        help="print errors when changes would be made")
    action_group.add_argument("-i", "--in-place", action="store_true",
        help="make changes to files in-place")
    parser.add_argument("--harness-features", help="harness/features.yml")

    args = parser.parse_args()

    if args.harness_features:
        harness_to_features = load_harness_to_features(args.harness_features)
    else:
        harness_to_features = None

    errors = []
    for test_file in collect_files(args.root):
        try:
            main(test_file, args.in_place, harness_to_features)
        except MalformedError as e:
            errors.append(e)

    if len(errors) != 0:
        sys.exit("\n".join("ERROR: " + str(e) for e in errors))

def main(test_file, update_in_place, harness_to_features):
    def err(msg):
        return MalformedError(msg + ": " + repr(test_file))
    def type_check(node, expected_type, object_name):
        if type(node) != expected_type:
            raise err("%s expected to be %s" % (object_name, expected_type.__name__))

    with open(test_file) as f:
        contents = f.read()
    try:
        start_offset = contents.index("/*---\n") + len("/*---\n")
        end_offset = contents.index("---*/", start_offset)
    except ValueError:
        raise err("cannot find frontmatter")

    frontmatter_contents = contents[start_offset:end_offset]
    try:
        frontmatter_node = yaml.compose(frontmatter_contents)
    except yaml.YAMLError as e:
        # These error messages span multiple lines, so add a preface line.
        raise MalformedError("yaml error in file: %s\n%s" % (repr(test_file), str(e)))
    type_check(frontmatter_node, yaml.MappingNode, "frontmatter")
    if frontmatter_node.flow_style != False:
        raise err("frontmatter expected to be in multiline style")

    # Record how sections partition the contents so we can make slices later.
    section_partitions = {
        # "features": (0, 13), # contents[0:13] == "features: []\n"
    }
    cursor = 0
    for i in range(len(frontmatter_node.value)):
        section_name = frontmatter_node.value[i][0].value
        if i + 1 < len(frontmatter_node.value):
            next_cursor = frontmatter_node.value[i + 1][0].start_mark.index
        else:
            next_cursor = len(frontmatter_contents)
        section_partitions[section_name] = (cursor, next_cursor)
        cursor = next_cursor

    # These are the changes we want to make.
    updated_section_names = set([
        # "features", # means we've added or edited the list of features
    ])
    removed_section_names = set([
        # "features", # means completely remove the list of features
    ])

    ############################################

    def check_includes_features():
        includes = set([
            # "testAtomics.js",
        ])

        try:
            includes_node = get_mapped_node(frontmatter_node, "includes")
        except KeyError:
            # No includes.
            pass
        else:
            type_check(includes_node, yaml.SequenceNode, "includes")

            if len(includes_node.value) == 0:
                # Defined but empty; remove it.
                removed_section_names.add("includes")
            else:
                i = 0
                while i < len(includes_node.value):
                    include_node = includes_node.value[i]
                    type_check(include_node, yaml.ScalarNode, "include")
                    include = include_node.value
                    if include in includes:
                        # Remove duplicate include.
                        del includes_node.value[i]
                        updated_section_names.add("includes")
                        continue
                    includes.add(include)
                    i += 1

        required_features = set([
            # "Symbol",
        ])
        for include in includes:
            try:
                harness_features = harness_to_features[include]
            except KeyError:
                # Harness dependency requires no features.
                continue
            required_features.update(harness_features)

        try:
            features_node = get_mapped_node(frontmatter_node, "features")
        except KeyError:
            # No features declared.
            if len(required_features) > 0:
                # Create features entry; we will add elements to it.
                features_node = yaml.SequenceNode(DEFAULT_SEQUENCE_TAG, [], flow_style=True)
                frontmatter_node.value.append((yaml.ScalarNode(DEFAULT_SCALAR_TAG, "features"), features_node))
                updated_section_names.add("features")
            else:
                features_node = None
        else:
            type_check(features_node, yaml.SequenceNode, "features")

        features = set([
            # "Symbol",
        ])
        if features_node != None:
            i = 0
            while i < len(features_node.value):
                feature_node = features_node.value[i]
                type_check(feature_node, yaml.ScalarNode, "feature")
                feature = feature_node.value
                if feature in features:
                    # Remove duplicate feature.
                    del features_node.value[i]
                    updated_section_names.add("features")
                    continue
                features.add(feature)
                i += 1

        missing_features = list(required_features - features)
        if len(missing_features) > 0:
            missing_features.sort()
            for missing_feature in missing_features:
                features_node.value.append(yaml.ScalarNode(DEFAULT_SCALAR_TAG, missing_feature))
            updated_section_names.add("features")

        if features_node != None and len(features_node.value) == 0:
            # Delete empty features list.
            removed_section_names.add("features")

    ############################################

    if harness_to_features != None:
        check_includes_features()

    if len(updated_section_names) + len(removed_section_names) > 0:
        if not update_in_place:
            raise err("frontmatter needs updates")
        else:
            # Canonicalize the entire frontmatter, and then grab excerpts from it.
            # Don't use the complete canonical formatting, because it's much worse for
            # paragraph-style text like "description". Additionally, we don't want to
            # make changes except where it actually matters.
            canonical_frontmatter_contents = yaml.serialize(frontmatter_node)
            canonical_frontmatter_node = yaml.compose(canonical_frontmatter_contents)
            new_frontmatter_contents_parts = []
            for section_name_node, section_node in frontmatter_node.value:
                section_name = section_name_node.value
                if section_name in removed_section_names:
                    # Skip this section.
                    continue
                elif section_name in updated_section_names:
                    # Use new formatting.
                    canonical_section_index = mapping_index(canonical_frontmatter_node, section_name)
                    slice_start = canonical_frontmatter_node.value[canonical_section_index][0].start_mark.index
                    if canonical_section_index + 1 < len(canonical_frontmatter_node.value):
                        slice_end = canonical_frontmatter_node.value[canonical_section_index + 1][0].start_mark.index
                    else:
                        slice_end = len(canonical_frontmatter_contents)
                    new_frontmatter_contents_parts.append(canonical_frontmatter_contents[slice_start:slice_end])
                else:
                    # Use old formatting.
                    (slice_start, slice_end) = section_partitions[section_name]
                    new_frontmatter_contents_parts.append(frontmatter_contents[slice_start:slice_end])

            with open(test_file, "w") as f:
                f.write(contents[:start_offset])
                for part in new_frontmatter_contents_parts:
                    f.write(part)
                f.write(contents[end_offset:])

class MalformedError(Exception):
    pass

def collect_files(path):
    if os.path.isfile(path):
        yield path
        return
    if not os.path.isdir(path): raise IOError("No such file or directory: " + repr(path))
    for root, dirs, file_names in os.walk(path):
        for file_name in file_names:
            if file_name.startswith('.'): continue
            yield os.path.join(root, file_name)

def load_harness_to_features(path):
    with open(path) as f:
        return yaml.safe_load(f)

def get_mapped_node(mapping_node, name):
  return mapping_node.value[mapping_index(mapping_node, name)][1]
def mapping_index(mapping_node, name):
  for i, (name_node, value_node) in enumerate(mapping_node.value):
    if name_node.value == name:
      return i
  raise KeyError

DEFAULT_SCALAR_TAG = u'tag:yaml.org,2002:str'
DEFAULT_SEQUENCE_TAG = u'tag:yaml.org,2002:seq'
DEFAULT_MAPPING_TAG = u'tag:yaml.org,2002:map'

if __name__ == "__main__":
    cli()
