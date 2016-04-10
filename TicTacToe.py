import sys
import os
class tic_tac_toe:
	def __init__(self):
		self.board=[0,0,0,0,0,0,0,0,0]
		self.turn = 0
	def display_board(self):
		os.system('clear')
		print " _ _ _ "
		count = 0
		for i in range(3):
			for j in range(3):
				if self.board[count]==0:
					sys.stdout.write('|_')
				elif self.board[count]==1:
					sys.stdout.write('|X')
				else :
					sys.stdout.write('|O')
				count = count + 1
			print "|"
	def won(self, board):
		for i in range(3):
			if (self.board[3*i]==self.board[3*i+1] and self.board[3*i+1]==self.board[3*i+2] and self.board[3*i+2]!=0):
				return self.board[3*i]
			if (self.board[i]==self.board[3+i] and self.board[3+i]==self.board[6+i] and self.board[6+i]!=0):
				return self.board[i]
		if self.board[0]==self.board[4] and self.board[4]==self.board[8] and self.board[8]!=0:
		  	return self.board[0]
		if self.board[2]==self.board[4] and self.board[4]==self.board[6] and self.board[6]!=0:
		  	return self.board[2]
		return 0
	def min_max(self,board,turn):
		x =self.won(board)
#		print turn,x,board
		if turn==8:
			return (x,-1)
		if x!=0:
			if x==2:
				return (1,-1)
			else: 
				return (-1,-1)
		if turn%2 == 0:
			mini = 99999
		else:
			maxi = -9999
		pos =-1
		for i in range(9):
			if board[i]==0:
				board[i] = (turn%2)+1
				new_score = self.min_max(board,turn+1)[0]
				board[i] = 0
				if turn%2 == 0:
					if new_score == -1:
						return (-1,i)	
					elif new_score<mini:
						mini = new_score
						pos = i
				else: 
					if new_score == 1:
						return (1,i)
					if new_score>maxi:
						maxi = new_score
						pos = i

		if turn%2==0:
			return (mini,pos)
		else:
			return (maxi,pos)

	def play_game(self):
		chance = (self.turn%2)+1
		print "turn=",self.turn
		if self.turn%2==0:
			print "player",chance," turn, select a position (1-9)"
			while(1):
				x = raw_input()
				if self.board[int(x)-1]==0:
					self.board[int(x)-1] = chance
					break
				else:
					print "invalid move, specify another position"
		else:
			move = self.min_max(self.board,self.turn)[1]
			self.board[move] = chance
		self.turn = self.turn + 1
		self.display_board()
		x = self.won(self.board)
		if x!=0:
			print "player ",x," won"
			return
		if self.turn < 9:
			self.play_game()
		elif self.turn==9 and x==0:
		  	print "tie"
		  	return 

	

game = tic_tac_toe()
game.display_board()
game.play_game()
