"""
Simplier is an esoteric programming language based on the concept of simplicity.
Some of the features of this language include:
- Small instruction names
- First line is never executed and can be as long as you want
- No repetition of lines (lines with more than one instruction can't be repeated)
- Maximum of 60 characters per line
- Lines must end with ; and everything after it is ignored but still counted for the 60 character limit
- No complex data types
- Character are given using their ASCII value
This language is interpreted by the Simplier Interpreter, which is written in Python.
"""

## interpreter settings
warn_error = False # if True, warnings will be treated as errors

## code
file_path = "test.simple" #input("Enter the file path: ")
if not file_path.endswith(".simple"): raise Exception("File must be a .simple file")

with open(file_path, "r") as file: code = file.read().split("\n")

# define the variables
is_running = True
variables = {} # name: value (tuple[type, value])
functions = {} # name: code (list[str])
curent_line = 1

def stop():
	"""stop the program"""
	global is_running
	is_running = False
	exit()
def error(message: str = "An unknow error occured on line {}".format(curent_line)) -> None:
	"""print the error message in red and exit the program"""
	print("\033[91mError: " + message + "\033[0m")
	stop()
def warn(message: str = "", is_error: bool = warn_error) -> None:
	"""print the warning message in yellow, unless warn_error is True"""
	if message == "": error("An unknow warning occured")
	elif is_error: error(message + " (warn -> error)")
	else: print("\033[93mWarning: " + message + "\033[0m")

warn("This language is still in development, so it may not work as expected", False)

# Remove empty lines and comments, return error if line is too long, repeated or empty
if len(code) > 1: code = code[1:]
else:error("File is empty")
for i in range(len(code)):
	if len(code[i]) > 60:
		error("Line {} is so long".format(i + 2))
	if not ";" in code[i] or code[i].strip().startswith(";"):
		error("Line {} is empty".format(i + 2))
	code[i] = code[i][:code[i].index(";")] # remove comments
	if len(code[i].split(" ")) > 2 and code[i] in code[:i]:
		error("Line {} is repeated".format(i + 2))

# main function
def run(words: list[str]) -> None:
	global curent_line, curent_word
	match words[0]:
		case "var": # define a variable
			#syntax: var <type> <name> <value>
			if len(words) != 4: error("var on line {} must have 3 arguments".format(curent_line))
			if words[2] in variables: error("Variable {} is already defined".format(words[2]))
			test, msg = is_value_valid(words[3], words[1])
			if not test: error(msg)
			else: variables[words[2]] = (words[1], words[3])
		case "set": # set a variable
			#syntax: set <name> <value> [<value>...]
			value = calculate(words[2:], variables[words[1]][0])
			if not words[1] in variables: error("Variable {} is not defined".format(words[1]))
			test, msg = is_value_valid(value, variables[words[1]][0])
			if not test: error(msg)
			else: 
				if variables[words[1]][0] == "42": value = int(float(value))
				variables[words[1]] = (variables[words[1]][0], str(value))
		case "say": # print a value
			#syntax: say <value> <value> ...
			say = ""
			for i in range(1, len(words)): say += str(get_value(words[i], "'"))
			print(say, end="")
		case "in": # ask for input
			#syntax: in <type> <name> [<name>... if type = ']
			if words[1] == "'":
				if len(words) < 3: error("in on line {} must have at least 2 arguments".format(curent_line)) 
			elif len(words) != 3: error("in on line {} must have 2 arguments".format(curent_line))
			for i in range(2, len(words)):
				if words[i] not in variables: error("Variable {} is not defined on line {}".format(words[i], curent_line))
				elif variables[words[i]][0] != words[1]: error("Variable {} is not a {} on line {}".format(words[i], words[1], curent_line))
			inp = input()
			match words[1]:
				case "'":
					length = len(inp)
					if len(words) -2 < length: error("Not enough place to store the input on line {}".format(curent_line))
					for i in range(length):
						test, msg = is_value_valid(str(ord(inp[i])), "'")
						if not test: error(msg)
						else: variables[words[i+2]] = ("'", str(ord(inp[i])))
				case "42"|"3.14"|"?":
					test, msg = is_value_valid(inp, words[1])
					if not test: error(msg)
					else: variables[words[2]] = (words[1], get_value(inp, words[1]))
				case _: error("Unknown type {} on line {}".format(words[1], curent_line))
		case "if": # if statement
			#syntax: if <value:?> <command>
			if get_value(words[1], "?"): run(words[2:])
		case "go": # go to a line
			#syntax: go <value:42>
			if len(words) != 2: error("go on line {} must have 1 argument".format(curent_line))
			test, msg = is_value_valid(words[1], "42")
			if not test: error(msg)
			elif get_value(words[1], "42") <= 1: error("Can't go to line {} from line {}".format(get_value(words[1], "42"), curent_line))
			else: curent_line = get_value(words[1], "42") - 1

