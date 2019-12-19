PHT1 = list() # PHT1 for one level predictor
PHT2 = list() # PHT1 for two level global branch predictor
LHT = list()
for i in range(0,16384):
    PHT1.append(0)
for i in range(0,16384):
    PHT2.append(0)
for i in range(0,16384):
    LHT.append(0)
correctpredicted = 0      # counters for one level predictor
mispredicted = 0
notpredicted = 0
GHR = 0            # Global History Register for two level gShare branch predictor
b = 0              # Number of bits to be discarded from PC before using PC for indexing
TC = list()
for i in range(0,16384):
    TC.append(3)

def twolevelGshareBranchPredictor(PC,p):
    global GHR
    PC = int(PC,16)
    GHR = GHR & ((1<<14)-1)
    PC = (PC>>b) & ((1<<14)-1)
    PC = PC | GHR
    if PHT1[PC] ==0 and p=="N":
        GHR = GHR<<1
        return "N";
    elif PHT1[PC]==0 and p == "T":
        PHT1[PC] = PHT1[PC] + 1
        GHR = (GHR<<1) | 1
        return "N";
    elif PHT1[PC]==3 and p == "T":
        GHR = (GHR<<1) | 1
        return "T";
    elif PHT1[PC]==3 and p == "N":
        PHT1[PC] = PHT1[PC] - 1
        GHR = GHR<<1
        return "T";
    elif PHT1[PC] == 1:
        if p == "T":
            PHT1[PC] = PHT1[PC] + 1
            GHR =(GHR<<1) | 1
        else:
            PHT1[PC] = PHT1[PC] - 1
            GHR = GHR<<1
        return "NP";
    elif PHT1[PC] == 2:
        if p == "T":
            PHT1[PC] = PHT1[PC] + 1
            GHR = (GHR<<1) | 1
        else:
            PHT1[PC] = PHT1[PC] - 1
            GHR = GHR<<1
        return "NP";

def twoLevelLocalHistoryBranchPredictor(PC,p):
    PC = int(PC,16)
    PC = (PC>>b) & ((1<<14)-1)
    LHT[PC] = LHT[PC] & ((1<<14)-1)
    if PHT2[LHT[PC]] ==0 and p=="N":
        LHT[PC] = LHT[PC]<<1
        return "N";
    elif PHT2[LHT[PC]]==0 and p == "T":
        PHT2[LHT[PC]] = PHT2[LHT[PC]] + 1
        LHT[PC] = (LHT[PC]<<1) | 1
        return "N";
    elif PHT2[LHT[PC]]==3 and p == "T":
        LHT[PC] = (LHT[PC]<<1) | 1
        return "T";
    elif PHT2[LHT[PC]]==3 and p == "N":
        PHT2[LHT[PC]] = PHT2[LHT[PC]] - 1
        LHT[PC] = LHT[PC]<<1
        return "T";
    elif PHT2[LHT[PC]] == 1:
        if p == "T":
            PHT2[LHT[PC]] = PHT2[LHT[PC]] + 1
            LHT[PC] =(LHT[PC]<<1) | 1
        else:
            PHT2[LHT[PC]] = PHT2[LHT[PC]] - 1
            LHT[PC] = LHT[PC]<<1
        return "NP";
    elif PHT2[LHT[PC]] == 2:
        if p == "T":
            PHT2[LHT[PC]] = PHT2[LHT[PC]] + 1
            LHT[PC] = (LHT[PC]<<1) | 1
        else:
            PHT2[LHT[PC]] = PHT2[LHT[PC]] - 1
            LHT[PC] = LHT[PC]<<1
        return "NP";

def tournamentPredictor(PC,G,L,A):
    global correctpredicted
    global mispredicted
    global notpredicted
    global b
    PC = int(PC,16)
    PC = (PC>>b)&((1<<14)-1)
    if TC[PC] == 0:
        if L =="NP" and G == "NP":
            notpredicted = notpredicted + 1
        elif (G == "T" and A == "T") or(G == "N" and A == "N"):
            correctpredicted = correctpredicted + 1
        elif (G == "T" and A == "N") or(G == "N" and A == "T") :
            mispredicted = mispredicted + 1
            if L == A:
                TC[PC] = TC[PC] + 1

    elif TC[PC] == 3:
        if L =="NP" and G == "NP":
            notpredicted = notpredicted + 1
        elif (L == "T" and A == "T") or(L == "N" and A == "N"):
            correctpredicted = correctpredicted + 1
        elif (L == "T" and A == "N") or(L == "N" and A == "T") :
            mispredicted = mispredicted + 1
            if G == A:
                TC[PC] = TC[PC] - 1

    elif TC[PC] == 1:
        if L =="NP" and G == "NP":
            notpredicted = notpredicted + 1
        elif (G == "T" and A == "T") or(G == "N" and A == "N"):
            if L !=A:
                TC[PC] = TC[PC] - 1
            correctpredicted = correctpredicted + 1
        elif (G == "T" and A == "N") or(G == "N" and A == "T") :
            if L == A:
                TC[PC] = TC[PC] + 1
            mispredicted = mispredicted + 1


    elif TC[PC] == 2:
        if L =="NP" and G == "NP":
            notpredicted = notpredicted + 1
        elif (L == "T" and A == "T") or(L == "N" and A == "N"):
            if G !=A:
                TC[PC] = TC[PC] + 1
            correctpredicted = correctpredicted + 1
        elif (L == "T" and A == "N") or(L == "N" and A == "T") :
            if G == A:
                TC[PC] = TC[PC] - 1
            mispredicted = mispredicted + 1






    return;

total = 0
b = 3       # Number of bits to be discarded from PC
trace = open("branch-trace-gcc.trace","r")
for line in trace:
    line = line.split()
    G = twolevelGshareBranchPredictor(line[0],line[1])
    L = twoLevelLocalHistoryBranchPredictor(line[0],line[1])
    tournamentPredictor(line[0],G,L,line[1])
    total = total + 1
trace.close()

missrate = (mispredicted/(correctpredicted+mispredicted))*100
print("CorrectPredicted=",correctpredicted)
print("Mispredicted=",mispredicted)
print("Not-Predicted=",notpredicted)
print("Misspredicted rate=",missrate)
