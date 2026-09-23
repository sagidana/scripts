codeunit 50100 Box
{
    procedure helper(Value: Integer): Integer
    begin
        exit(Value + 1);
    end;

    procedure greet(Value: Integer): Integer
    begin
        exit(helper(Value) * 2);
    end;

    procedure runner(): Integer
    begin
        exit(greet(3));
    end;
}
