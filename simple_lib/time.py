"""
time library for the simplier esoteric language
"""
import time

function_names = ["now"]

def call(words: list[str],main: dict) -> None:
	match words[0]:
		case "now": # get current time
			# syntaxe: now <varriable:3.14>
			if len(words) > 2: main["error"]("now on line {} must have 1 arguments".format(main["curent_line"]))
			test, msg = main["is_value_valid"](main["get_variable"](words[1]), "3.14")
			if not test: main["error"](msg)
			main["variables"][words[1]] = main["variables"][words[1]] = ("3.14", main["get_value"](str(time.time()), "3.14"))
