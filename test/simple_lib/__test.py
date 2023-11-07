"""
time library for the simplier esoteric language
"""
function_names = ["test"]

def init(main: dict) -> None:
	print("test lib loaded")
def call(words: list[str],main: dict) -> None:
	match words[0]:
		case "test":
			print("test")
			main["tprint"]("test tprint")
			main["tprint"](main["variables"])
			main["variables"]["test"] = ("'","1")
			main["tprint"](main["variables"])
			main["warn"]("test warn")
