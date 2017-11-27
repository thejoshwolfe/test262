// This file was procedurally generated from the following sources:
// - src/type-coercion/ToIndex-primitives.case
// - src/type-coercion/ToIndex/String.prototype.indexOf-offset.template
/*---
description: ToIndex coercion for primitive values (String.prototype.indexOf offset)
flags: [generated]
---*/



assert.sameValue("a".indexOf("a", 0), 0);
assert.sameValue("a".indexOf("a", NaN), 0);
assert.sameValue("aa".indexOf("a", 1), 1);
assert.sameValue("aa".indexOf("a", true), 1);
assert.throws(TypeError, function() { "".indexOf("", Symbol('1')); });
assert.throws(MyError, function() { "".indexOf("", ); });
