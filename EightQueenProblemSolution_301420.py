class GeneticAlgorithm:

    def __init__(self,n):
        self.board = self.createPopulation(n)
        self.solutions = []
        self.size = n
        self.env = []
        self.goal = None
        self.goalIndex = -1


    def createPopulation(self,n):
        board = [[0 for i in range(n)] for j in range(n)]
        return board

    def setPopulation(self,board,gen):
        for i in range(self.size):
            board[gen[i]][i] = 1
    def generateSequence(self):
        from random import shuffle
        DNA = list(range(self.size))
        shuffle(DNA)
        while DNA in self.env:
            shuffle(DNA)
        return DNA

    def initFirstSequenceGenereation(self):
        for i in range(500):
            self.env.append(self.generateSequence())

    def buildLogic(self,gen):

        hits = 0
        board = self.createPopulation(self.size)
        self.setPopulation(board,gen)
        col = 0

        for dna in gen:
            try:
                for i in range(col-1,-1,-1):
                    if board[dna][i] == 1:
                        hits+=1
            except IndexError:
                print(gen)
                quit()
            for i,j in zip(range(dna-1,-1,-1),range(col-1,-1,-1)):
                if board[i][j] == 1:
                    hits+=1
            for i,j in zip(range(dna+1,self.size,1),range(col-1,-1,-1)):
                if board[i][j] == 1:
                    hits+=1
            col+=1
        return hits

    def isGoalGen(self,gen):
        if self.buildLogic(gen) == 0:
            return True
        return False

    def crossOverGeneticAlgoFunction(self,firstGen,secondGen):
        for i in range(1,len(firstGen)):
            if abs(firstGen[i-1] - firstGen[i])<2:
                firstGen[i],secondGen[i] = secondGen[i],firstGen[i]
            if abs(secondGen[i-1] - secondGen[i])<2:
                firstGen[i],secondGen[i] = secondGen[i],firstGen[i]
        
    def MutantGeneticAlgoFunction(self,gen):
        bound = self.size//2
        from random import randint as rand
        leftSideIndex = rand(0,bound)
        RightSideIndex = rand(bound+1,self.size-1)
        newGen = []
        for dna in gen:
            if dna not in newGen:
                newGen.append(dna)
        for i in range(self.size):
            if i not in newGen:
                newGen.append(i)

        gen = newGen
        gen[leftSideIndex],gen[RightSideIndex] = gen[RightSideIndex],gen[leftSideIndex]
        return gen


    def crossOverAndMutant(self):
        for i in range(1,len(self.env),2):
            firstGen = self.env[i-1][:]
            secondGen = self.env[i][:]
            self.crossOverGeneticAlgoFunction(firstGen,secondGen)
            firstGen = self.MutantGeneticAlgoFunction(firstGen)
            secondGen = self.MutantGeneticAlgoFunction(secondGen)
            self.env.append(firstGen)
            self.env.append(secondGen)

    def performSelection(self):
        #index problem
        genUtilities = []
        newEnv = []

        for gen in self.env:
            genUtilities.append(self.buildLogic(gen))
        if min(genUtilities) == 0:
            self.goalIndex = genUtilities.index(min(genUtilities))
            self.goal = self.env[self.goalIndex]
            return self.env
        minUtil=None
        while len(newEnv)<self.size:
            minUtil = min(genUtilities)
            minIndex = genUtilities.index(minUtil)
            newEnv.append(self.env[minIndex])
            genUtilities.remove(minUtil)
            self.env.remove(self.env[minIndex])

        return newEnv

    def performGeneticAlgorithmSolution(self):
        self.initFirstSequenceGenereation()
        for gen in self.env:
            if self.isGoalGen(gen):
                return gen
        count = 0
        while True:
            self.crossOverAndMutant()
            self.env = self.performSelection()
            count +=1
            if self.goalIndex >= 0 :
                try:
                    return self.goal
                except IndexError:
                    print(self.goalIndex)
            else:
                continue

if(__name__=='__main__'):
 
    generateSequqnce = GeneticAlgorithm(8)
    solution = generateSequqnce.performGeneticAlgorithmSolution()
    print(solution)