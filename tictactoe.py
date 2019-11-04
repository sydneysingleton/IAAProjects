# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 16:43:06 2019

@author: sydne
"""
import numpy as np

def checkWin(x):
    if all(i == x[0][0] for i in x[0]):
        return(False)
    elif all(i == x[1][0] for i in x[1]):
         return(False)
    elif all(i == x[2][0] for i in x[2]):
         return(False)
    elif all(i == x[0][0] for i in x[:,0]):
         return(False)
    elif all(i == x[0][1] for i in x[:,1]):
         return(False)
    elif all(i == x[0][2] for i in x[:,2]):
         return(False)
    elif all(i == x[0][0] for i in np.array([x[0][0], x[1][1], x[2][2]])):
         return(False)
    elif all(i == x[0][2]  for i in np.array([x[0][2],x[1][1],x[2][0]])):
         return(False)
    else :
        return(True)
    
def checkValid(x,y): #x=gameboard matrix, y=userinput
    if y in x :
        return(True)

    else: 
        return(False)

def tictactoe(p1,p2):
    print("Lets play tic tac toe! Here is the gameboard:")
    gameboard=np.array([["A1","A2","A3"],["B1","B2","B3"],["C1","C2","C3"]])
    print(gameboard[0])
    print(gameboard[1])
    print(gameboard[2])
    loop = 0
    while checkWin(gameboard):
        print(p1+", its your turn!")
        x=input("please input the space you would like to place your X:")
        while checkValid(gameboard,x):
            gameboard[np.where(gameboard==x)]="X"
            print(gameboard)
            break
        else:
            while not checkValid(gameboard,x):
                print("Space not valid.")
                x= input("Enter valid space:")
            gameboard[np.where(gameboard==x)]="X"
            print(gameboard)
        if not checkWin(gameboard):
            print("winner!")
            break
        loop=loop+1
        print(loop)
        if loop == 9:
            print("its a tie!")
            break
        print(p2+", its your turn!")
        y=input("please input the space you would like to place your O:")
        while checkValid(gameboard,y):
            gameboard[np.where(gameboard==y)]="O"
            print(gameboard)
            break
        else:
            while not checkValid(gameboard,y):
                print("Space not valid.")
                y= input("Enter valid space:")
            gameboard[np.where(gameboard==y)]="O"
            print(gameboard)
        loop=loop+1
        if not checkWin(gameboard):
            print("winner!")
tictactoe("Player 1","Player 2")