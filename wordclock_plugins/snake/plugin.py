# Authored by Bernhard Weyrauch
# http://www.bernhardweyrauch.de

import os
import time
import random
import sys
import re
from Snakeobject import Snakeobject
import wordclock_tools.wordclock_colors as wcc

class plugin:
    '''
    A class to implement the snake game
    '''

    def __init__(self, config):
        '''
        Initializations for the startup of the current wordclock plugin
        '''
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "Snake"
        self.description = "... back to the 90ies"

    def updatePoints(self, sn, wcd):
        points = sn.data["points"]
        '''
        The minute pixels of the wordclock represent the 'big' points.
        A big point will represent 12 single points.
        The first four big points will be in yellow color, then the points become pink
        '''
        m = int(points/12)
        if (m >= 1): wcd.setColorBy1DCoordinates([113], wcc.YELLOW)
        if (m >= 2): wcd.setColorBy1DCoordinates([1], wcc.YELLOW)
        if (m >= 3): wcd.setColorBy1DCoordinates([112], wcc.YELLOW)
        if (m >= 4): wcd.setColorBy1DCoordinates([0], wcc.YELLOW)
        if (m >= 5): wcd.setPixesetColorBy1DCoordinateslColor([113], wcc.PINK)
        if (m >= 6): wcd.setColorBy1DCoordinates([1], wcc.PINK)
        if (m >= 7): wcd.setColorBy1DCoordinates([112], wcc.PINK)
        if (m >= 8): wcd.setColorBy1DCoordinates([0], wcc.PINK)

    def keyPressed(self, event, sn, wcd, wci):
        sn.data["ignoreNextTimerEvent"] = True # for better timing
                
        # now process keys that only work if the game is not over
        if (sn.data["isGameOver"] == False):
            if (event == wci.EVENT_BUTTON_LEFT):
                self.moveSnake(sn, 0, -2)
            elif (event == wci.EVENT_BUTTON_RIGHT):
                self.moveSnake(sn, 0, 2)
        self.redrawAll(sn, wcd)
    
    def moveSnake(self, sn, drow, dcol):
        snakeBoard = sn.data["snakeBoard"]
        rows = len(snakeBoard)
        cols = len(snakeBoard[0])
        
        headRow = sn.data["headRow"]
        headCol = sn.data["headCol"]
        
        if((dcol == -2) or (dcol == 2)):
            dcol=int(dcol/2)
            # left moving and left pressed?
            if ((sn.data["snakeDrow"] == 0) and (sn.data["snakeDcol"] == -1) and (dcol == -1)):
                drow=1
                dcol=0
            # right moving and left pressed?
            elif ((sn.data["snakeDrow"] == 0) and (sn.data["snakeDcol"] == 1) and (dcol == -1)):
                drow=-1
                dcol=0
            # up moving and left pressed?
            elif ((sn.data["snakeDrow"] == -1) and (sn.data["snakeDcol"] == 0) and (dcol == -1)):
                drow=0
                dcol=-1
            # down moving and left pressed?
            elif ((sn.data["snakeDrow"] == 1) and (sn.data["snakeDcol"] == 0) and (dcol == -1)):
                drow=0
                dcol=1
            # left moving and right pressed?
            elif ((sn.data["snakeDrow"] == 0) and (sn.data["snakeDcol"] == -1) and (dcol == 1)):
                drow=-1
                dcol=0
            # right moving and right pressed?
            elif ((sn.data["snakeDrow"] == 0) and (sn.data["snakeDcol"] == 1) and (dcol == 1)):
                drow=1
                dcol=0
            # up moving and right pressed?
            elif ((sn.data["snakeDrow"] == -1) and (sn.data["snakeDcol"] == 0) and (dcol == 1)):
                drow=0
                dcol=1
            # down moving and right pressed?
            elif ((sn.data["snakeDrow"] == 1) and (sn.data["snakeDcol"] == 0) and (dcol == 1)):
                drow=0
                dcol=-1
        
        # move the snake one step forward in the given direction.
        sn.data["snakeDrow"] = drow # store direction for next timer event
        sn.data["snakeDcol"] = dcol
       
        newHeadRow = headRow + drow
        newHeadCol = headCol + dcol
        
        self.findSnakeTail(sn)
        isLoop=False
        if ((sn.data["tailRow"] == newHeadRow) and (sn.data["tailCol"] == newHeadCol)):
            isLoop=True
        
        if ((newHeadRow < 0) or (newHeadRow >= rows) or
            (newHeadCol < 0) or (newHeadCol >= cols)):
            # snake ran off the board
            self.gameOver(sn)
        elif ((snakeBoard[newHeadRow][newHeadCol] > 0) and (isLoop == False)):
            # snake ran into itself!
            self.gameOver(sn)
        elif (snakeBoard[newHeadRow][newHeadCol] < 0):
            # eating food!  Yum!
            sn.data["points"] = 1 + sn.data["points"]
            snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol];
            sn.data["headRow"] = newHeadRow
            sn.data["headCol"] = newHeadCol
            self.placeFood(sn)
        else:
            # normal move forward (not eating food)
            snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol];
            sn.data["headRow"] = newHeadRow
            sn.data["headCol"] = newHeadCol
            self.removeTail(sn)
    
    def removeTail(self, sn):
        # find every snake cell and subtract 1 from it.  When we're done,
        # the old tail (which was 1) will become 0, so will not be part of the snake.
        # So the snake shrinks by 1 value, the tail.
        snakeBoard = sn.data["snakeBoard"]
        rows = len(snakeBoard)
        cols = len(snakeBoard[0])
        for row in range(rows):
            for col in range(cols):
                if (snakeBoard[row][col] > 0):
                    snakeBoard[row][col] -= 1

    def gameOver(self, sn):
        sn.data["isGameOver"] = True
    
    def drawSnakeCell(self, sn, snakeBoard, row, col, headRow, headCol, wcd):
        wcd.setColorBy2DCoordinates(col, row, wcc.BLACK)
        
        if((row == headRow) and (headCol == col)):
            # draw snake body head
             wcd.setColorBy2DCoordinates(col, row, wcc.YELLOW) #Green
        elif (snakeBoard[row][col] > 0):
            # draw part of the snake body
            wcd.setColorBy2DCoordinates(col, row, wcc.Color(34, 177, 76)) #Green
        elif (snakeBoard[row][col] < 0):
            # draw food
            wcd.setColorBy2DCoordinates(col, row, wcc.RED)
        
    def drawSnakeBoard(self, sn, wcd):
        snakeBoard = sn.data["snakeBoard"]
        
        self.findSnakeHead(sn)
        headRow = sn.data["headRow"]
        headCol = sn.data["headCol"]

        rows = len(snakeBoard)
        cols = len(snakeBoard[0])
        for row in range(rows):
            for col in range(cols):
                #print(str(row) + " " + str(col))
                self.drawSnakeCell(sn, snakeBoard, row, col, headRow, headCol, wcd)
    
    def redrawAll(self, sn, wcd):
        wcd.resetDisplay()
        self.drawSnakeBoard(sn, wcd)
        self.updatePoints(sn, wcd)
        wcd.show()
        if (sn.data["isGameOver"] == True):
            for i in range(3):
                wcd.resetDisplay()
                wcd.show()
                time.sleep(0.3)
                self.drawSnakeBoard(sn, wcd)
                wcd.show()
                time.sleep(0.6)
            # print("Game Over!!!")
            # wcd.showText("Game Over", None, wcc.BLUE)
            return
        
    def placeFood(self, sn):
        # place food (-1) in a random location on the snakeBoard, but
        # keep picking random locations until we find one that is not
        # part of the snake!
        snakeBoard = sn.data["snakeBoard"]
        rows = len(snakeBoard)
        cols = len(snakeBoard[0])
        while True:
            row = random.randint(0,rows-1)
            col = random.randint(0,cols-1)
            if (snakeBoard[row][col] == 0):
                break
        snakeBoard[row][col] = -1

    def findSnakeHead(self, sn):
        # find where snakeBoard[row][col] is largest, and
        # store this location in headRow, headCol
        snakeBoard = sn.data["snakeBoard"]
        rows = len(snakeBoard)
        cols = len(snakeBoard[0])
        headRow = 0
        headCol = 0
        for row in range(rows):
            for col in range(cols):
                if (snakeBoard[row][col] > snakeBoard[headRow][headCol]):
                    headRow = row
                    headCol = col
        sn.data["headRow"] = headRow
        sn.data["headCol"] = headCol
        
    def findSnakeTail(self, sn):
        # find where snakeBoard[row][col] is largest, and
        # store this location in tailRow, tailCol
        snakeBoard = sn.data["snakeBoard"]
        rows = len(snakeBoard)
        cols = len(snakeBoard[0])
        tailRow = 0
        tailCol = 0
        for row in range(rows):
            for col in range(cols):
                if (snakeBoard[row][col] == 1):
                    tailRow = row
                    tailCol = col
        sn.data["tailRow"] = tailRow
        sn.data["tailCol"] = tailCol
        
    def loadSnakeBoard(self, sn):
        rows = sn.data["rows"]
        cols = sn.data["cols"]
        snakeBoard = [ ]
        for row in range(rows):
            snakeBoard += [[0] * cols]
        snakeBoard[int(rows/2)][int(cols/2)+3] = 1
        sn.data["snakeBoard"] = snakeBoard
        
        for i in range(4):
            self.findSnakeHead(sn)
            headRow = int(sn.data["headRow"])
            headCol = int(sn.data["headCol"])
            newHeadCol = headCol-1
            snakeBoard[headRow][newHeadCol] = 1 + snakeBoard[headRow][headCol];
            sn.data["headCol"] = newHeadCol
            sn.data["snakeBoard"] = snakeBoard
            
        
        self.placeFood(sn)
        
    def init(self, sn, wcd):
        self.loadSnakeBoard(sn)
        sn.data["isGameOver"] = False
        sn.data["snakeDrow"] = 0
        sn.data["snakeDcol"] = -1 # start moving left
        sn.data["ignoreNextTimerEvent"] = False
        sn.data["points"] = 0
        self.redrawAll(sn, wcd)
        
    def run(self, wcd, wci):
        '''
        Init snake game with rows and cols setup
        '''
        sn = Snakeobject(11,10)
        self.init(sn, wcd)
        skipWait=False
        while True:
            event=0
            if (sn.data["isGameOver"] == True):
                return
            
            if (skipWait == False):
                event = wci.waitForEvent(1)
            else:
                skipWait=False
            if (event == wci.EVENT_BUTTON_RETURN):
                return # Exit snake and return to wordclock
            
            if event > 0:
                self.keyPressed(event, sn, wcd, wci)
                time.sleep(wci.lock_time)
                skipWait=True
            else:
                ignoreThisTimerEvent = sn.data["ignoreNextTimerEvent"]
                sn.data["ignoreNextTimerEvent"] = False
                if ((sn.data["isGameOver"] == False) and
                    (ignoreThisTimerEvent == False)):
                    # only process timerFired if game is not over
                    drow = sn.data["snakeDrow"]
                    dcol = sn.data["snakeDcol"]
                    self.moveSnake(sn, drow, dcol)
                    self.redrawAll(sn, wcd)
                
