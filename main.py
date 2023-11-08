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
- You can't initialise function inside functions
This language is interpreted by the Simplier Interpreter, which is written in Python.
"""

## interpreter settings
warn_error = False # if True, warnings will be treated as errors
debug_mode = False # if True, the interpreter will print information about what it's doing
debug_mode_step = False # if True, the interpreter will wait for the user to press enter before executing the next line
debug_format_multi_line = False # if True, the interpreter will print debug messages on multiple lines
interpreter_debug_mode = False # if True, the interpreter will print even more information about what it's doing, use to debug the interpreter

#import
from os import listdir, path, chdir
from importlib import import_module

# define the variables
function_names = ["var", "set", "say", "in", "if", "go", "fn", "end", "call", "lib", "run"]
is_running = True
variables = {} # name: value (tuple[type, value])		{'a': ("'", "65"), 'b': ("42", "42"), 'c': ("3.14", "3.14"), 'd': ("?", "yes")}
functions = {} # name: code (list[str])
libs = {} # name: import
curent_line = 1
local_path = path.dirname(path.realpath(__file__))

# error and warning functions
def stop():
	"""stop the program"""
	global is_running
	is_running = False
	from sys import exit
	exit()
def error(message: str = f"An unknow error occured on line {curent_line}") -> None:
	"""print the error message in red and exit the program"""
	print("\033[91mError: " + str(message) + "\033[0m")
	stop()
def warn(message: str = "", is_error: bool = warn_error) -> None:
	"""print the warning message in yellow, unless warn_error is True"""
	if message == "": error("An unknow warning occured")
	elif is_error: error(message + " (warn -> error)")
	else: print("\033[93mWarning: " + str(message) + "\033[0m")
def debug(message: str|dict, text: str = "") -> None:
	"""print the debug message in blue, unless debug_mode is False"""
	if debug_mode:
		if text == "": print("\033[94mDebug: " + str(message) + "\033[0m")
		elif interpreter_debug_mode: print("\033[94mDebug: " + str(text) + str(message) + "\033[0m")
		else: 
			show = print_variables(message, text)
			if show != "": print(f"\033[94mDebug: {show}\033[0m")
def iprint(message: str) -> None:
	"""print the message in green, used to debug the interpreter"""
	if interpreter_debug_mode and message != "": print("\033[92m" + repr(message) + "\033[0m")
def tprint(message: str) -> None:
	"""print the message in pink, used to debug the interpreter as a temporary print"""
	print("\033[95m" + repr(message) + "\033[0m")
def print_variables(variables: dict[str, any] | dict[str,list[str]] | dict[str,tuple[str,str]], message: str) -> str:
	"""output the variables in a non string like format"""
	if variables != {}: # if the dictionary is not empty
		out = message
		type = ""
		for var in variables:
			type = variables[var].__class__.__name__
			break
		if type == "tuple":
			type_values = {}
			for var in variables:
				if variables[var][0] in type_values: type_values[variables[var][0]][var] = variables[var][1]
				else: type_values[variables[var][0]] = {var: variables[var][1]}
		if debug_format_multi_line:
			match type:
				case "module":
					# {'time': <module 'simple_lib.time' ( from 'C:\\Users\\nilsh\\Documents\\buro\\codding\\Python\\Simplier\\simple_lib\\time.py')>, 'pomme': <module 'simple_lib.pomme' ( from 'C:\\Users\\nilsh\\Documents\\buro\\codding\\Python\\Simplier\\simple_lib\\pomme.py')>} -> '\n\ttime\ntpomme'
					for i in variables: out += f"\n\t{i}"
				case "list":
					# {'pomme': ["set a 2", "set b $c = $a", "if $b go 5", "say 1", "say 10"]} -> '\n\tpomme:\n\t\tset a 2;\n\t\tset b $c = $a;\n\t\tif $b go 5;\n\t\tsay 1;\n\t\tsay 10;'
					for i in variables:
						out += f"\n\t{i}:"
						for j in variables[i]: out += f"\n\t\t{j};"
				case "tuple":
					# {'a': ("'", "63"), 'c': ("42", "10"), 'd': ("3.14", "3.9"), 'b': ("'", "27"), 'e': ("?", "yes")} -> '\n\ta: 63\n\tb: 27\n42:\n\tc: 10\n3.14:\n\td: 3.9\n?:\n\te: yes'
					for i in type_values:
						out += f"\n\t{i}"
						for j in type_values[i]: out += f"\n\t\t{j}: {type_values[i][j]}"
				case _:iprint("unknown type" + type)
		else:
			match type:
				case "module":
					# {'time': <module 'simple_lib.time' ( from 'C:\\Users\\nilsh\\Documents\\buro\\codding\\Python\\Simplier\\simple_lib\\time.py')>, 'pomme': <module 'simple_lib.pomme' ( from 'C:\\Users\\nilsh\\Documents\\buro\\codding\\Python\\Simplier\\simple_lib\\pomme.py')>} -> [time, pomme]
					out += "["
					for i in variables: out += f"{i}, "
					out = out[:-2] + "]"
				case "list":
					# {'pomme': ["set a 2", "set b $c = $a", "if $b go 5", "say 1", "say 10"]} -> {pomme: [set a 2; set b $c = $a; if $b go 5; say 1; say 10;]}
					out += "{"
					for i in variables:
						out += f"{i}: ["
						for j in variables[i]: out += f"{j}; "
						out = out[:-1] + "], "
					out = out[:-2] + "}"
				case "tuple":
					# {'a': ("'", "63"), 'c': ("42", "10"), 'd': ("3.14", "3.9"), 'b': ("'", "27"), 'e': ("?", "yes")} -> {': [a:63, b: 27], 42: [c: 10], 3.14: [d: 3.9], ?: [e: yes]}
					out += "{"
					for i in type_values:
						out += f"{i}: ["
						for j in type_values[i]: out += f"{j}: {type_values[i][j]}, "
						out = out[:-2] + "], "
					out = out[:-2] + "}"
				case _:iprint("unknown type" + type)
		return out
	return ""

## code
from os import system, name
system("cls" if name == "nt" else "clear")
file_path = input("Enter the file path: ")
if not file_path.endswith((".simple",".simplier")): error("File must be a .simple file")

try: 
	with open(file_path, "r") as file: code = file.read().split("\n")
except FileNotFoundError: error(f"File {file_path} does not exist")

# set the path of execution to the location of the file
# this is to ensure that the file can be run from any location and won't mess up the import
chdir(path.dirname(path.realpath(__file__)))

warn("This language is still in development, so it may not work as expected", False)

# Remove empty lines and comments, return error if line is too long, repeated or empty
if len(code) > 1: code = code[1:]
else:error("File is empty")
for i in range(len(code)):
	if len(code[i]) > 60:
		error(f"Line {i + 2} is so long")
	if not ";" in code[i] or code[i].strip().startswith(";"):
		error(f"Line {i + 2} is empty")
	code[i] = code[i][:code[i].index(";")] # remove comments
	if len(code[i].split(" ")) > 2 and code[i] in code[:i]:
		error(f"Line {i + 2} is repeated")

# main function
def run(words: list[str]) -> None:
	global curent_line
	if words[0] in function_names:
		match words[0]:
			case "var": # define a variable
				#syntax: var <type> <name> <value>
				if len(words) != 4: error(f"var on line {curent_line} must have 3 arguments")
				if words[2] in variables: error(f"Variable {words[2]} is already defined")
				test, msg = is_value_valid(words[3], words[1])
				if not test: error(msg)
				else: variables[words[2]] = (words[1], words[3])
			case "set": # set a variable
				#syntax: set <name> <value> [<operation> <value>...]
				iprint((words[2:], variables[words[1]][0]))
				value = calculate(words[2:], variables[words[1]][0])
				if not words[1] in variables: error(f"Variable {words[1]} is not defined")
				test, msg = is_value_valid(value, variables[words[1]][0])
				if not test: error(msg)
				else:
					if variables[words[1]][0] == "42": value = int(float(value))
					variables[words[1]] = (variables[words[1]][0], str(value))
			case "say": # print a value
				#syntax: say <value> <value> ...
				say = ""
				for i in range(1, len(words)):
					if isinstance(words[i],str) and words[i].startswith("$"):
						temp = get_variable(words[i][1:])[0]
						match variables[words[i][1:]][0]:
							case "'": say += chr(int(temp))
							case "?": say += "yes" if temp=="yes" else "no"
							case _: say += str(temp)
					else: say += chr(int(get_value(words[i], "'")))
				print(say,end="")
			case "in": # ask for input
				#syntax: in <type> <name> [<name>... if type = ']
				if words[1] == "'":
					if len(words) < 3: error(f"in on line {curent_line} must have at least 2 arguments")
				elif len(words) != 3: error(f"in on line {curent_line} must have 2 arguments")
				for i in range(2, len(words)):
					if words[i] not in variables: error(f"Variable {words[i]} is not defined on line {curent_line}")
					elif variables[words[i]][0] != words[1]: error(f"Variable {words[i]} is not a {words[1]} on line {curent_line}")
				inp = input()
				match words[1]:
					case "'":
						length = len(inp)
						if len(words) -2 < length: error(f"Not enough place to store the input on line {curent_line}")
						for i in range(length):
							test, msg = is_value_valid(str(ord(inp[i])), "'")
							if not test: error(msg)
							else: variables[words[i+2]] = ("'", str(ord(inp[i])))
					case "42"|"3.14":
						variables[words[2]] = (words[1], str(get_value(inp, words[1])))
					case "?":
						test, msg = is_value_valid(inp, "?")
						if test:variables[words[2]] = ("?", inp)
						else: error(msg)
					case _: error(f"Unknown type {words[1]} on line {curent_line}")
			case "if": # if statement
				#syntax: if <value:?> <command>
				if get_value(words[1], "?"): run(words[2:])
			case "go": # go to a line
				#syntax: go <value:42>
				if len(words) != 2: error(f"go on line {curent_line} must have 1 argument")
				test, msg = is_value_valid(words[1], "42")
				if not test: error(msg)
				elif get_value(words[1], "42") <= 1: error(f"Can't go to line {get_value(words[1], '42')} from line {curent_line}")
				else: curent_line = get_value(words[1], "42") - 1
			case "fn": # define a function
				#syntax: fn <name>
				if len(words) != 2: error(f"fn on line {curent_line} must have 1 arguments")
				#get the position of the end of the function
				for i in range(curent_line -1, len(code)):
					if code[i]=="end": break
				else: error(f"Function {words[1]} on line {curent_line} is not closed")
				functions[words[1]] = code[curent_line-1:i]
				curent_line = i + 2
			case "end": # end a function, if should never be executed, if it is, it's an error
				error(f"end on line {curent_line} should never be executed")
			case "call": # call a function
				#syntax: call <name>
				if len(words) != 2: error(f"call on line {curent_line} must have 1 arguments")
				if not words[1] in functions: error(f"Function {words[1]} is not defined on line {curent_line}")
				old_line, curent_line = curent_line, 1
				function_name = words[1]
				debug(f"start running function {function_name}")
				while is_running and curent_line -1 < len(functions[function_name]):
					curent_line += 1
					line = functions[function_name][curent_line-2]
					words = line.split(" ")

					debug(f"Fn Line: {curent_line}")

					run(words)

					debug(variables, "Variables: ")
					debug(functions, "Functions: ")
					debug(libs, "Library: ")
					if debug_mode_step: input()
				debug(f"end running function {function_name}")
				curent_line = old_line
			case "lib": # import a library
				#syntax: lib <name>
				if len(words) != 2: error(f"lib on line {curent_line} must have 1 arguments")
				elif words[1] in libs: error(f"Library {words[1]} on line {curent_line} is allready imported")
				elif words[1] + ".py" in listdir(f"simple_lib"):
					libs[words[1]] = import_module(f"simple_lib.{words[1]}")
					libs[words[1]].init(lib_import_var())
				else: error(f"Library {words[1]} does not exist")
			case "run": # run some code but change the variables written in it with their content
				temp = []
				i = 1
				while i < len(words):
					v = get_command(words, i)
					if v[0] != "":temp.append(v[0])
					i = v[1] + 1
				debug(f"Run: {' '.join(temp)};")
				run(temp)
			case _: # if the function is not a default one, may be a library function
				error()
	else:
		# if the function is not a default one, it may be a library function
		for lib in libs:
			if words[0] in libs[lib].function_names:
				libs[lib].call(words, lib_import_var())
				break
		else: error(f"Function {words[0]} is not defined on line {curent_line}")

# define the functions
def is_value_valid(value: str, type: str) -> tuple[bool,str]:
	"""return True if the value is valid for the given type"""
	iprint((value, type))
	value = str(value)
	match type:
		case "'": # character
			try:
				value = chr(int(value))
				return (True, "")
			except: return False, f"{value} on line {curent_line} is not a '"
		case "42": # integer
			try: value = int(float(value))
			except: return False, f"{value} on line {curent_line} is not a 42"
			return (True, "")
		case "3.14": # float
			try: value = float(value)
			except: return False, f"{value} on line {curent_line} is not a 3.14"
			return (True, "")
		case "?": # boolean
			if value in ["yes", "no"]: return (True, "")
			else: return False, f"{value} on line {curent_line} is not a ?"
		case _: return False, f"Unknown type {type} on line {curent_line}"
def get_value(value: str, type: str) -> str | int | float | bool:
	"""get the real value inside the string value"""
	iprint((value, type))
	if isinstance(value,str) and value.startswith("$"):
		v = get_variable(value[1:])
		return get_value(v[0], v[1])
	else:
		test, msg = is_value_valid(value, type)
		if not test: error(msg)
		else:
			match type:
				case "'":
					#return a character from its ascii value
					iprint((value, chr(int(value))))
					return value
				case "42": return int(float(value))
				case "3.14": return float(value)
				case "?": return value == "yes"
def get_variable(name: str) -> tuple[str,str] :
	"""return the value of the variable with the given name"""
	iprint(name)
	if name in variables: return (variables[name][1], variables[name][0])
	else: error(f"Variable {name} is not defined")
def calculate(values: list[str], type: str):
	"""calculate the value of the given values"""
	if len(values) == 1:
		if type == "?": return "yes" if get_value(values[0], type) else "no"
		iprint(values[0])
		return get_value(values[0], type)
	elif (len(values)-1)%2 == 0 and len(values) >= 3:
		index = 1
		calc = [values[0]]
		while index < len(values):
			calc += values[index:index+2]
			index += 2
			try:
				match type:
					case "'": error(f"Can't calculate anything with type ' on line {curent_line}")
					case "42"|"3.14":
						match calc[1]:
							case "+":calc = [get_value(calc[0], type) + get_value(calc[2], type)]
							case "-": calc = [get_value(calc[0], type) - get_value(calc[2], type)]
							case "*": calc = [get_value(calc[0], type) * get_value(calc[2], type)]
							case "/": calc = [get_value(calc[0], type) / get_value(calc[2], type)]
							case "%": calc = [get_value(calc[0], type) % get_value(calc[2], type)]
							case "^": calc = [get_value(calc[0], type) ** get_value(calc[2], type)]
							case ".-": calc = [min(get_value(calc[0], type), get_value(calc[2], type))]
							case ".+": calc = [max(get_value(calc[0], type), get_value(calc[2], type))]
							case _: error(f"Unknown operator between {type} {calc[1]} on line {curent_line}")
					case "?":
						if is_value_valid(calc[0] if not calc[0].startswith("$") else get_variable(calc[0][1:])[0], "?")[0]:
							match calc[1]:
								case "&": calc = ["yes" if get_value(calc[0], type) and get_value(calc[2], type) else "no"]
								case "/": calc = ["yes" if get_value(calc[0], type) or get_value(calc[2], type) else "no"]
								case "*": calc = ["yes" if get_value(calc[0], type) == get_value(calc[2], type) else "no"]
								case _: error(f"Unknown operator between ? {calc[1]} on line {curent_line}")
						elif calc[0].startswith("$") and calc[2].startswith("$"):
							#if there's a varriable, test if the value and type are the same
							match calc[1]:
								case "=": calc = ["yes" if get_variable(calc[0][1:]) == get_variable(calc[2][1:]) else "no"]
								case "!": calc = ["yes" if get_variable(calc[0][1:]) != get_variable(calc[2][1:]) else "no"]
								case ">": calc = ["yes" if get_variable(calc[0][1:]) > get_variable(calc[2][1:]) else "no"]
								case "<": calc = ["yes" if get_variable(calc[0][1:]) < get_variable(calc[2][1:]) else "no"]
								case _: error(f"Unknown operator between {type} {calc[1]} on line {curent_line}")
					case _: return False, f"Unknown type {type} on line {curent_line}"
			except ZeroDivisionError: error(f"Can't divide by 0 on line {curent_line}")
			except TypeError: error(f"Can't calculate {calc[0]} and {calc[2]} on line {curent_line}")
			except:
				if is_running: error()
				else: stop()
		return calc[0]
	elif type == "?" and len(values) == 2 and values[0] == "!":
		return "yes" if not get_value(values[1], "?") else "no"
	else: error(f"Invalid number of arguments on line {curent_line}")
def lib_import_var() -> dict:
	"""return all variables and functions of the interpreter"""
	return {
		# debug
		"debug_mode": debug_mode,
		"debug_mode_step": debug_mode_step,
		"interpreter_debug_mode": interpreter_debug_mode,
		# functions
		"stop": stop,
		"error": error,
		"warn": warn,
		"debug": debug,
		"iprint": iprint,
		"tprint": tprint,
		"run": run,
		"is_value_valid": is_value_valid,
		"get_value": get_value,
		"get_variable": get_variable,
		"calculate": calculate,
		"get_command": get_command,
		# variables
		"variables": variables,
		"functions": functions,
		"curent_line": curent_line,
		"libs": libs,
	}
def get_command(commands: list[str], pos: int) -> None:
	"""get the command and return it"""
	if commands[pos].startswith("$"):
		v = get_variable(commands[pos][1:])
		out = (str(get_value(v[0], v[1])))
		match v[1]:
			case "'": out = chr(int(out))
			case "?": out = "yes" if bool(out) else "no"
		if pos < (len(commands) - 1): 
			v = get_command(commands, pos+1)
			pos = v[1]
			out += v[0]
	else: out = commands[pos]
	return (out, pos)

# run the code
try:
	while is_running and curent_line -1 < len(code):
		curent_line += 1
		line = code[curent_line-2]
		words = line.split(" ")

		debug(f"Line: {curent_line}")

		run(words)

		debug(variables, "Variables: ")
		debug(functions, "Functions: ")
		debug(libs, "Library: ")
		if debug_mode_step: input()
except KeyboardInterrupt: error("KeyboardInterrupt")
