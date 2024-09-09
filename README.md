# BBacknForth
My custom esolang
```
Running starts at + command, every action has a delay value, every 8 delay, switch to the - directly after the +.
If you run out of - operations to do, defaults to NOP
After 8 delay on -, switch back to +
The plus to Jump back to is the plus after the last cycle
The exception is if the SWITCHDLY command is run, It offsets the start by the amount of instructions defined by the delay.
For example:
cycle ends here
      |
      V
+-+-+-+-+-+
  | |   | |
 -2 -1  1 2


only - can read/write to array
only + can write to registers
both can read buffer, registers and input
When you POP from array, the value goes into buffer

Input is written at start, seperated by commas. Input is a stack starting with first element of input, whenever input is read, the input is Popped from input.
when you run out of + instructions, stop program


  |Syntax                               | Delay | Usage
   INP = [Inputs]                       : 0     | Set the input stack
+  COPY [Value] to [Adress]             : 2     | Copy a value to a register
+- ADD [Value] [Value] [Adress]         : 1     | Add 2 numbers and save the result in a register
+- SUB [Value] [Value] [Adress]         : 1     | Subtracts 2 numbers value1 - value2 and saves the result in a register
-  PUSH [Value] [Value]                 : 3     | Push a value into the array at specified index
-  POP [Value]                          : 2     | Pop element at specified index off the array and save it in Buffer
+- COND [Cond] [Value] [Value] [Delay]  : Any   | Checks Condition against 2 Values, if false: its delay is 0, otherwize the delay is the delay specified (>0)
+- LBL [Label]                          : 1     | Creates a Label that you can jump back to with the JMP command
+- JMP [Label]                          : 1     | Jumps to Label specified, if the label and the JMP is on the same instruction set (both + or both -)
+- COND [Cond] [Value] [Value] SKIP     : 0     | Checks Condition against 2 Values, if true: skip next command
+- OUT [Value]                          : 2     | Ouput the value as a number
+- OUT [Value] Char                     : 2     | Ouput the value as a ascii character
+- NOP                                  : 0     | No operation 
+- WAIT [Value]                         : Any   | Wait a specified Delay
+- SWPOFFSET [Value]                    : 1     | See above
+- WAITSWP                              : Any   | Waits until switch instruction set
+- STOP                                 : 0     | Exits program

Comments start with # on a newline!!!
Blank = NOP

Adresses: R0-R3 
Value: Adress/Input/Number/Buffer/DlyLeft
Cond : ==, !=, <, >, <=, >=
Delay: COND/WAIT Any positive, SWITCHDLY any number.
```


# USAGE

Put code in example.txt, 
Run interpreter

3 modes: No debug, Debug with music, Debug without music

No debug just runs the code, 
Debug with music advances every tick to the beat, 
Debug without music advances every tick on enter press

# EXAMPLE PROGRAM
```
#Hello World
+OUT 72 Char
-OUT 111 Char
+OUT 101 Char
-OUT 119 Char
+OUT 108 Char
-OUT 32 Char
+OUT 108 Char
-OUT 111 Char
+OUT 114 Char
-
+OUT 108 Char
-
+OUT 100 Char
-
+STOP
```

```
#Truth Machine
INP = 1
+COPY Input to R0 
-
+WAIT 3 
-
+OUT R0 
-
+COND == 1 R0 SKIP
-WAITSWP 
+STOP
-SWPOFFSET -4
+WAITSWP
-
```


