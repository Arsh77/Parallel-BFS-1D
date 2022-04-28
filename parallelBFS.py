from mpi4py import MPI
import time
import csv
import sys

def graphCSVCreation(A):
    with open("result1.txt", "w") as file:
        arr = " ".join(map(str, A))
        file.write(arr)

def splitGraph(array, n):
    length = len(array)
    each = length//n
    m = length % n
    final = []
    begin, end = 0,0
    for i in range(n):
        end +=each
        if i<m: 
            end+=1
        final.append(array[begin:end])
        begin = end
    return final

def readCSV(fileName):
    arr = []
    c = 0
    with open('{}.csv'.format(fileName), mode ='r')as file:    
        csvFile = csv.reader(file, delimiter=',')        
        for lines in csvFile:
            if c%2==0:
                temp = [int(i) for i in lines]
                arr.append(temp)
            c+=1
    return arr

def graphPadding(A, p):
    if len(A)%p==0:
        return A
    n = len(A)//p
    r = p*(n+1) - len(A)
    for i in range(r):
        arr = [0]
        A.append(arr)
    return A

def parallelBFS(comm, rank, nProcs, A, vertexOffset, source):

    vertexLevelSet = [float("inf") if vertexOffset*rank + i != 0 else 0 for i in range(len(A))]
    level=0
    frontier = set([i for i in range(len(A)) if vertexLevelSet[i]==level])
    visited = set()

    while True:
        neighbors = set()

        for i in frontier:
            i=i%vertexOffset
            for j in A[i]:
                if j not in visited:
                    neighbors.add(j)
        
        sendBuffer = [[] for i in range(nProcs)]
        for i in neighbors:
            sendBuffer[i//vertexOffset].append(i)
        recvBuf = comm.alltoall(sendBuffer)

        recvNeighbors = set()

        for i in recvBuf:
            for j in i:
                if j is not visited:
                    recvNeighbors.add(j)
        for i in recvNeighbors:
            idx = i%vertexOffset
            if i not in visited and vertexLevelSet[idx]==float("inf"):
                vertexLevelSet[idx]=level+1
        level+=1
        frontier = recvNeighbors
        visited.update(recvNeighbors)
        visited.update(neighbors)
    
        size = len(frontier)
        size = comm.allreduce(size,op=MPI.SUM)

        if size==0:
            break

    levelSetConsolidated = comm.gather(vertexLevelSet, root = 0)
    ans = []

    if levelSetConsolidated:
        for i in levelSetConsolidated:
            if len(i)>0:
                ans+=i    
    #if rank==0:
        #graphCSVCreation(ans)
        #print("level approached: ", ans)
    return ans

def mainfn(num):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nProcs = comm.Get_size()

    vertexOffset = 0
    #for i in range(nProcs):
    graphA = readCSV("splitG{}/nGraph{}".format(num,rank))
    #print("rank: ", rank, " Length graphA: ", len(graphA))
        #graphA = graphPadding(graphA, nProcs)
    vertexOffset = len(graphA)
        #data = splitGraph(graphA, nProcs)
    #else:
        #data = None
    
    #data = comm.scatter(data, root=0)
    data = graphA
    vertexOffset = comm.allreduce(vertexOffset, MPI.MAX)
    st = time.time()
    levelSet = parallelBFS(comm, rank, nProcs, data, vertexOffset, 0)
    if rank==0:
        print("length: ", len(graphA)*nProcs)
        print("time: ", time.time()-st)

if __name__=="__main__":
    mainfn(sys.argv[1])
