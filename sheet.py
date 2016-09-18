import curses
import cursor

class Sheet:
	def __init__(self, filename):
		self.file = open('test.csv')
		self.sheet = []

		# Parse text file into 2D array
		for line in self.file.readlines():
			line = line[:-1]
			row = []
			for val in line.split(','):
				row.append(val)
			self.sheet.append(row)

		# Ensure all rows are same number of cells
		maxLen = 0
		for row in self.sheet:
			if len(row) > maxLen:
				maxLen = len(row)
		for row in self.sheet:
			if len(row) < maxLen:
				row += [' '] * (maxLen - len(row))

		# Set up the cursor
		self.cursor = cursor.Cursor(self)

		self.running = True

	def main(self, screen):
		curses.curs_set(0)

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
				text += ' ' * (colwidth[col] - len(text)) # pad cell with extra spaces

				if (row, col) == self.cursor.getPos():
					screen.addstr(row, colpos, text, curses.color_pair(1))
				else:
					screen.addstr(row, colpos, text)
				colpos += colwidth[col] # increment column by needed width

		self.cursor.printPos(screen)

	def quit(self):
		self.running = False

	def maxRow(self):
		return len(self.sheet) - 1

	def maxCol(self):
		return len(self.sheet[0]) - 1

s = Sheet(input(""))
curses.wrapper(s.main)

