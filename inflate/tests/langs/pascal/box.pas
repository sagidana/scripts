unit Box;

interface

implementation

function helper(value: Integer): Integer;
begin
  Result := value + 1;
end;

function greet(value: Integer): Integer;
begin
  Result := helper(value) * 2;
end;

function runner: Integer;
begin
  Result := greet(3);
end;

end.
