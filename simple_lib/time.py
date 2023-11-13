"""
time library for the simplier esoteric language
"""
import time

def init(main: dict) -> None: main["libs"]["time"] = _main(main)

class _main:
	function_names = ["now", "zzz"]
	def __init__(self, main) -> None:
		#prints
		self.debug = main["debug"]
		self.error = main["error"]
		self.tprint = main["tprint"]

		# start loading the library
		self.debug("loading time library")

		#functions
		self.is_value_valid = main["is_value_valid"]
		self.get_variable = main["get_variable"]
		self.get_value = main["get_value"]
		#variables aren't set here because they can change until the program is run

		# finish loading the library
		self.debug("time library loaded successfully")
	def call(self,words: list[str],main: dict) -> None:
		#variables
		self.curent_line = main["curent_line"]
		self.variables = main["variables"]

		#look for the function
		match words[0]:
			case "now": # get the current unix time
				# syntaxe: now <varriable:42|3.14>
				if len(words) != 2: self.error(f"now on line {self.curent_line} must have 1 arguments")
				var = self.get_variable(words[1])
				if var[1] == "3.14": self.variables[words[1]] = self.variables[words[1]] = ("3.14", self.get_value(str(time.time()), "3.14"))
				elif var[1] == "42": self.variables[words[1]] = self.variables[words[1]] = ("42", self.get_value(str(int(time.time())), "42"))
				else: self.error(f"{var[0]} on line {self.curent_line} must be a number")
			case "zzz": # wait for x seconds
				# syntaxe: zzz <varriable:42|3.14>
				if len(words) != 2: self.error(f"zzz on line {self.curent_line} must have 1 arguments")
				if words[1].startswith("$"): v = self.get_variable(words[1][1:])
				else: v = [words[1], "3.14"]
				test, msg = self.is_value_valid(v[0], v[1])
				if not test: self.error(msg)
				time.sleep(float(self.get_value(words[1], "3.14")))
