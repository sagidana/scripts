local helper(value) =
  value + 1;

local greet(value) =
  helper(value) * 2;

local runner() =
  greet(3);

{ out: 1 }
