"""
time library for the simplier esoteric language
"""
function_names = ["test"]
print("test lib loaded")

def call(words: list[str],main: dict) -> None:
	match words[0]:
		case "test":
			print("test")
			main["tptint"]("test tprint")
			main["tptint"](main["variables"])
			main["variables"]["test"] = ("'","1")
			main["tptint"](main["variables"])
			main["warn"]("test warn")
