       IDENTIFICATION DIVISION.
       PROGRAM-ID. BOX.
       PROCEDURE DIVISION.

       helper SECTION.
           ADD 1 TO WS-VALUE.

       greet SECTION.
           PERFORM helper.

       runner SECTION.
           PERFORM greet.
