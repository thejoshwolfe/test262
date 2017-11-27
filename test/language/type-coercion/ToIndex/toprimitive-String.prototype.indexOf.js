// This file was procedurally generated from the following sources:
// - src/type-coercion/String.prototype.indexOf.case
// - src/type-coercion/ToIndex/toprimitive.template
/*---
description: String.prototype.indexOf offset parameter type coercion (toprimitive)
flags: [generated]
---*/

function err() {
  throw new Test262Error();
}
function MyError() {}

assert.sameValue("a".indexOf("a", ({[Symbol.toPrimitive]: function() { return 0; }, valueOf: err, toString: err})), 0);
assert.sameValue("a".indexOf("a", ({valueOf: function() { return 0; }, toString: err})), 0);
assert.sameValue("a".indexOf("a", ({toString: function() { return 0; }})), 0);
assert.throws(TypeError, function() { "".indexOf("", ({[Symbol.toPrimitive]: function() { return {}; }})); });
assert.throws(TypeError, function() { "".indexOf("", ({[Symbol.toPrimitive]: {}})); });
assert.sameValue("a".indexOf("a", ({[Symbol.toPrimitive]: null, toString: function() { return 0; }})), 0);
assert.throws(MyError, function() { "".indexOf("", ({[Symbol.toPrimitive]: function() { throw new MyError(); }})); });
