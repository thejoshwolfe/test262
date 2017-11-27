// This file was procedurally generated from the following sources:
// - src/type-coercion/String.prototype.indexOf.case
// - src/type-coercion/ToIndex/primitives.template
/*---
description: String.prototype.indexOf offset parameter type coercion (primitives)
flags: [generated]
---*/

assert.sameValue("a".indexOf("a", 0), 0);
assert.sameValue("a".indexOf("a", NaN), 0);
assert.sameValue("aa".indexOf("a", 1), 1);
assert.sameValue("aa".indexOf("a", true), 1);
assert.throws(TypeError, function() { "".indexOf("", Symbol("1")); });
