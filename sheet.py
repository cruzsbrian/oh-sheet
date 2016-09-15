import curses

class Sheet:
	def __init__(self, filename):
		self.file = open(filename)
		self.sheet = []

		# Parse text file into 2D array
		for line in self.file.readlines():
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

	def main(self, screen):
		curses.curs_set(0)

		screen.clear()
		self.display(screen)
		screen.refresh()
		screen.getch()

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
				screen.addstr(row, colpos, self.sheet[row][col])
				colpos += colwidth[col] # increment column by needed width

s = Sheet(input("Filename: "))
curses.wrapper(s.main)

