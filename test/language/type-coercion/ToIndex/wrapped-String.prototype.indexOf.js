// This file was procedurally generated from the following sources:
// - src/type-coercion/String.prototype.indexOf.case
// - src/type-coercion/ToIndex/wrapped.template
/*---
description: String.prototype.indexOf offset parameter type coercion (wrapped)
flags: [generated]
---*/

assert.sameValue("a".indexOf("a", Object(0)), 0);
assert.sameValue("a".indexOf("a", ({[Symbol.toPrimitive]: function() { return 0; }})), 0);
assert.sameValue("a".indexOf("a", ({valueOf: function() { return 0; }})), 0);
assert.sameValue("a".indexOf("a", ({toString: function() { return 0; }})), 0);
assert.sameValue("a".indexOf("a", Object(NaN)), 0);
assert.sameValue("a".indexOf("a", ({[Symbol.toPrimitive]: function() { return NaN; }})), 0);
assert.sameValue("a".indexOf("a", ({valueOf: function() { return NaN; }})), 0);
assert.sameValue("a".indexOf("a", ({toString: function() { return NaN; }})), 0);
assert.sameValue("aa".indexOf("a", Object(true)), 1);
assert.sameValue("aa".indexOf("a", ({[Symbol.toPrimitive]: function() { return true; }})), 1);
assert.sameValue("aa".indexOf("a", ({valueOf: function() { return true; }})), 1);
assert.sameValue("aa".indexOf("a", ({toString: function() { return true; }})), 1);
assert.throws(TypeError, function() { "".indexOf("", Object(Symbol("1"))); });
assert.throws(TypeError, function() { "".indexOf("", ({[Symbol.toPrimitive]: function() { return Symbol("1"); }})); });
assert.throws(TypeError, function() { "".indexOf("", ({valueOf: function() { return Symbol("1"); }})); });
assert.throws(TypeError, function() { "".indexOf("", ({toString: function() { return Symbol("1"); }})); });
