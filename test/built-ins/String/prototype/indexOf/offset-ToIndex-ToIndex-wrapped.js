// This file was procedurally generated from the following sources:
// - src/type-coercion/ToIndex-wrapped.case
// - src/type-coercion/ToIndex/String.prototype.indexOf-offset.template
/*---
description: ToIndex coercion for simple object wrappers (String.prototype.indexOf offset)
flags: [generated]
---*/



assert.sameValue("a".indexOf("a", Object(0)), 0);
assert.sameValue("a".indexOf("a", ({[Symbol.toPrimitive]: function() { return 0; }})), 0);
assert.sameValue("aa".indexOf("a", Object(true)), 1);
assert.sameValue("aa".indexOf("a", ({[Symbol.toPrimitive]: function() { return true; }})), 1);
assert.throws(TypeError, function() { "".indexOf("", Object(Symbol('1'))); });
assert.throws(MyError, function() { "".indexOf("", ); });
