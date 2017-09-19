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

    args = parser.parse_args()
    errors = []
    for test_file in collect_files(args.root):
        try:
            main(test_file, args.in_place)
        except MalformedError as e:
            errors.append(e)

    if len(errors) != 0:
        sys.exit("\n".join("ERROR: " + str(e) for e in errors))

class MalformedError(Exception):
    pass

def main(test_file, update_in_place):
    with open(test_file) as f:
        contents = f.read()
    try:
        start_offset = contents.index("/*---\n") + len("/*---\n")
        end_offset = contents.index("---*/", start_offset)
    except ValueError:
        raise MalformedError("Cannot find frontmatter: " + repr(test_file))

    frontmatter_contents = contents[start_offset:end_offset]
    try:
        frontmatter_node = yaml.compose(frontmatter_contents)
    except yaml.YAMLError as e:
        # these error messages span multiple lines, so add a preface line
        raise MalformedError("yaml error in file: %s\n%s" % (repr(test_file), str(e)))

    new_frontmatter_contents = yaml.serialize(frontmatter_node)
    if new_frontmatter_contents != frontmatter_contents:
        if update_in_place:
            new_contents = contents[:start_offset] + new_frontmatter_contents + contents[end_offset:]
            with open(test_file, "w") as f:
                f.write(new_contents)
        else:
            raise MalformedError("Malformed frontmatter: " + repr(test_file))

def collect_files(path):
    if os.path.isfile(path):
        yield path
        return
    if not os.path.isdir(path): raise IOError("No such file or directory: " + repr(path))
    for root, dirs, file_names in os.walk(path):
        for file_name in file_names:
            if file_name.startswith('.'): continue
            yield os.path.join(root, file_name)

if __name__ == "__main__":
    cli()
