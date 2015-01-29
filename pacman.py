from subprocess import call
import sys
from time import sleep


class Data(object):
	def __init__(self, p, w, d, b):
		self.dead = False
		self.player = p
		self.wall = w
		self.dot = d
		self.blank = b
		# open the file as a string, split block into rows by newline,
		# split rows into chars via list(), use [:-1] to ignore the newline at the end of the file
		self.board = [list(r) for r in open("level.txt").read().split("\n")[:-1]]
		self.px = 0
		self.py = 0
		for r in range(len(self.board)):
			for c in range(len(self.board[r])):
				if self.board[r][c] == self.player:
					self.px = c
					self.py = r
		self.collected = 0
		self.total = 0
		for r in self.board:
			for c in r:
				if c == self.dot:
					self.total += 1


def update(data, move):
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


def display(data):
	call("clear")
	for r in data.board:
		print("".join(r))


def check(data):
	if data.dead:
		# print("You lose!")
		sys.exit()
	if data.collected == data.total:
		# print("You win!")
		sys.exit()


def main(argv):
	inputs = argv if argv[0] in ["l", "r", "u", "d"] else argv[1:]
	data = Data("@", "#", ".", " ")
	for i in inputs:
		update(data, i)
		# sleep(0.1)
		# display(data)
		check(data)
	return [data.collected, data.total]


if __name__ == "__main__":
	main(sys.argv)
# TODO: ADD GHOSTS - NO RANDOMNESS
