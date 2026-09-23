helper(Value, Out) :-
    Out is Value + 1.

greet(Value, Out) :-
    helper(Value, Mid),
    Out is Mid * 2.

runner(Out) :-
    greet(3, Out).
