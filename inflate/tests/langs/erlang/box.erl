-module(box).
-compile(export_all).

helper(Value) ->
    Value + 1.

greet(Value) ->
    helper(Value) * 2.

runner() ->
    greet(3).
