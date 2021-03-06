import curses
import re

MODE_NORMAL = 0
MODE_INSERT = 1
MODE_VISUAL = 2
MODE_COMMAND = 3

COMM_NONE = 0
COMM_GOTO = 1
COMM_WRITE = 2

class Cursor:
	def __init__(self, sheet):
		self.sheet = sheet
		self.mode = MODE_NORMAL
		self.command = COMM_NONE
		self.message = ''
		self.input = ''
		self.inputPos = 0
		self.row = 0
		self.col = 0
		self.cellPos = 0
		self.modified = False

	def key(self, k):
		if self.mode == MODE_NORMAL:
			self.message = ''

			self.command = COMM_NONE
			self.input = ''

			# Key inputs
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
				self.command = COMM_GOTO
				self.message = 'GOTO '
				self.mode = MODE_COMMAND

			elif k == ord('i'):
				self.cellPos = len(self.sheet.sheet[self.row][self.col])
				self.mode = MODE_INSERT

			elif k == ord('r'):
				self.sheet.sheet[self.row][self.col] = ''
				self.mode = MODE_INSERT

			elif k == ord('w'):
				if self.sheet.filename == '':
					self.message = 'Enter a filename: '
					self.command = COMM_WRITE
					self.mode = MODE_COMMAND
				else:
					try:
						self.sheet.write()
					except:
						self.message = 'Error writing file'
					else:
						self.message = 'Wrote file'
						self.modified = False

			elif k == ord('q'):
				if self.modified:
					self.message = 'Unsaved changes: press q again to quit without saving, or w to save'
					self.modified = False
				else:
					self.sheet.quit()


		elif self.mode == MODE_COMMAND:
			if k == ord('\n'): # enter
				if self.command == COMM_GOTO:
					self.goto(self.input)

				elif self.command == COMM_WRITE:
					self.sheet.filename = self.input

					try:
						self.sheet.write()
					except:
						self.message = 'Error writing file'
					else:
						self.message = 'Wrote file'
						self.modified = False

				self.mode = MODE_NORMAL

			elif k == 27: # escape
				self.input = ''
				self.mode = MODE_NORMAL

			elif k == 127: # backspace
				self.input = self.input[:-1]

			else:
				self.input += chr(k)


		elif self.mode == MODE_INSERT:
			value = self.sheet.sheet[self.row][self.col]

			if k == ord('\n') or k == 27: # enter or escape
				self.cellPos = 0
				self.mode = MODE_NORMAL

			elif k == 127: # backspace
				if self.cellPos > 0:
					self.sheet.sheet[self.row][self.col] = value[:self.cellPos - 1] + value[self.cellPos:]
					self.cellPos -= 1
					self.modified = True

			elif k == curses.KEY_LEFT:
				if self.cellPos > 0:
					self.cellPos -= 1

			elif k == curses.KEY_RIGHT:
				if self.cellPos < len(value):
					self.cellPos += 1

			else:
				self.sheet.sheet[self.row][self.col] = value[:self.cellPos] + chr(k) + value[self.cellPos:]
				self.cellPos += 1
				self.modified = True


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

		elif self.mode == MODE_COMMAND:
			modeText = self.message + self.input

		filename = self.sheet.filename
		if filename == '':
			filename = 'New File'

		screen.addstr(screenHeight - 1, 0, '[' + filename + '] ' + modeText)

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

