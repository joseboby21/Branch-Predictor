PHT1 = list() # PHT for one level predictor
PHT2 = list() # PHT for two level global branch predictor
PHT3 = list() # PHT for two level gShare branch predictor
PHT4 = list() # PHT for two level local history Branch predictor
LHT = list() # LHT for two level local history Branch predictor
for i in range(0,1024): #Initializing PHT for One level
    PHT1.append(0)
for i in range(0,1024): #INitializing PHT for Two Level Global
    PHT2.append(0)
for i in range(0,1024): # Initializing PHT for Two Level Gshare
    PHT3.append(0)
for i in range(0,1024): # Initializing PHT for Two Level Local
    PHT4.append(0)
for i in range(0,128):  # Initializing  LHT for Two Level Local
    LHT.append(0)
correctpredicted1 = 0      # counters for one level predictor
mispredicted1 = 0
notpredicted1 = 0
correctpredicted2 = 0      # counters for two level global branch predictor
mispredicted2 = 0
notpredicted2 = 0
correctpredicted3 = 0      # counters for two level gShare branch predictor
mispredicted3 = 0
notpredicted3 = 0
correctpredicted4 = 0      # counters for two level local branch predictor
mispredicted4 = 0
notpredicted4 = 0

GHR1 = 0            # Global History Register for two level global branch predictor
GHR2 = 0            # Global History Register for two level gShare branch predictor
b = 0

def oneLevelBranchPredictor(PC,p):
    global correctpredicted1
    global mispredicted1
    global notpredicted1
    PC = int(PC,16)
    PC = ((PC>>b) & ((1<<10)-1))
    if PHT1[PC] ==0 and p=="N":
        correctpredicted1 = correctpredicted1 + 1
    elif PHT1[PC]==0 and p == "T":
        mispredicted1 = mispredicted1 + 1
        PHT1[PC] = PHT1[PC] + 1
    elif PHT1[PC]==3 and p == "T":
        correctpredicted1 = correctpredicted1 + 1
    elif PHT1[PC]==3 and p == "N":
        mispredicted1 = mispredicted1 + 1
        PHT1[PC] = PHT1[PC] - 1
    elif PHT1[PC] == 1:
        if p == "T":
            PHT1[PC] = PHT1[PC] + 1

        else:
            PHT1[PC] = PHT1[PC] - 1
        notpredicted1 = notpredicted1 + 1
    elif PHT1[PC] == 2:
        if p == "T":
            PHT1[PC] = PHT1[PC] + 1
        else:
            PHT1[PC] = PHT1[PC] - 1
        notpredicted1 = notpredicted1 + 1
    return;

def twolevelGlobalBranchPredictor(p):
    global correctpredicted2
    global mispredicted2
    global notpredicted2
    global GHR1
    global b
    GHR1 = GHR1 & ((1<<10)-1)
    if PHT2[GHR1] ==0 and p=="N":
        correctpredicted2 = correctpredicted2 + 1
        GHR1 = GHR1<<1
    elif PHT2[GHR1]==0 and p == "T":
        mispredicted2 = mispredicted2 + 1
        PHT2[GHR1] = PHT2[GHR1] + 1
        GHR1 = (GHR1<<1) | 1
    elif PHT2[GHR1]==3 and p == "T":
        correctpredicted2 = correctpredicted2 + 1
        GHR1 = (GHR1<<1) | 1
    elif PHT2[GHR1]==3 and p == "N":
        mispredicted2 = mispredicted2 + 1
        PHT2[GHR1] = PHT2[GHR1] - 1
        GHR1 = GHR1<<1
    elif PHT2[GHR1] == 1:
        if p == "T":
            PHT2[GHR1] = PHT2[GHR1] + 1
            GHR1 =(GHR1<<1) | 1
        else:
            PHT2[GHR1] = PHT2[GHR1] - 1
            GHR1 = GHR1<<1
        notpredicted2 = notpredicted2 + 1
    elif PHT2[GHR1] == 2:
        if p == "T":
            PHT2[GHR1] = PHT2[GHR1] + 1
            GHR1 = (GHR1<<1) | 1
        else:
            PHT2[GHR1] = PHT2[GHR1] - 1
            GHR1 = GHR1<<1
        notpredicted2 = notpredicted2 + 1

    return;

