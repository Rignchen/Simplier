"""
Simplier is an esoteric programming language based on the concept of simplicity.
Some of the features of this language include:
- Small instruction names
- First line is never executed and can be as long as you want
- No repetition of lines (lines with more than one instruction can't be repeated)
- Maximum of 60 characters per line
- Lines must end with ; and everything after it is ignored but still counted for the 60 character limit
- No complex data types
- Numbers in variables are between 0 and 255, Floats are between -128 and 127
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
		error("Line {} is so long".format(i + 1))
	if not ";" in code[i] or code[i].strip().startswith(";"):
		error("Line {} is empty".format(i + 1))
	code[i] = code[i][:code[i].index(";")] # remove comments
	if len(code[i].split(" ")) > 1 and code[i] in code[:i]:
		error("Line {} is repeated".format(i + 1))

# define the functions
def is_value_valid(value: str, type: str) -> tuple[bool,str]:
	"""return True if the value is valid for the given type"""
	value = str(value)
	match type:
		case "'": # character
			if len(value) > 1: return False, "' on line {} is too long".format(curent_line)
			return (True, "")
		case "42": # integer
			try: value = int(float(value))
			except: return False, "42 on line {} is not a number".format(curent_line)
			if not 0 <= value <= 255: return False, "42 on line {} is not in range 0-255".format(curent_line)
			return (True, "")
		case "3.14": # float
			try: value = float(value)
			except: return False, "3.14 on line {} is not a number".format(curent_line)
			if not -128 <= value <= 127: return False, "3.14 on line {} is not in range -128 - 127".format(curent_line)
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
			case "'": return str(value)
			case "42": return int(value)
			case "3.14": return float(value)
			case "?": return value == "yes"
def get_variable(name: str):
	"""return the value of the variable with the given name"""
	if name in variables: return get_value(variables[name][1], variables[name][0])
	else: error("Variable {} is not defined".format(name))
def calculate(values: list[str], type: str):
	"""calculate the value of the given values"""
	if len(values) == 1: return get_value(values[0], type)
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
						if calc[1] == "&": calc = [get_value(calc[0], type) and get_value(calc[2], type)]
						elif calc[1] == "/": calc = [get_value(calc[0], type) or get_value(calc[2], type)]
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

	match words[0]:
		case "var": # define a variable
			#syntax: var <type> <name> <value>
			if len(words) != 4: error("var on line {} must have 3 arguments".format(curent_line))
			if words[2] in variables: error("Variable {} is already defined".format(words[2]))
			test, msg = is_value_valid(words[3], words[1])
			if not test: error(msg)
			else: variables[words[2]] = (words[1], words[3])
		case "set": # set a variable
			#syntax: set <name> <value>
			value = calculate(words[2:], variables[words[1]][0])
			if not words[1] in variables: error("Variable {} is not defined".format(words[1]))
			test, msg = is_value_valid(value, variables[words[1]][0])
			if not test: error(msg)
			else: 
				if variables[words[1]][0] == "42": value = int(float(value))
				variables[words[1]] = (variables[words[1]][0], str(value))
