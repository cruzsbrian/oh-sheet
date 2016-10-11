import re

def calc(exp):
	try:
		exp = splitstring(exp)
		exp = parse(exp)
		val = evaluate(exp)
		return str(val)
	except:
		return 'ERR'


numPattern = re.compile('^-?\d*.?\d+$')
def isNumber(ch):
	if numPattern.match(ch):
		return True
	return False


def precedence(op):
	if op in '()':
		return 0

	if op in '+-':
		return 1

	if op in '*/':
		return 2

	if op in '^':
		return 3


def splitstring(exp):
	out = []
	word = ''

	for ch in exp:
		if ch.isdigit() or ch == '.':
			word += ch
		else:
			if ch == '-' and word == '':
				word = '-'
			else:
				if word != '':
					out.append(word)
					word = ''
				out.append(ch)

	if word != '':
		out.append(word)

	return out


# Google "shunting yard algorithm"
def parse(exp):
	out = []
	ops = []

	for ch in exp:
		if isNumber(ch):
			out.append(ch)
		elif ch == '(':
			ops.append(ch)
		elif ch == ')':
			while len(ops) > 0 and ops[-1] != '(':
				out.append(ops.pop())
			ops.pop()
		else:
			while len(ops) > 0 and precedence(ops[-1]) > precedence(ch):
				out.append(ops.pop())
			ops.append(ch)

	while len(ops) >= 1:
		out.append(ops.pop())

	return out

def evaluate(exp):
	ins = []
	for ch in exp:
		if isNumber(ch):
			ins.append(float(ch))
		else:
			in1 = ins.pop()
			in2 = ins.pop()
			out = 0

			if ch == '+':
				out = in1 + in2
			elif ch == '-':
				out = in2 - in1
			elif ch == '*':
				out = in1 * in2
			elif ch == '/':
				out = in2 / in1
			elif ch == '^':
				out = in2 ** in1

			ins.append(out)

	return ins[0]

