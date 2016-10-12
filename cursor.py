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
		self.message = ''
		self.row = 0
		self.col = 0

	def key(self, k):
		if self.mode == MODE_NORMAL:
			self.message = ''

			if k == ord('h'):
				if self.col > 0:
					self.col -= 1

			elif k == ord('j'):
				self.row += 1
				if self.row > self.sheet.maxRow():
					self.sheet.addRow(1)

			elif k == ord('k'):
				if self.row > 0:
					self.row -= 1

			elif k == ord('l'):
				self.col += 1
				if self.col > self.sheet.maxCol():
					self.sheet.addCol(1)

			elif k == ord('g'):
				self.mode = MODE_GOTO

			elif k == ord('i'):
				self.mode = MODE_INSERT

			elif k == ord('w'):
				try:
					self.sheet.write()
				except:
					self.message = 'Error writing file'
				else:
					self.message = 'Wrote file'

			elif k == ord('q'):
				self.sheet.quit()


		elif self.mode == MODE_GOTO:
			if k == ord('\n'): # enter
				self.goto(self.command)
				self.command = ''

			elif k == 27: # escape
				self.command = ''
				self.mode = MODE_NORMAL

			elif k == 127: # backspace
				self.command = self.command[:-1]

			else:
				self.command += chr(k)


		elif self.mode == MODE_INSERT:
			if k == ord('\n') or k == 27: # enter or escape
				self.mode = MODE_NORMAL

			elif k == 127: # backspace
				value = self.sheet.sheet[self.row][self.col]
				self.sheet.sheet[self.row][self.col] = value[:-1]

			else:
				self.sheet.sheet[self.row][self.col] += chr(k)


	def goto(self, posString):
		# Input validation
		m = re.search('\d+[a-zA-Z]+', posString)
		if m == None:
			self.message = 'Invalid input'
			self.mode = MODE_NORMAL
			return

		self.row, self.col = cellFromCode(posString)

		self.mode = MODE_NORMAL

	def printStatus(self, screen):
		screenHeight, screenWidth = screen.getmaxyx()

		# Print mode/command
		modeText = ''
		if self.mode == MODE_NORMAL:
			if self.message == '':
				modeText = 'NORMAL'
			else:
				modeText = self.message

		elif self.mode == MODE_INSERT:
			modeText = 'INSERT'

		elif self.mode == MODE_VISUAL:
			modeText = 'VISUAL'

		elif self.mode == MODE_GOTO:
			modeText = 'GOTO ' + self.command

		screen.addstr(screenHeight - 1, 0, modeText)

		posText = codeFromCell(self.row, self.col)
		screen.addstr(screenHeight - 1, screenWidth - len(posText) - 1, posText)

	def getPos(self):
		return self.row, self.col


def cellFromCode(code):
	code = code.upper()
	m = re.search('[a-zA-Z]', code)
	rowStr = code[:m.start()]
	colStr = code[m.start():]

	colStr = colStr[::-1]
	col = 0
	for i in range(len(colStr)):
		digit = ord(colStr[i]) - 64
		col += digit * 26 ** i
	col -= 1

	row = int(rowStr)

	return row, col

def codeFromCell(row, col):
	colStr = ''
	digit = col % 26
	col //= 26
	colStr = chr(digit + 65) + colStr
	while col > 0:
		digit = col % 26
		col //= 26
		colStr = chr(digit + 64) + colStr

	return str(row) + colStr