def twolevelGshareBranchPredictor(PC,p):
    global correctpredicted3
    global mispredicted3
    global notpredicted3
    global GHR2
    global b
    PC = int(PC,16)
    GHR2 = GHR2 & ((1<<10)-1)
    PC = (PC>>b) & ((1<<10)-1)
    PC = PC | GHR2
    if PHT3[PC] ==0 and p=="N":
        correctpredicted3 = correctpredicted3 + 1
        GHR2 = GHR2<<1
    elif PHT3[PC]==0 and p == "T":
        mispredicted3 = mispredicted3 + 1
        PHT3[PC] = PHT3[PC] + 1
        GHR2 = (GHR2<<1) | 1
    elif PHT3[PC]==3 and p == "T":
        correctpredicted3 = correctpredicted3 + 1
        GHR2 = (GHR2<<1) | 1
    elif PHT3[PC]==3 and p == "N":
        mispredicted3 = mispredicted3 + 1
        PHT3[PC] = PHT3[PC] - 1
        GHR2 = GHR2<<1
    elif PHT3[PC] == 1:
        if p == "T":
            PHT3[PC] = PHT3[PC] + 1
            GHR2 =(GHR2<<1) | 1
        else:
            PHT3[PC] = PHT3[PC] - 1
            GHR2 = GHR2<<1
        notpredicted3 = notpredicted3 + 1
    elif PHT3[PC] == 2:
        if p == "T":
            PHT3[PC] = PHT3[PC] + 1
            GHR2 = (GHR2<<1) | 1
        else:
            PHT3[PC] = PHT3[PC] - 1
            GHR2 = GHR2<<1
        notpredicted3 = notpredicted3 + 1
    return;

def twoLevelLocalHistoryBranchPredictor(PC,p):
    global correctpredicted4
    global mispredicted4
    global notpredicted4
    global b
    PC = int(PC,16)
    PC = (PC>>b) & ((1<<7)-1)
    LHT[PC] = LHT[PC] & ((1<<10)-1)
    if PHT4[LHT[PC]] ==0 and p=="N":
        correctpredicted4 = correctpredicted4 + 1
        LHT[PC] = LHT[PC]<<1
    elif PHT4[LHT[PC]]==0 and p == "T":
        mispredicted4 = mispredicted4 + 1
        PHT4[LHT[PC]] = PHT4[LHT[PC]] + 1
        LHT[PC] = (LHT[PC]<<1) | 1
    elif PHT4[LHT[PC]]==3 and p == "T":
        correctpredicted4 = correctpredicted4 + 1
        LHT[PC] = (LHT[PC]<<1) | 1
    elif PHT4[LHT[PC]]==3 and p == "N":
        mispredicted4 = mispredicted4 + 1
        PHT4[LHT[PC]] = PHT4[LHT[PC]] - 1
        LHT[PC] = LHT[PC]<<1
    elif PHT4[LHT[PC]] == 1:
        if p == "T":
            PHT4[LHT[PC]] = PHT4[LHT[PC]] + 1
            LHT[PC] =(LHT[PC]<<1) | 1
        else:
            PHT4[LHT[PC]] = PHT4[LHT[PC]] - 1
            LHT[PC] = LHT[PC]<<1
        notpredicted4 = notpredicted4 + 1
    elif PHT4[LHT[PC]] == 2:
        if p == "T":
            PHT4[LHT[PC]] = PHT4[LHT[PC]] + 1
            LHT[PC] = (LHT[PC]<<1) | 1
        else:
            PHT4[LHT[PC]] = PHT4[LHT[PC]] - 1
            LHT[PC] = LHT[PC]<<1
        notpredicted4 = notpredicted4 + 1
    return;





b=3
trace = open("branch-trace-gcc.trace","r")
for line in trace:
    line = line.split()
    oneLevelBranchPredictor(line[0],line[1])
    twolevelGlobalBranchPredictor(line[1])
    twolevelGshareBranchPredictor(line[0],line[1])
    twoLevelLocalHistoryBranchPredictor(line[0],line[1])
trace.close()
missrate1 = (mispredicted1/(correctpredicted1+mispredicted1))*100
missrate2 = (mispredicted2/(correctpredicted2+mispredicted2))*100
missrate3 = (mispredicted3/(correctpredicted3+mispredicted3))*100
missrate4 = (mispredicted4/(correctpredicted4+mispredicted4))*100
print("*********************One Level Predictor********************")
print("CorrectPredicted=",correctpredicted1)
print("Mispredicted=",mispredicted1)
print("Not-Predicted=",notpredicted1)
print("Misprediction rate",missrate1)
print("************************************************************")
print()
print("*********************Two level GLobal Predictor*********************")
print("CorrectPredicted=",correctpredicted2)
print("Mispredicted=",mispredicted2)
print("Not-Predicted=",notpredicted2)
print("Misprediction rate",missrate2)
print("********************************************************************")
print()
print("*********************GShare Predictor*********************")
print("CorrectPredicted=",correctpredicted3)
print("Mispredicted=",mispredicted3)
print("Not-Predicted=",notpredicted3)
print("Misprediction rate",missrate3)
print("***********************************************************")
print()
print("*********************Two Level Local Predictor*********************")
print("CorrectPredicted=",correctpredicted4)
print("Mispredicted=",mispredicted4)
print("Not-Predicted=",notpredicted4)
print("Misprediction rate",missrate4)
print("*******************************************************************")
print()
