: helper ( n -- n )
  1 + ;

: greet ( n -- n )
  helper 2 * ;

: runner ( -- n )
  3 greet ;
