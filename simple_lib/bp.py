"""
time library for the simplier esoteric language
"""

def init(main: dict) -> None: main["libs"]["bp"] = _main(main)

class _main:
	function_names = ["cvrt","add","del"]
	def __init__(self, main) -> None:
		#prints
		self.debug = main["debug"]
		self.error = main["error"]
		self.warn = main["warn"]
		self.tprint = main["tprint"]
		self.iprint = main["iprint"]

		# start loading the library
		self.debug("loading bypass library")

		#functions
		self.is_value_valid = main["is_value_valid"]
		self.get_variable = main["get_variable"]
		self.get_value = main["get_value"]
		#variables aren't set here because they can change until the program is run

		# finish loading the library
		self.debug("bypass library loaded successfully")
	def call(self,words: list[str],main: dict) -> None:
		#variables
		self.curent_line = main["curent_line"]
		self.variables = main["variables"]
		self.is_function_running = main["is_function_running"]
		self.code = main["code"]

		#look for the function
		match words[0]:
			case "cvrt": # convert a variable to any other value type
				# syntaxe: cvrt <varriable> <variable>
				if len(words) != 3: self.error(f"cvrt on line {self.curent_line} takes 2 arguments not {len(words)}")
				v1 = self.get_variable(words[1])
				v2 = self.get_variable(words[2])
				if v1[1] == v2[1]: self.error(f"cannot convert {v1[1]} to {v2[1]} on line {self.curent_line}")
				match v1[1]:
					case "'":
						match v2[1]:
							case "42": self.variables[words[2]] = ('42', v1[0])
							case "3.14": self.variables[words[2]] = ('3.14', str(float(v1[0])))
							case "?":
								match v1[0]:
									case "121": self.variables[words[2]] = ('?', "yes")
									case "110": self.variables[words[2]] = ('?', "no")
									case _: self.error(f"' {v1[0]} cannot be converted to ? on line {self.curent_line}")
					case "42": 
						match v2[1]:
							case "'": 
								self.warn(f"convertion on line {self.curent_line} can and should be done using the run command")
								self.variables[words[2]] = ("'", v1[0])
							case "3.14": 
								self.warn(f"convertion on line {self.curent_line} can and should be done using the set command")
								self.variables[words[2]] = ('3.14', str(float(v1[0])))
							case "?": self.error(f"cannot convert {v1[1]} to {v2[1]} on line {self.curent_line}")
					case "3.14":
						match v2[1]:
							case "'": self.variables[words[2]] = ("'", str(int(v1[0].split(".")[0])))
							case "42":
								self.warn(f"convertion on line {self.curent_line} can and should be done using the set command")
								self.variables[words[2]] = ('42', int(float(v1[0])))
							case "?": self.error(f"cannot convert {v1[1]} to {v2[1]} on line {self.curent_line}")
					case "?": 
						if v2[1] == "'": self.variables[words[2]] = ("'", str(ord(v1[0][0])))
						else: self.error(f"cannot convert {v1[1]} to {v2[1]} on line {self.curent_line}")
			case "add": # add some code to the end of the 
				# syntaxe: cvrt <varriable> <variable>
				if self.is_function_running: self.error("add command cannot be used inside a function")
				if len(words) < 2: self.error(f"add on line {self.curent_line} takes at least 1 argument")
				self.code[self.curent_line-3] += " " + " ".join(words[1:])
				self.iprint(self.code[self.curent_line-3])
			case "del": # delete a variable
				# syntaxe: del <varriable>
				if len(words) != 2: self.error(f"del on line {self.curent_line} takes 1 argument not {len(words)}")
				if words[1] not in self.variables: self.error(f"variable {words[1]} does not exist on line {self.curent_line}")
				del self.variables[words[1]]
