from subprocess import call
import sys
from time import sleep


class Data(object):
	def __init__(self, path, p, g, w, d, b):
		self.dead = False
		self.player = p
		self.ghost = g
		self.wall = w
		self.dot = d
		self.blank = b
		# open the file as a string, split block into rows by newline,
		# split rows into chars via list(), use [:-1] to ignore the newline at the end of the file
		self.board = [list(r) for r in open(path).read().split("\n")[:-1]]
		self.px = self.py = 0
		self.gx = self.gy = 0
		for r in range(len(self.board)):
			for c in range(len(self.board[r])):
				if self.board[r][c] == self.player:
					self.px = c
					self.py = r
				elif self.board[r][c] == self.ghost:
					self.gx = c
					self.gy = r
		self.collected = 0
		self.total = 0
		for r in self.board:
			for c in r:
				if c == self.dot or c == self.ghost:
					self.total += 1
		self.ghost_over = self.dot


def update_player(data, move):
	if data.px == data.gx and data.py == data.gy:
		data.dead = True
		return
	data.board[data.py][data.px] = data.blank
	if move is "l" and data.px > 0 and data.board[data.py][data.px-1] is not data.wall:
		data.px -= 1
	elif move is "r" and data.px < len(data.board[0])-1 and data.board[data.py][data.px+1] is not data.wall:
		data.px += 1
	elif move is "u" and data.py > 0 and data.board[data.py-1][data.px] is not data.wall:
		data.py -= 1
	elif move is "d" and data.py < len(data.board)-1 and data.board[data.py+1][data.px] is not data.wall:
		data.py += 1
	if data.board[data.py][data.px] == data.dot:
		data.collected += 1
	data.board[data.py][data.px] = data.player


def update_ghost(data):
	data.board[data.gy][data.gx] = data.ghost_over
	dx = data.px - data.gx
	dy = data.py - data.gy
	if abs(dx) > abs(dy):
		if dx < 0 and data.gx > 0 and data.board[data.gy][data.gx-1] is not data.wall:
			data.gx -= 1
		elif dx > 0 and data.gx < len(data.board[0])-1 and data.board[data.gy][data.gx+1] is not data.wall:
			data.gx += 1
	else:
		if dy < 0 and data.gy > 0 and data.board[data.gy-1][data.gx] is not data.wall:
			data.gy -= 1
		elif dy > 0 and data.gy < len(data.board)-1 and data.board[data.gy+1][data.gx] is not data.wall:
			data.gy += 1
	data.ghost_over = data.board[data.gy][data.gx]
	data.board[data.gy][data.gx] = data.ghost


def display(board):
	call("clear")
	for r in board:
		print("".join(r))


def main(argv):
	inputs = argv if argv[0] in ["l", "r", "u", "d"] else argv[1:]
	data = Data("level1.txt", "@", "0", "#", ".", " ")
	for i in inputs:
		update_player(data, i)
		update_ghost(data)
		# sleep(0.1)
		# display(data.board)
		if data.dead:
			# print("You lose!")
			break
		elif data.collected == data.total:
			# print("You win!")
			break
	return data


if __name__ == "__main__":
	main(sys.argv)
