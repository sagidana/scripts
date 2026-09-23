package body Box is

   function helper (Value : Integer) return Integer is
   begin
      return Value + 1;
   end;

   function greet (Value : Integer) return Integer is
   begin
      return helper (Value) * 2;
   end;

   function runner return Integer is
   begin
      return greet (3);
   end;

end Box;
