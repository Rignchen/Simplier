"""
time library for the simplier esoteric language
"""
import time

function_names = ["now", "zzz"]

def init(main: dict[str,function]) -> None:
	main["debug"]("loading time library")
def call(words: list[str],main: dict) -> None:
	match words[0]:
		case "now": # get current time
			# syntaxe: now <varriable:3.14>
			if len(words) > 2: main["error"]("now on line {} must have 1 arguments".format(main["curent_line"]))
			test, msg = main["is_value_valid"](main["get_variable"](words[1]), "3.14")
			if not test: main["error"](msg)
			main["variables"][words[1]] = main["variables"][words[1]] = ("3.14", main["get_value"](str(time.time()), "3.14"))
		case "zzz": # wait for x seconds
			# syntaxe: zzz <varriable:42|3.14>
			if len(words) > 2: main["error"]("zzz on line {} must have 1 arguments".format(main["curent_line"]))
			test, msg = main["is_value_valid"](words[1], "3.14")
			if not test: main["error"](msg)
			time.sleep(float(main["get_value"](words[1], "3.14")))
