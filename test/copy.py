with open("main.py") as f: text = f.read().split("\n")
a = 'system("cls" if name == "nt" else "clear")'
b = 'file_path = input("Enter the file path: ")'
text.remove(a)
text.remove(b)

files = [ # set -> in -> calcul -> bool -> if -> go -> function -> lib -> run
	"set.simple",
	"in.simple",
	"calcul.simple",
	"bool.simple",
	"if.simple",
	"go.simple",
	"function.simple",
	"lib.simple",
	"run.simple",
]

out = '#import\nfrom os import chdir, path, remove, name, system\n\nsystem("cls" if name == "nt" else "clear")\n\n# if in main folder, move to test folder\nchdir(path.dirname(path.realpath(__file__)))\n\n# test files\nfile_list = ['
for i in files: out += f'\n\t"{i}",'
out += '\n]\n\n# interpreter\nfor file_path in file_list:\n\tprint(f"now testing {file_path}")'

for line in text: out += f"\n\t{line}"
out += "\nremove(path.realpath(__file__))"

with open("test/test_all.py","w+") as f: f.write(out)
