import os
import time
import sys
#pip install pygame

enableDebug = (input("Enable Debug? Y/N:").upper() == "Y")
enableDebugMusic = False

if enableDebug:
    enableDebugMusic = (input("Enable Debug Music? Y/N:").upper() == "Y")





#play music
musicLocation = "REQUIREDmusic.mp3"
fileLocation = os.path.realpath(__file__)





#Get Program


temp = os.listdir(os.path.split(os.path.relpath(fileLocation))[0])
temp.remove(os.path.split(fileLocation)[1])
temp.remove(musicLocation)
temp.remove("README.md")

Program = open(os.path.relpath(os.path.join(os.path.split(fileLocation)[0],temp[0])), "r")


DelayPCycle = 8

SwitchOffset = 0

Input = []

Buffer = None

#global delayLeft 
delayLeft = DelayPCycle

Register = [0,0,0,0]

Stack = []

Syntax = [
    "ADD",
    "SUB",
    "COPY",
    "PUSH",
    "POP",
    "COND",
    "OUT",
    "NOP",
    "",
    "WAIT",
    "SWPOFFSET",
    "WAITSWP",
    "STOP",
    "NP"
]

TokenProgram = []

InpFlag = False

l = 0

PossibleStarts = ["#", "I", "+", "-", "\n"]

lastSign = "-"

skip = False

for line in Program:

    l += 1
    line.strip()
    if line not in ["", "\n"]:
        if line[0].upper() in PossibleStarts:
            if line[0] != "#":
                test = line.split()
                sign = test[0][0]
                test[0] = test[0][1:]
                
                #print(test)
                
                if test[0] == "NP":
                    if InpFlag:
                        raise Exception("You cannot have 2 input statements! Line: " + str(l))
                    InpFlag = True
                    
                    tmp = "".join(test[2:])
                    tmp =  tmp.split(",")
                    
                    for i in tmp:
                        try:
                            Input.append(int(i))
                        except:
                            Input.append(ord(i))
                        
                        
                    
                    
                
                if test[0] not in Syntax:
                    raise Exception("Start of line " + str(l) + " is not correct syntax")
                    
                test.insert(0,sign)
                
                #print(test[1])
                
                if test[1] == "":
                    test[1] = "NOP"
                
                
                if sign == lastSign:
                    raise Exception("2 " + sign + "s in a row! Line: " + str(l))
                lastSign = sign
                if test[1] != "NP":
                    TokenProgram.append(test)
                
                
        else:
            raise Exception("Start of line " + str(l) + " is not formatted correctly")


CustmInp = (input("Custom input? Y/N:").upper() == "Y")
if CustmInp:
    Inputs = input("What should the input be? ex: 10,50,d,t\n")
    Inputs =  Inputs.split(",")
    Input = []
    
    for i in Inputs:
        if i != " ":
            i.strip(" ")
        try:
            Input.append(int(i))
        except:
            Input.append(ord(i))
if enableDebugMusic:
    from pygame import mixer
if enableDebugMusic:
    mixer.init()
    mixer.music.load(os.path.relpath(os.path.join(os.path.split(fileLocation)[0],musicLocation)))
    mixer.music.play()



def printDbg(HlightLine = (len(TokenProgram) + 1), DlyLeft = 8):

    li = 1
    for i in TokenProgram:
        
        if li == HlightLine:
            print(">",end = "")
            print(DlyLeft,end = "")
        else:
            print("  ",end = "")
        
        
                
        
        for j in i:
            
            print(j,end = "")
            print(" ",end = "")
        
        print() 
        li += 1
    print()
    print(printStr)
    print()
    
    



DlyRemove = 0

def valueToNum(Value):
    val = None
    global delayLeft
    match Value[0]:
        case "R":
            val = Register[int(Value[1])]
        case "I":
            val = Input.pop(0)
        case "B":
            val = Buffer
        case "D":
            val = delayLeft
        case _:
            try:
                val = int(Value)
            except:
                raise Exception(str(Value) + " Is not a valid value!")
                
    return int(val)
            
result = False

IsPlus = True

printStr = ""

DlyRemove = 0

