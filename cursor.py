import curses
import re

MODE_NORMAL = 0
MODE_INSERT = 1
MODE_VISUAL = 2
MODE_GOTO = 3

class Cursor:
	def __init__(self, sheet):
		self.sheet = sheet
		self.mode = MODE_NORMAL
		self.command = ''
		self.row = 0
		self.col = 0

	def key(self, k):
		if self.mode == MODE_NORMAL:
			if k == ord('h'):
				if self.col > 0:
					self.col -= 1

			elif k == ord('j'):
				if self.row < self.sheet.maxRow():
					self.row += 1

			elif k == ord('k'):
				if self.row > 0:
					self.row -= 1

			elif k == ord('l'):
				if self.col < self.sheet.maxCol():
					self.col += 1

			elif k == ord('g'):
				self.mode = MODE_GOTO

			elif k == ord('q'):
				self.sheet.quit()


		elif self.mode == MODE_GOTO:
			if k == ord('\n'): # enter
				self.goto(self.command)
				self.command = ''
				self.mode = MODE_NORMAL

			elif k == 27: # escape
				self.command = ''
				self.mode = MODE_NORMAL

			elif k == 127: # backspace
				self.command = self.command[:-1]

			else:
				self.command += chr(k)

	def goto(self, posString):
		# Split into row and col portion
		m = re.search('[a-zA-Z]', posString) # find first letter
		rowStr = posString[:m.start()]
		colStr = posString[m.start():]

		self.row = int(rowStr)
		self.col = ord(colStr) - 65

	def printStatus(self, screen):
		screenHeight, screenWidth = screen.getmaxyx()

		# Print mode/command
		modeText = ''
		if self.mode == MODE_NORMAL:
			modeText = 'NORMAL'

		elif self.mode == MODE_INSERT:
			modeText = 'INSERT'

		elif self.mode == MODE_VISUAL:
			modeText = 'VISUAL'

		elif self.mode == MODE_GOTO:
			modeText = 'GOTO ' + self.command

		screen.addstr(screenHeight - 1, 0, modeText)

		# Print position
		rowStr = str(self.row)
		colStr = chr(self.col + 65)

		posText = rowStr + colStr
		screen.addstr(screenHeight - 1, screenWidth - len(posText) - 1, posText)

	def getPos(self):
		return self.row, self.col

