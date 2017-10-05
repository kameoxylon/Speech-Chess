#! /usr/bin/env python
"""
 Project: Python Chess
 File name: PythonChessMain.py
 Description:  Chess for player vs. player, player vs. AI, or AI vs. AI.
	Uses Tkinter to get initial game parameters.  Uses Pygame to draw the 
	board and pieces and to get user mouse clicks.  Run with the "-h" option 
	to get full listing of available command line flags.  
	
 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 *******
 This program is free software; you can redistribute it and/or modify 
 it under the terms of the GNU General Public License as published by 
 the Free Software Foundation; either version 2 of the License, or 
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful, but 
 WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
 or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License 
 for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

 *******
 Version history:

 v 0.7 - 27 April 2009.  Dramatically lowered CPU usage by using 
   "pygame.event.wait()" rather than "pygame.event.get()" in
   ChessGUI_pygame.GetPlayerInput().
 
 v 0.6 - 20 April 2009.  Some compatibility fixes: 1) Class: instead of 
   Class(), 2) renamed *.PNG to *.png, 3) rendered text with antialias flag on.  
   Also changed exit() to sys.exit(0). (Thanks to tgfcoder from pygame website 
   for spotting these errors.)
 
 v 0.5 - 16 April 2009.  Added new AI functionality - created 
   "ChessAI_defense" and "ChessAI_offense."  Created PythonChessAIStats 
   class for collecting AI vs. AI stats.  Incorporated Python module 
   OptionParser for better command line parsing.
   
 v 0.4 - 14 April 2009.  Added better chess piece graphics from Wikimedia
   Commons.  Added a Tkinter dialog box (ChessGameParams.py) for getting
   the game setup parameters.  Converted to standard chess notation for 
   move reporting and added row/col labels around the board.
 
 v 0.3 - 06 April 2009.  Added pygame graphical interface.  Includes
   addition of ScrollingTextBox class.
   
 v 0.2 - 04 April 2009.  Broke up the program into classes that will
   hopefully facilitate easily incorporating graphics or AI play.
 
 v 0.1 - 01 April 2009.  Initial release.  Draws the board, accepts
   move commands from each player, checks for legal piece movement.
   Appropriately declares player in check or checkmate.

 Possible improvements:
   - Chess Rules additions, ie: Castling, En passant capture, Pawn Promotion
   - Better AI
   - Network play
   
"""

from ChessBoard import ChessBoard
from ChessAI import ChessAI_random, ChessAI_defense, ChessAI_offense
from ChessPlayer import ChessPlayer
from ChessGUI_text import ChessGUI_text
from ChessGUI_pygame import ChessGUI_pygame
from ChessRules import ChessRules
from ChessGameParams import TkinterGameSetupParams

from optparse import OptionParser
import time
import pygame, sys

