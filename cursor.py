import curses

MODE_NORMAL = 0
MODE_INSERT = 1
MODE_VISUAL = 2

class Cursor:
	def __init__(self, sheet):
		self.sheet = sheet
		self.mode = MODE_NORMAL
		self.row = 0
		self.col = 0

	def key(self, k):
		k = chr(k)

		if self.mode == MODE_NORMAL:
			if k == 'h':
				if self.col > 0:
					self.col -= 1

			elif k == 'j':
				if self.row < self.sheet.maxRow():
					self.row += 1

			elif k == 'k':
				if self.row > 0:
					self.row -= 1

			elif k == 'l':
				if self.col < self.sheet.maxCol():
					self.col += 1

			elif k == 'q':
				self.sheet.quit()

	def printPos(self, screen):
		rowStr = chr(self.row + 65)
		colStr = str(self.col)
		screenHeight, screenWidth = screen.getmaxyx()

		text = rowStr + colStr
		screen.addstr(screenHeight - 1, screenWidth - len(text) - 1, text)

	def getPos(self):
		return self.row, self.col

