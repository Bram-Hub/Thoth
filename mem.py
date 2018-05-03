from Tkinter import *
import sen
import sys, subprocess, Tkconstants, tkFileDialog, os

def saveS():
	save(tkFileDialog.asksaveasfilename(initialdir = os.path.dirname(os.path.realpath(__file__)),title = "Select file"))
	
def loadS():
	file = tkFileDialog.askopenfilename(initialdir = os.path.dirname(os.path.realpath(__file__)),title = "Select file")
	subprocess.call(['python', 'thoth.py', file])
	sys.exit(0)
	#os.execlp("thoth.py", "test.txt")
	#load("test.txt")

def save(file):
	Llist = sen.getCurrData()[0]
	s = open(file,"w")
	for l in Llist:
		s.write(l.sentenceData+"\n")
		s.write(l.justData+"\n")
	s.close
	
def load(file):
	l = open(file,"r")
	lineData = l.readlines()
	l.close
	
	sen.clear()
	
	root = Tk()
	root.title(file)

	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="Save", command=saveS)
	filemenu.add_command(label="Load", command=loadS)
	#filemenu.add_command(label="Erase", command=erase)
	menubar.add_cascade(label="File", menu=filemenu)

	root.config(menu=menubar)

	proof = Frame(root)
	proof.grid(row=0)
	
	i = 0
	j = 1
	while i < len(lineData)-2:
		sentence = lineData[i].strip("\n\r")
		#print sentence
		just = lineData[i+1].strip("\n\r")
		#print just
		sen.addPreset(sentence, just, proof, j) 
		#sen.addInfrence(sentence, just, proof, j) 
		#addInfrence(sentence, just)
		i+=2
		j+=1
	sentence = lineData[i].strip("\n\r")
	just = lineData[i+1].strip("\n\r")
	#Llist = sen.GlList
	#Llist[0].grid(row=0)
	
	sen.addInfrence(sentence, just, proof, j)

	root.mainloop()

def start():
	root = Tk()
	root.title("untitled")
	
	sen.clear()

	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="Save", command=saveS)
	filemenu.add_command(label="Load", command=loadS)
	#filemenu.add_command(label="Erase", command=erase)
	menubar.add_cascade(label="File", menu=filemenu)

	root.config(menu=menubar)

	#Lcount = 1
	proof = Frame(root)
	proof.grid(row=0)
	sen.addPremise(proof,1)
	#Llist[0].grid(row=0)

	root.mainloop()