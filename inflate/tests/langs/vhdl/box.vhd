package body Box is

  function helper(value : integer) return integer is
  begin
    return value + 1;
  end function;

  function greet(value : integer) return integer is
  begin
    return helper(value) * 2;
  end function;

  function runner return integer is
  begin
    return greet(3);
  end function;

end package body;
