#!/usr/bin/python3


import pandas as pd

__author__ = "Alexis Torrano"
__email__ = "a.torrano.m@gmail.com"
__status__ = "Production"


## **************************************************************
def DFS(currentNode,step,dfsControl):
       
    visitMask = dfsControl['visitMask']
    route = dfsControl['route']
    routeCost = dfsControl['routeCost']
    dist = dfsControl['dist']
    tempWinner = dfsControl['tempWinner']
    tempWinnerCost = dfsControl['tempWinnerCost']
    N = dfsControl['N']
    omega = dfsControl['omega']
    
    visitMask[currentNode] = True
    route[step] = currentNode
    pastNode = route[step-1]
    routeCost[step] = routeCost[step-1] + dist[pastNode][currentNode] 
    
    if routeCost[step] >= tempWinnerCost:
        visitMask[currentNode] = False
        return 1
   
    if currentNode == omega:
        if tempWinnerCost > routeCost[step]:            
            tempWinnerCost = dfsControl['pathCost']
            ##TODO erase int(routeCost[step])
            dfsControl['tempWinnerCost'] = tempWinnerCost
            ##TODO erase int(routeCost[step])
            #tempWinner = route.copy() <-- faulty
            for i in range(len(route)):
                tempWinner[i]=route[i]
            if step < N-1 : # padding of -1 til end of tempWinner
                tempWinner[step+1:] = [-1]*len(tempWinner[step+1:])
        
        visitMask[currentNode] = False
        return 1
    
    # route[step-1] is parent node of current Node
    for neigh in range(N): 
        if neigh!=currentNode and \
        not visitMask[neigh] and \
        dist[currentNode][neigh]!=-1 and \
        step < N-1:
            oldCost = dfsControl['pathCost']
            dfsControl['pathCost'] = dfsControl['pathCost']+dist[currentNode][neigh]
            DFS(neigh,step+1,dfsControl)
            dfsControl['pathCost'] = oldCost
    
    visitMask[currentNode] = False
    return 1    
    
## **************************************************************
def BestRoute(alfa,omega,dist):

    N = len(dist)

    ## dfs CONTROL
    visitMask = [False]*N
    route = [-1]*N
    routeCost = [-1]*N
    tempWinner = [-1]*N
    tempWinnerCost = 1000 # should be sum of all items in dist matrix
    
    dfsControl = {}
    dfsControl['visitMask'] = visitMask
    dfsControl['route'] = route
    dfsControl['routeCost'] = routeCost
    dfsControl['dist'] = dist
    dfsControl['tempWinner'] = tempWinner
    dfsControl['tempWinnerCost'] = tempWinnerCost
    dfsControl['N'] = N


    ## init dfs search
    step=0
    routeCost[step] = 0
    route[step] = alfa
    currentNode = alfa 
    pastNode = alfa
    dfsControl['alfa']=alfa
    dfsControl['omega']=omega
    dfsControl['pathCost']=0.0
    for neigh in range(N): 
        if neigh!=currentNode and \
        not visitMask[neigh] and \
        dist[currentNode][neigh]!=-1 and \
        step < N-1:
            oldCost = dfsControl['pathCost']
            dfsControl['pathCost'] = dfsControl['pathCost']+dist[currentNode][neigh]
            DFS(neigh,step+1,dfsControl)
            dfsControl['pathCost'] = oldCost

    return tempWinner, dfsControl['tempWinnerCost']
    
## **************************************************************
def test1():
    N=5
    ## DATA
    dist=[None]*N
    dist[0] = [ 0, 1, 2, 2,-1]
    dist[1] = [-1, 0, 1, 2, 4]
    dist[2] = [-1, 1, 0, 1,-1]
    dist[3] = [-1, 2, 1, 0, 2]
    dist[4] = [-1,-1,-1,-1, 0]
    #TODO set dist[x,x] = 0
    
    
    winner, winnerCost = BestRoute(0,4,dist)
    
    print(str(winner))
    print(winnerCost)
    






