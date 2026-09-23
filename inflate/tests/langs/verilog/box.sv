module Box;

  function int helper(int value);
    return value + 1;
  endfunction

  function int greet(int value);
    return helper(value) * 2;
  endfunction

  function int runner();
    return greet(3);
  endfunction

endmodule
