"""
files library for the simplier esoteric language
"""

def init(main: dict) -> None: main["libs"]["files"] = _main(main)

from genericpath import exists, isdir
from os import path, remove, rmdir, walk

class _main:
	function_names = ["look", "pen", "free", "len", "del"]
	def __init__(self, main) -> None:
		#prints
		self.debug = main["debug"]
		self.error = main["error"]
		self.tprint = main["tprint"]

		# start loading the library
		self.debug("loading files library")

		#functions
		self.is_value_valid = main["is_value_valid"]
		self.get_variable = main["get_variable"]
		self.get_value = main["get_value"]
		
		#variables
		self.file_path: str = main["file_location"].replace("\\","/")

		# finish loading the library
		self.debug("files library loaded successfully")
	def call(self,words: list[str],main: dict) -> None:
		#variables
		self.curent_line: int = main["curent_line"]
		self.variables: dict[str,tuple[str,str]] = main["variables"]

		#look for the function
		match words[0]:
			case "look": # read a character at a position in a file
				# syntax: look <variable:'> <variable:42> <path> <path> <path>...
				if len(words) < 4: self.error(f"look on line {self.curent_line} needs at least 3 arguments")
				if self.get_variable(words[1])[1] != "'": self.error(f"{self.get_variable(words[1])[0]} on line {self.curent_line} is not a '")
				if words[2].startswith("$"): v = self.get_variable(words[2][1:])
				else: v = words[2]
				test, msg = self.is_value_valid(v[0], "42")
				if not test: self.error(msg)
				file_name = self.get_name(words[3:])
				try:
					with open(file_name,"r",encoding="utf-8") as file:
						self.variables[words[1]] = ("'",str(ord(file.read()[int(v[0])]))) # set the variable to the character
				except FileNotFoundError:
					self.error(f"file {file_name} not found")
			case "pen": # write a character at the end of a file
				# syntax: pen <variable> <path> <path> <path>...
				if len(words) < 4: self.error(f"pen on line {self.curent_line} needs at least 3 arguments")
				if words[1].startswith("$"):
					v = self.get_variable(words[1][1:])
					match v[1]:
						case "'": text = chr(int(v[0]))
						case _: text = v[0]
				elif self.is_value_valid(words[1], "'")[0]: text = chr(int(words[1]))
				else: self.error(f"{words[1]} on line {self.curent_line} is not a '")
				file_name = self.get_name(words[2:])
				try: 
					with open(file_name,"a",encoding="utf-8") as file: file.write(text)
				except FileNotFoundError:
					self.error(f"file {file_name} not found")
			case "free": # vide entièrement un fichier/crée le fichier si inexistant
				# syntax: free <path> <path> <path>...
				if len(words) < 3: self.error(f"free on line {self.curent_line} needs at least 2 arguments")
				file_name = self.get_name(words[1:])
				open(file_name,"w+",encoding="utf-8").close()
			case "len": # get the length of a file
				# syntax: len <variable:42> <path> <path> <path>...
				if len(words) < 3: self.error(f"len on line {self.curent_line} needs at least 2 arguments")
				if self.get_variable(words[1])[1] != "42": self.error(f"{self.get_variable(words[1])[0]} on line {self.curent_line} is not a 42")
				file_name = self.get_name(words[2:])
				try:
					with open(file_name,"r",encoding="utf-8") as file:
						a = ("42",str(len(file.read())))
						self.variables[words[1]] = a # set the variable to the length of the file
				except FileNotFoundError:
					self.error(f"file {file_name} not found")
			case "del": # delete a file or a folder
				# syntax: del <path> <path> <path>...
				if len(words) < 2: self.error(f"del on line {self.curent_line} needs at least 1 argument")
				file_name = self.get_name(words[1:])
				if file_name.endswith(("/", "\\")):
					if not exists(file_name): self.error(f"Directory {file_name} not found")
					if not isdir(file_name): self.error(f"{file_name} is not a directory")
					for root, _, files in walk(file_name):
						for name in files: 
							try: remove(path.join(root, name))
							except PermissionError: self.error(f"Permission denied for {path.join(root, name)}")
					for root, dirs, _ in walk(file_name):
						for name in dirs: rmdir(path.join(root, name))
					rmdir(file_name)
				else:
					try: remove(file_name)
					except FileNotFoundError:
						self.error(f"File {file_name} not found")
					except IsADirectoryError:
						self.error(f"{file_name} is a folder")
					except PermissionError:
						self.error(f"Permission denied for {file_name}")
		pass
	def get_name(self, chr_list: list[str]) -> str:
		out = "".join([chr(int(self.get_value(word,"'"))) for word in chr_list])
		if not out.startswith(("/","\\")): out = self.file_path + "/" + out
		return out