# define the functions
def is_value_valid(value: str, type: str) -> tuple[bool,str]:
	"""return True if the value is valid for the given type"""
	value = str(value)
	match type:
		case "'": # character
			try:
				value = chr(int(value))
				return (True, "")
			except: return False, "'{}' on line {} is not an ascii value".format(value, curent_line)
		case "42": # integer
			try: value = int(float(value))
			except: return False, "42 on line {} is not a number".format(curent_line)
			return (True, "")
		case "3.14": # float
			try: value = float(value)
			except: return False, "3.14 on line {} is not a number".format(curent_line)
			return (True, "")
		case "?": # boolean
			if value == "yes" or value == "no": return (True, "")
			else: return False, "{} on line {} is not a ?".format(value, curent_line)
		case _: return False, "Unknown type {} on line".format(type, curent_line)
def get_value(value: str, type: str):
	"""get the real value inside the string value"""
	if value.startswith("$"): return get_variable(value[1:])
	test, msg = is_value_valid(value, type)
	if not test: error(msg)
	else:
		match type:
			case "'":
				#return a character from its ascii value
				return chr(int(value))
			case "42": return int(float(value))
			case "3.14": return float(value)
			case "?": return value == "yes"
def get_variable(name: str):
	"""return the value of the variable with the given name"""
	if name in variables: return get_value(variables[name][1], variables[name][0])
	else: error("Variable {} is not defined".format(name))
def calculate(values: list[str], type: str):
	"""calculate the value of the given values"""
	if len(values) == 1: 
		if type == "?": return "yes" if get_value(values[0], type) else "no"
		return get_value(values[0], type)
	elif (len(values)-1)%2 == 0 and len(values) >= 3:
		index = 1
		calc = [values[0]]
		while index < len(values):
			calc += values[index:index+2]
			index += 2
			try:
				match type:
					case "'": error("Can't calculate anything with type ' on line {}".format(curent_line))
					case "42"|"3.14":
						match calc[1]:
							case "+": calc = [get_value(calc[0], type) + get_value(calc[2], type)]
							case "-": calc = [get_value(calc[0], type) - get_value(calc[2], type)]
							case "*": calc = [get_value(calc[0], type) * get_value(calc[2], type)]
							case "/": calc = [get_value(calc[0], type) / get_value(calc[2], type)]
							case "%": calc = [get_value(calc[0], type) % get_value(calc[2], type)]
							case "^": calc = [get_value(calc[0], type) ** get_value(calc[2], type)]
							case _: error("Unknown operator between {} {} on line {}".format(type, calc[1], curent_line))
					case "?":
						if calc[1] == "&": calc = ["yes" if get_value(calc[0], type) and get_value(calc[2], type) else "no"]
						elif calc[1] == "/": calc = ["yes" if get_value(calc[0], type) or get_value(calc[2], type) else "no"]
						elif calc[1] == "*": calc = ["yes" if get_value(calc[0], type) == get_value(calc[2], type) else "no"]
						else: error("Unknown operator between ? {} on line {}".format(calc[1], curent_line))
					case _: return False, "Unknown type {} on line".format(type, curent_line, curent_word)
			except ZeroDivisionError: error("Can't divide by 0 on line {}".format(curent_line))
			except TypeError: error("Can't calculate {} and {} on line {}".format(calc[0], calc[2], curent_line))
			except:
				if is_running: error()
				else: stop()
		return calc[0]
	else: error("Invalid number of arguments on line {}".format(curent_line))

while is_running and curent_line -1 < len(code):
	curent_line += 1
	curent_word = 0
	line = code[curent_line-2]
	words = line.split(" ")

	print(curent_line)

	run(words)
