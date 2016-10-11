import curses
import cursor
import calc

class Sheet:
	def __init__(self):
		self.file = open('test.csv')
		self.sheet = []

		# Parse text file into 2D array
		for line in self.file.readlines():
			line = line[:-1]
			row = []
			for val in line.split(','):
				row.append(val)
			self.sheet.append(row)

		# Check for empty file
		if self.sheet == []:
			self.sheet = [[]]

		# Ensure all rows are same number of cells
		maxLen = 0
		for row in self.sheet:
			if len(row) > maxLen:
				maxLen = len(row)
		for row in self.sheet:
			if len(row) < maxLen:
				row += [''] * (maxLen - len(row))

		# Set up the cursor
		self.cursor = cursor.Cursor(self)

		self.running = True

	def main(self, screen):
		curses.curs_set(0)
		self.height, self.width = screen.getmaxyx()

		# colors to highlight cursor cell
		curses.start_color()
		curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

		while self.running:
			screen.clear()
			self.display(screen)
			screen.refresh()

			self.cursor.key(screen.getch())

	def display(self, screen):
		# Find needed max width for each column
		colwidth = [4] * len(self.sheet[0])
		for row in range(len(self.sheet)):
			for col in range(len(self.sheet[row])):
				length = len(self.sheet[row][col]) + 1
				if length > colwidth[col]:
					colwidth[col] = length

		# Display the sheet
		for row in range(len(self.sheet)):
			colpos = 0
			for col in range(len(self.sheet[row])):
				text = self.sheet[row][col]

				# Calculations if necessary
				if len(text) > 0 and text[0] == '=' and (row, col) != self.cursor.getPos():
					text = calc.calc(text[1:])

				text += ' ' * (colwidth[col] - len(text)) # pad cell with extra spaces

				if row < self.height and colpos + len(text) < self.width:
					if (row, col) == self.cursor.getPos():
						screen.addstr(row, colpos, text, curses.color_pair(1))
					else:
						screen.addstr(row, colpos, text)

				colpos += colwidth[col] # increment column by needed width

		self.cursor.printStatus(screen)

	def write(self):
		sheetfile = open('output.csv', 'w')

		mr = self.maxWrittenRow() + 1
		mc = self.maxWrittenCol() + 1
		for row in range(mr):
			writerow = self.sheet[row][:mc]
			sheetfile.write(','.join(writerow) + '\n')
		sheetfile.close()

	def quit(self):
		self.running = False

	def addRow(self, n):
		cols = len(self.sheet[0])
		for i in range(n):
			self.sheet.append([''] * cols)

	def addCol(self, n):
		for row in self.sheet:
			row += [''] * n

	def maxRow(self):
		return len(self.sheet) - 1

	def maxCol(self):
		return len(self.sheet[0]) - 1

	def maxWrittenRow(self):
		row = 0
		for i in range(len(self.sheet)):
			for cell in self.sheet[i]:
				if cell != '':
					row = i

		return row

	def maxWrittenCol(self):
		col = 0
		for row in self.sheet:
			for i in range(len(row)):
				if row[i] != '' and i > col:
					col = i

		return col


s = Sheet()
curses.wrapper(s.main)

