"""
this is a template for a library file
"""

# please keep this variable format: {str(name): (str(type), str(value))}
# for example: {'a': ("'", "65"), 'b': ("42", "42"), 'c': ("3.14", "3.14"), 'd': ("?", "yes")}

function_names = []

def init(main: dict) -> None:
	"""
	this function is called when the library is loaded
	main: dict with all the functions from the interpreter
	"""
	main["debug"]("loading library template")
def call(words: list[str],main: dict[str,function]) -> None:
	"""
	words: list of words in the line
	"""
	match words[0]:
		case "":
			pass