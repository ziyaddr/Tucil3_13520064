import os
import time
from tkinter import messagebox
from tkinter import filedialog
import tkinter
from turtle import width
from pyparsing import col

from sympy import false, true
import puzzle
from tkinter import *
import timeit
import threading
import copy
import numpy as np



def generateBoard():
    global tileBuffer
    global boardFrame
    tileBuffer = []
    for i in range(4):
        tempList = []
        for j in range(4):
            tempLabel = Label(boardFrame, text='', borderwidth=1, relief="solid", width=12, height=6, bg="white")
            tempLabel.grid(column=j, row=i)
            tempList.append(tempLabel)
        tileBuffer.append(tempList)
def refreshBoard():
    global Mat_Puzzle
    global tileBuffer
    for i in range(4):
        for j in range(4):
            if (Mat_Puzzle.buffer[i,j] == 16):
                tileBuffer[i][j].config(text = '', bg="white")
            else:
                tileBuffer[i][j].config(text = Mat_Puzzle.buffer[i,j], bg="grey")

def generateInfo():
    global infoFrame
    global infoBuffer
    infoBuffer = []
    for i in range(16):
        num = i+1
        tempLabel = Label(infoFrame, text = "Kurang(" + str(num) + ") = " + str(Mat_Puzzle.Kurang(num)), anchor="w", justify="left")
        infoBuffer.append(tempLabel)
        tempLabel.grid(row=i, column=1, sticky=W)
    tempLabel = Label(infoFrame, text = "Total Kurang = " + str(Mat_Puzzle.Kurang(num)), anchor="w", justify="left")
    infoBuffer.append(tempLabel)
    tempLabel.grid(row=16, column=1, sticky=W)
    tempLabel = Label(infoFrame, text = " ", anchor="w", justify="left")
    tempLabel.grid(row=17, column=1, sticky=W)
    infoBuffer.append(tempLabel)
    tempLabel = Label(infoFrame, text="Waktu: ", anchor=W, justify="left")
    tempLabel.grid(row=18, column=1, sticky=W)
    infoBuffer.append(tempLabel)
    tempLabel = Label(infoFrame, text="Total simpul dibangkitkan: ", anchor=W, justify="left")
    tempLabel.grid(row=19, column=1, sticky=W)
    infoBuffer.append(tempLabel)

def refreshInfo():
    global infoBuffer
    global Mat_Puzzle
    global globalTime
    global solved
    for i in range(16):
        num = i+1
        infoBuffer[i].config(text = "Kurang(" + str(num) + ") = " + str(Mat_Puzzle.Kurang(num)))
    infoBuffer[16].config(text = "Total Kurang = " + str(Mat_Puzzle.TotalKurang()))
    if Mat_Puzzle.isSolveable():
        infoBuffer[17].config(text = "DAPAT DISELESAIKAN")
    else:
        infoBuffer[17].config(text = "TIDAK DAPAT DISELESAIKAN")
    infoBuffer[18].config(text = ("Waktu = " + str(globalTime) + " s") )
    infoBuffer[19].config(text = ("Simpul dibangkitkan = ") + str(globalNodeCount))
    if Mat_Puzzle.TotalKurang() == 0:
        solved = True
    else:
        solved = False


def refresh():
    global Mat_Puzzle
    global solveable
    refreshBoard()
    refreshInfo()
    if Mat_Puzzle.isSolveable():
        solveable = True
    else:
        solveable = False

def on_press(key):
    global Mat_Puzzle
    if key.keysym == "Up":
        Mat_Puzzle = Mat_Puzzle.move('u')
    elif key.keysym == "Down":
        Mat_Puzzle = Mat_Puzzle.move('d')
    elif key.keysym == "Right":
        Mat_Puzzle = Mat_Puzzle.move('r')
    elif key.keysym == "Left":
        Mat_Puzzle = Mat_Puzzle.move('l')
    refresh()

def generateButton():
    global buttonFrame
    tempButton = Button(buttonFrame, text="Solve", command=thd_solve)
    tempButton.grid(column=0, row=2)
    tempButton = Button(buttonFrame, text="Generate Random Puzzle", command=generateRandom)
    tempButton.grid(column=0, row=0)
    tempButton = Button(buttonFrame, text="Read From File", command=browse)
    tempButton.grid(column=0, row=1)

    refresh()
def browse():
    global Mat_Puzzle
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a matrix file(.txt)")
    if (solving):
        messagebox.showinfo("Alert", "Puzzle is being solved")
    else:
        try:
            Mat_Puzzle.readFile(filename)          
            refresh()
        except:
            messagebox.showinfo("Alert", "Invalid file input")
        

def generateRandom():
    global solving
    global Mat_Puzzle
    if (solving):
        messagebox.showinfo("Alert", "Puzzle is being solved")
    else:
        Mat_Puzzle.randomize()
        refresh()

def thd_solve():
    global solving
    global solved
    if solved:
       messagebox.showinfo("Alert", "Puzzle is already solved") 
    else:
        if solveable:
            if not solving:
                t = threading.Thread(target=solve)
                t.start()
            else:
                messagebox.showinfo("Alert", "Puzzle is being solved")
        else:
            messagebox.showinfo("Alert", "Puzzle can't be solved")

def solve():
    
    global solving
    global globalTime
    global globalSteps
    global globalNodeCount
    global Mat_Puzzle
    solving = True

    
    Mat_Puzzle_Cpy = copy.deepcopy(Mat_Puzzle)
    puzzle.Tree.reset()
    Tree_Puzzle = puzzle.Tree(None, Mat_Puzzle_Cpy, 0, 0, '-')
    Tree_Puzzle.solve()
    globalTime = Tree_Puzzle.timeElapsed[0]
    globalSteps = Tree_Puzzle.livingNode[0].steps
    globalNodeCount = Tree_Puzzle.nodeCount[0]
    for i in globalSteps:
        Mat_Puzzle = Mat_Puzzle.move(i)
        time.sleep(0.1)
        refresh()


    solving = False



# global variable
solving = False
solveable = True
solved = False
Mat_Puzzle = puzzle.Matrix()
tileBuffer = []
infoBuffer = []
globalTime = 0
globalSteps = 0
globalNodeCount = 0


root = Tk()
root.geometry("600x600")
boardFrame = Frame(root)
infoFrame = Frame(root)
buttonFrame = Frame(root)

Mat_Puzzle.randomize()
generateBoard()
generateInfo()
generateButton()
refresh()
boardFrame.grid(column=0, row=0, padx=10, pady=10)
infoFrame.grid(column=1, row=0, padx=10, pady=10)
buttonFrame.grid(column=0, row=1, padx=10, pady=10)

root.title("15 Puzzle")

root.bind("<Key>", on_press)

root.mainloop()


