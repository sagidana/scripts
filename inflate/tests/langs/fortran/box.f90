module Box
contains

   function helper(value) result(r)
      integer :: value, r
      r = value + 1
   end function

   function greet(value) result(r)
      integer :: value, r
      r = helper(value) * 2
   end function

   function runner() result(r)
      integer :: r
      r = greet(3)
   end function

end module Box