def step(LineNum,Dbg = False):
    global skip
    global printStr
    global delayLeft
    global DlyRemove
    global SwitchOffset
    LineNum -= 1
    line = TokenProgram[LineNum]
    if skip:
        line = ["+","NOP"]
        skip = False
    match line[1]:
            case "COPY":
                if line[0] == "-":
                    raise Exception("Only plus can write to Register!! Line: " + str(LineNum + 1))
                Register[int(line[4][1])] = valueToNum(line[2])
                DlyRemove = 2
            case "ADD":
                val = valueToNum(line[2]) + valueToNum(line[3])
                if line[4] == "B":
                    Buffer = val
                else:
                    if line[0] == "-":
                        raise Exception("Only plus can write to Register!! Line: " + str(LineNum + 1))
                    Register[int(line[4][1])] = val
                DlyRemove = 1
            case "SUB":
                val = valueToNum(line[2]) + valueToNum(line[3])
                if line[4] == "B":
                    Buffer = val
                else:
                    if line[0] == "-":
                        raise Exception("Only plus can write to Register!! Line: " + str(LineNum + 1))
                    Register[int(line[4][1])] = val
                DlyRemove = 1
            case "PUSH":
                if line[0] == "+":
                    raise Exception("Only minus can write to Stack!! Line: " + str(LineNum + 1))
                Stack.append(valueToNum(line[2]))
                DlyRemove = 3
            case "POP":
                if line[0] == "+":
                    raise Exception("Only minus can Read Stack!! Line: " + str(LineNum + 1))
                Buffer = Stack.pop()
                DlyRemove = 2
            case "OUT":
                out = valueToNum(line[2])
                if len(line) == 4:
                    out = chr(out)
                
                printStr += str(out)
                if not enableDebug:
                    print(out,end="")
                DlyRemove = 2
            case "NOP":
                DlyRemove = 0
            case "WAIT":
                DlyRemove = valueToNum(line[2])
            case "WAITSWP":
                DlyRemove = delayLeft
            case "SWPOFFSET":
                SwitchOffset = valueToNum(line[2]) * 2
                DlyRemove = 1
            case "STOP":
                if enableDebugMusic: mixer.music.stop()
                printDbg(LineNum + 1, delayLeft)   
                input("\nExecution finished, press enter to quit")
                sys.exit()
            case "COND":
                result = eval(str(valueToNum(line[3])) + line[2] + str(valueToNum(line[4])))
                if line[5][0] != "S":
                    if result:
                        DlyRemove = valueToNum(line[5])
                    else: DlyRemove = 0
                else:
                    if result:
                        skip = True
                    DlyRemove = 0
    
    if DlyRemove < 0:
        raise Exception("Dont put a negative number for a wait value!")
    
    
    if Dbg:
        for i in range(DlyRemove):
            printDbg(LineNum + 1, delayLeft)

            delayLeft -= 1
            if enableDebugMusic:
                time.sleep(0.5)
            else:
                input()
            
            
    else:
        for i in range(DlyRemove):
            delayLeft -= 1

    
    if delayLeft < 0:
        raise Exception("A operation happened during a switch! (try checking the debug mode) Line: " + str(LineNum + 1))
    return
    
        
        
        
def MainInterpLoop():

        returnLine = 0
        
        global IsPlus
        global delayLeft
        global SwitchOffset
        
        lineNum = 1
        
        while True:
            
            step(lineNum, enableDebug)
            

            
            
            if delayLeft == 0:
                
                if IsPlus:
                    returnLine = lineNum
                    lineNum += 3 + SwitchOffset
                    SwitchOffset = 0
                    
                else:
                    lineNum = returnLine + SwitchOffset
                    SwitchOffset = 0
                    
                IsPlus = not IsPlus
                delayLeft = DelayPCycle
            
            if IsPlus:
                lineskip = 2
            else:
                lineskip = -2
                
            
            lineNum += lineskip
            
            try:
                TokenProgram[lineNum - 1]
            except:
                if IsPlus:
                    if enableDebugMusic: mixer.music.stop()
                    printDbg(lineNum, delayLeft)                    
                    input("\nExecution finished, press enter to quit")
                    sys.exit()
                else:
                    lineNum += 2
                    delayLeft = 0 
MainInterpLoop()
