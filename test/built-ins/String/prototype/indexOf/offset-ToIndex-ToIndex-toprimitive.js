// This file was procedurally generated from the following sources:
// - src/type-coercion/ToIndex-toprimitive.case
// - src/type-coercion/ToIndex/String.prototype.indexOf-offset.template
/*---
description: ToPrimitive coercion edge cases (String.prototype.indexOf offset)
flags: [generated]
---*/

function err() {
  throw new Test262Error();
}
function MyError() {}


assert.sameValue("a".indexOf("a", ({[Symbol.toPrimitive]: function() { return 0; }, valueOf: err, toString: err})), 0);
assert.sameValue("a".indexOf("a", ({valueOf: function() { return 0; }, toString: err})), 0);
assert.sameValue("aa".indexOf("a", ), 1);
assert.sameValue("aa".indexOf("a", ), 1);
assert.throws(TypeError, function() { "".indexOf("", ({[Symbol.toPrimitive]: function() { return {}; }})); });
assert.throws(MyError, function() { "".indexOf("", ({[Symbol.toPrimitive]: function() { throw new MyError(); }})); });