class PythonChessMain:
	def __init__(self,options):
		if options.debug:
			self.Board = ChessBoard(2)
			self.debugMode = True
		else:
			self.Board = ChessBoard(0)#0 for normal board setup; see ChessBoard class for other options (for testing purposes)
			self.debugMode = False

		self.Rules = ChessRules()
		
	def SetUp(self,options):
		#gameSetupParams: Player 1 and 2 Name, Color, Human/AI level
		if self.debugMode:
			player1Name = 'Kasparov'
			player1Type = 'human'
			player1Color = 'white'
			player2Name = 'Light Blue'
			player2Type = 'randomAI'
			player2Color = 'black'		
		else:
			GameParams = TkinterGameSetupParams()
			(player1Name, player1Color, player1Type, player2Name, player2Color, player2Type) = GameParams.GetGameSetupParams()

		self.player = [0,0]
		if player1Type == 'human':
			self.player[0] = ChessPlayer(player1Name,player1Color)
		elif player1Type == 'randomAI':
			self.player[0] = ChessAI_random(player1Name,player1Color)
		elif player1Type == 'defenseAI':
			self.player[0] = ChessAI_defense(player1Name,player1Color)
		elif player1Type == 'offenseAI':
			self.player[0] = ChessAI_offense(player1Name,player1Color)
			
		if player2Type == 'human':
			self.player[1] = ChessPlayer(player2Name,player2Color)
		elif player2Type == 'randomAI':
			self.player[1] = ChessAI_random(player2Name,player2Color)
		elif player2Type == 'defenseAI':
			self.player[1] = ChessAI_defense(player2Name,player2Color)
		elif player2Type == 'offenseAI':
			self.player[1] = ChessAI_offense(player2Name,player2Color)
			
		if 'AI' in self.player[0].GetType() and 'AI' in self.player[1].GetType():
			self.AIvsAI = True
		else:
			self.AIvsAI = False
			
		if options.pauseSeconds > 0:
			self.AIpause = True
			self.AIpauseSeconds = int(options.pauseSeconds)
		else:
			self.AIpause = False
			
		#create the gui object - didn't do earlier because pygame conflicts with any gui manager (Tkinter, WxPython...)
		if options.text:
			self.guitype = 'text'
			self.Gui = ChessGUI_text()
		else:
			self.guitype = 'pygame'
			if options.old:
				self.Gui = ChessGUI_pygame(0)
			else:
				self.Gui = ChessGUI_pygame(1)
			
	def MainLoop(self):
		currentPlayerIndex = 0
		turnCount = 0
		while not self.Rules.IsCheckmate(self.Board.GetState(),self.player[currentPlayerIndex].color):
			print "1"
			board = self.Board.GetState()
			currentColor = self.player[currentPlayerIndex].GetColor()
			print "2"
			#hardcoded so that player 1 is always white
			if currentColor == 'white':
				turnCount = turnCount + 1
			print "3"
			self.Gui.PrintMessage("")
			baseMsg = "TURN %s - %s (%s)" % (str(turnCount),self.player[currentPlayerIndex].GetName(),currentColor)
			print "4"
			self.Gui.PrintMessage("-----%s-----" % baseMsg)
			self.Gui.Draw(board)
			print "5"
			if self.Rules.IsInCheck(board,currentColor):
				self.Gui.PrintMessage("Warning..."+self.player[currentPlayerIndex].GetName()+" ("+self.player[currentPlayerIndex].GetColor()+") is in check!")
			
			print "6"
			if self.player[currentPlayerIndex].GetType() == 'AI':
				moveTuple = self.player[currentPlayerIndex].GetMove(self.Board.GetState(), currentColor) 
			else:
				moveTuple = self.Gui.GetPlayerInput(board,currentColor)
			print "7"
			moveReport = self.Board.MovePiece(moveTuple) #moveReport = string like "White Bishop moves from A1 to C3" (+) "and captures ___!"
			self.Gui.PrintMessage(moveReport)
			print "8"
			currentPlayerIndex = (currentPlayerIndex+1)%2 #this will cause the currentPlayerIndex to toggle between 1 and 0
			print "9"
			if self.AIvsAI and self.AIpause:
				time.sleep(self.AIpauseSeconds)
		
		self.Gui.PrintMessage("CHECKMATE!")
		winnerIndex = (currentPlayerIndex+1)%2
		self.Gui.PrintMessage(self.player[winnerIndex].GetName()+" ("+self.player[winnerIndex].GetColor()+") won the game!")
		self.Gui.EndGame(board)
		

parser = OptionParser()
parser.add_option("-d", dest="debug",
				  action="store_true", default=False, help="Enable debug mode (different starting board configuration)")
parser.add_option("-t", dest="text",
				  action="store_true", default=False, help="Use text-based GUI")
parser.add_option("-o", dest="old",
				  action="store_true", default=False, help="Use old graphics in pygame GUI")
parser.add_option("-p", dest="pauseSeconds", metavar="SECONDS",
				  action="store", default=0, help="Sets time to pause between moves in AI vs. AI games (default = 0)")


(options,args) = parser.parse_args()

game = PythonChessMain(options)
game.SetUp(options)
game.MainLoop()


	