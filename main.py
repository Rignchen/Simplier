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
