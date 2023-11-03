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

def error(message: str = "An unknow error occured") -> None:
	"""print the error message in red and exit the program"""
	print("\033[91mError: " + message + "\033[0m")
	exit()
def warn(message: str = "", is_error: bool = warn_error) -> None:
	"""print the warning message in yellow, unless warn_error is True"""
	if message == "": error("An unknow warning occured")
	elif is_error: error(message + " (warn -> error)")
	else: print("\033[93mWarning: " + message + "\033[0m")

warn("This language is still in development, so it may not work as expected", False)

# Remove empty lines and comments, return error if line is too long, repeated or empty
if len(code) > 1:code = code[1:]
else: error("File is empty")
for i in range(len(code)):
	if len(code[i]) > 60:
		error("Line {} is so long".format(i + 1))
	if not ";" in code[i] or code[i].strip().startswith(";"):
		error("Line {} is empty".format(i + 1))
	code[i] = code[i][:code[i].index(";")] # remove comments
	if len(code[i].split(" ")) > 1 and code[i] in code[:i]:
		error("Line {} is repeated".format(i + 1))

# define the variables
is_running = True
variables = {} # name: value (tuple[type, value])
functions = {} # name: code (list[str])
curent_line = -1

while is_running and curent_line + 1 < len(code):
	curent_line += 1
	curent_word = 0
	line = code[curent_line]
