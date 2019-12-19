PHT3 = list() # PHT for two level gShare branch predictor
PHT4 = list() # PHT for two level local history Branch predictor
LHT = list() # LHT for two level local history Branch predictor
for i in range(0,1024):
    PHT3.append(0)
for i in range(0,1024):
    PHT4.append(0)
for i in range(0,128):
    LHT.append(0)
correctpredicted3 = 0      # counters for two level gShare branch predictor
mispredicted3 = 0
notpredicted3 = 0
correctpredicted4 = 0
mispredicted4 = 0   # counters for two level local branch predictor
notpredicted4 = 0
GHR2 = 0            # Global History Register for two level gShare branch predictor
b = 0


def twolevelGshareBranchPredictor(PC,path):
    global correctpredicted3
    global mispredicted3
    global notpredicted3
    global GHR2
    global n
    global b
    PC = int(PC,16)
    GHR2 = GHR2 & ((1<<10)-1)
    PC = (PC>>b) & ((1<<10)-1)
    PC = PC | GHR2
    if path == "T":
        if PHT3[PC] > pow(2,n)/2:
            correctpredicted3 = correctpredicted3 + 1
            if PHT3[PC]<(pow(2,n)-1):
                PHT3[PC] = PHT3[PC] + 1
        elif PHT3[PC] < ((pow(2,n)/2) - 1):
            mispredicted3 = mispredicted3 + 1
            PHT3[PC] = PHT3[PC] + 1
        else:
            PHT3[PC] = PHT3[PC] + 1
            notpredicted3 = notpredicted3 + 1
        GHR2 = (GHR2<<1) | 1
    elif path =="N":
        if PHT3[PC] > pow(2,n)/2:
            mispredicted3 = mispredicted3 + 1
            PHT3[PC] = PHT3[PC] - 1
        elif PHT3[PC] < ((pow(2,n)/2) - 1):
            correctpredicted3 = correctpredicted3 + 1
            if PHT3[PC] > 0:
                PHT3[PC] = PHT3[PC] - 1
        else:
            PHT3[PC] = PHT3[PC] - 1
            notpredicted3 = notpredicted3 + 1
        GHR2 = (GHR2<<1) | 0
    return;

def twoLevelLocalHistoryBranchPredictor(PC,path):
    global correctpredicted4
    global mispredicted4
    global notpredicted4
    global n
    global b
    PC = int(PC,16)
    PC = (PC>>b) & ((1<<7)-1)
    LHT[PC] = LHT[PC] & ((1<<10)-1)
    if path == "T":
        if PHT4[LHT[PC]] > pow(2,n)/2:
            correctpredicted4 = correctpredicted4 + 1
            if PHT4[LHT[PC]]<(pow(2,n)-1):
                PHT4[LHT[PC]] = PHT4[LHT[PC]] + 1
        elif PHT4[LHT[PC]] < ((pow(2,n)/2) - 1):
            mispredicted4 = mispredicted4 + 1
            PHT4[LHT[PC]] = PHT4[LHT[PC]] + 1
        else:
            PHT4[LHT[PC]] = PHT4[LHT[PC]] + 1
            notpredicted4 = notpredicted4 + 1
        LHT[PC] = (LHT[PC]<<1) | 1
    elif path =="N":
        if PHT4[LHT[PC]] > pow(2,n)/2:
            mispredicted4 = mispredicted4 + 1
            PHT4[LHT[PC]] = PHT4[LHT[PC]] - 1
        elif PHT4[LHT[PC]] < ((pow(2,n)/2) - 1):
            correctpredicted4 = correctpredicted4 + 1
            if PHT4[LHT[PC]] > 0:
                PHT4[LHT[PC]] = PHT4[LHT[PC]] - 1
        else:
            PHT4[LHT[PC]] = PHT4[LHT[PC]] - 1
            notpredicted4 = notpredicted4 + 1
        LHT[PC] = (LHT[PC]<<1)
    return;




print("Enter the number of bits for counter(Enter numerically eg: 2)")
n = int(input())
b=3
trace = open("branch-trace-gcc.trace","r")
for line in trace:
    line = line.split()
    twolevelGshareBranchPredictor(line[0],line[1])
    twoLevelLocalHistoryBranchPredictor(line[0],line[1])
trace.close()
missrate3 = (mispredicted3/(mispredicted3+correctpredicted3))*100
missrate4 = (mispredicted4/(correctpredicted4+mispredicted4))*100
print()
print("Number of Bits used for counter is: ",n)
print("*********************GShare Predictor*********************")
print("CorrectPredicted=",correctpredicted3)
print("Mispredicted=",mispredicted3)
print("Not-Predicted=",notpredicted3)
print("Misprediction rate",missrate3)
print("***********************************************************")
print()
print("*********************Two Level Local History Predictor*********************")
print("CorrectPredicted=",correctpredicted4)
print("Mispredicted=",mispredicted4)
print("Not-Predicted=",notpredicted4)
print("Misprediction rate",missrate4)
print("***************************************************************************")
