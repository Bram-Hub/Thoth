from Tkinter import *
import parcer
import Tkconstants, tkFileDialog, os

class Sentence(Frame):
	def __init__(self, master, sen, just, Lcount, proof, Llist, cList):
		Frame.__init__(self, master)
		
		global curr
		curr = self
		
		self.Lcount = Lcount + 1
		#self.Llist = Llist
		self.just = just
		
		self.proof = proof
		
		self.IDlable = Label(master, text = Lcount)
		#self.IDlable.pack(side = LEFT)
		self.IDlable.grid(row=0, column=0, sticky=W)
		
		self.cList = cList
		
		self.selected = IntVar()
		self.select = Checkbutton(master, variable=self.selected)
		self.cList.append(self.selected)
		self.select.grid(row=0, column=1, sticky=W)
		
		self.sentence = Label(master, text = sen)
		#self.sentence.pack(side = LEFT)
		self.sentence.grid(row=0, column=2, sticky=W)
		
		self.justLable = Label(master, text = just, fg = 'grey')
		#self.justLable.pack(side = LEFT)
		self.justLable.grid(row=0, column=3, sticky=W)
		
		self.rule = StringVar(master)
		self.rule.set("modus ponens")
		
		#self.rules = OptionMenu(master, self.rule, "modus ponens", "P>(Q>P)")
		
		if tar == None:
			self.rules = apply(OptionMenu, (master, self.rule) + tuple(ruleL))
			#self.rules.pack(side = RIGHT)
		else:
			self.rules = apply(OptionMenu, (master, self.rule) + tuple(["modus ponens", "end"]))
		
		self.rules.grid(row=0, column=6, sticky=E)
		
		self.step_button = Button(master, text="Add Step", command= self.checkRule)
		#self.step_button.pack(side = RIGHT)
		self.step_button.grid(row=0, column=5, sticky=E)
		
		self.sentenceData = parcer.shuck(sen)
		#print self.sentenceData
		
		self.justData = just
		
		self.antecedentData, self.consequentData = parcer.senParce(sen)
		
		self.type = "sentence"
		
		self.Llist = Llist
		
		if just != "premise":
			#self.Llist.append(self)
			self.Llist.append(self)
		#print self.Lcount
		
		#self.ax_button = Button(master, text="Axiom", command= lambda: self.nextMP(self.master))
		#self.ax_button.pack(side = RIGHT)
		#make this a drop down
		
		
	def lock(self):
		self.rules.destroy()
		self.step_button.destroy()
		#print self.sentenceData
		#self.Llist.append(self)
	
	def lockDist(self):
		#print "test"
		#self.Lcount += 1
		#self.Llist.append(self)
		if self.type == "premise":
			self.lockP(self.master)
		else:
			self.lock()
		
	def nextStep(self):
		self.lockDist()
		r = self.rule.get()
		arg = startAX(r)
		axNum = ruleL.index(r)
		#print axNum
		addInfrence(arg, 'axiom '+str(axNum), self.master.master, self.Lcount)
	
	def checkRule(self):
		if self.type == "premise":
			self.sentenceData = self.sentence.get()
			self.antecedentData, self.consequentData = parcer.senParce(self.sentenceData)
			#self.Llist.append(self)
			self.Llist.append(self)
			#print len(self.Llist)
			#print "test"
		if self.rule.get()=="modus ponens" or self.rule.get() == "deduction" or self.rule.get() == "undo" or self.rule.get()=="Q.E.D.":
			#print self.Lcount
			i = 0;
			argL = []
			while i < self.Lcount-1:					
				#self.cList[i].set(1)
				if self.cList[i].get() != 0: 
					#print i
					argL.append(i)
					#checkL[i].set(0)
					self.cList[i].set(0)
				i += 1
			if self.rule.get()=="modus ponens" and len(argL) == 2:
				#self.Llist.append(self)
				s = mpInfrence(argL[0],argL[1], self.Llist)
				#print s
				if s != None:
					self.lockDist()
					j = "M.P. " + str(argL[0]+1)+','+str(argL[1]+1)
					addInfrence(s, j, self.master.master, self.Lcount)
				else:
					if self.type == "premise":
						#self.Llist.pop()
						self.Llist.pop()
			elif self.rule.get()=="deduction" and len(argL) == 0:
				s = startD()
				if s != "":
					self.lockDist()
					j = "deduction"
					addDeduction(s, j, self.master.master, self.Lcount)
				else:
					if self.type == "premise":
						self.Llist.pop()
				#parcer.deductionS(self.Llist, argL[0])
				#parcer.getSource(GlList[argL[0]].justData)
			elif self.rule.get()=="undo" and len(argL) == 1:
				i = 0
				while i <= argL[0]:
					#print self.Llist[i].sentenceData
					i += 1
			elif self.rule.get()=="Q.E.D." and self.type != "premise":
				self.rules.destroy()
				self.step_button.destroy()
			else:
				if self.type == "premise":
					self.Llist.pop()
		elif self.rule.get() == "end":
			parcer.deductionS(self.Llist, tar-1)
			#print tar
		else:
			self.nextStep()

class Premise(Sentence):
	def __init__(self, master, Lcount, proof, Llist, cList):
		Sentence.__init__(self, master, "", "premise", Lcount, proof, Llist, cList)
		#master.title("A simple GUI")

		self.sentence = Entry(master)
		#self.sentence.pack(side = LEFT)
		self.sentence.grid(row=0, column=2, sticky=W)
		
		self.premise_button = Button(master, text="Add Premise", command= lambda: self.nextPremise(self.master))
		#self.premise_button.pack(side = LEFT)
		self.premise_button.grid(row=0, column=4, sticky=E)
		
		self.type = "premise"
		
		#self.test_button = Button(master, text="Test", command= lambda: master.test2(id))
		#self.test_button.pack(side = RIGHT)

		#self.close_button = Button(master, text="Close", command=master.quit)
		#self.close_button.pack()

	def nextPremise(self, master):
		#self.Llist.append(self)
		self.Llist.append(self)
		self.lockDist()
		addPremise(master.master, self.Lcount)
		
	def lockP(self, master):
		self.rules.destroy()
		self.premise_button.destroy()
		self.step_button.destroy()
		#self.ax_button.destroy()
		s = self.sentence.get().lower()
		self.sentence.destroy()
		self.sentence = Label(master, text = s)
		#self.sentence.pack(side = LEFT)
		self.sentence.grid(row=0, column=2)
		
		self.sentenceData = parcer.shuck(s)
		self.antecedentData, self.consequentData = parcer.senParce(s)
		#self.Llist.append(self)
		
	def nextStepP(self):
		self.lockDist(self.master)
		self.nextStep()
		#self.step_button.destroy()
		#args = startMP()
		#mpInfrence(args[0],args[1])
		
class Preset(Sentence):
	def __init__(self, master, sen, just, Lcount, proof, Llist, cList):
		Sentence.__init__(self, master, sen, just, Lcount, proof, Llist, cList)
		#master.title("A simple GUI")
		
		if just == "premise":
			#self.Llist.append(self)
			self.Llist.append(self)

		self.rules.destroy()
		self.step_button.destroy()

def startAX(ax):
	quest = Toplevel()
	quest.title("enter values for axiom")
	
	variables = []
	values = []
	
	axShell = Label(quest, text = ax)
	axShell.grid(row = 0)
	
	i = 1
	for c in ax:
		if c.isalpha() and c not in variables:
			line = Frame(quest)
			lineL = Label(line, text = c)
			lineL.grid(row = 0, column = 0)
			
			lineVal = StringVar()
			lineE = Entry(line, textvariable = lineVal)
			lineE.grid(row = 0, column = 1)
			line.grid(row = i)
			
			i += 1
			variables.append(c)
			values.append(lineVal)
			
	go_button = Button(quest, text="Submit", command = quest.destroy)
	go_button.grid(row = i)
	
	quest.wait_window()
	
	axD = {}
	i = 0
	while i < len(variables):
		if len(values[i].get()) == 0:
			return startAX(ax)
		axD[variables[i]] = values[i].get().lower()
		i += 1
	
	return parcer.snowClone(ax, axD)
	
def startD():
	quest = Toplevel()
	quest.title("enter value for assumption")
	
	line = Frame(quest)
	lineVal = StringVar()
	lineE = Entry(line, textvariable = lineVal)
	lineE.grid(row = 0, column = 0)
	line.grid(row = 0)
			
	go_button = Button(quest, text="Submit", command = quest.destroy)
	go_button.grid(row = 1)
	
	quest.wait_window()
	
	return lineVal.get().lower()
	
def addPremise(proof, Lcount):
		#print index
		#Llist.append(Premise(root))
		#Llist[index].pack(side = BOTTOM, fill = X, expand = 1)
		#line = Frame(thoth.root)
		#line.grid(row=index)
		#thoth.Llist.append(Premise(line))
		#thoth.Llist[index].grid(row=0)
	Llist, cList = getCurrData()
	box = Frame(proof)
	line = Premise(box, Lcount, proof, Llist, cList)
	line.grid(row = 0)
	#print Lcount
	box.grid(row = Lcount-1, column = 0)
	#display(box, Llist, line)
		
def addInfrence(sen, just, proof, Lcount):
	#Llist.append(Sentence(root, sen, just))
	#Llist[index].pack(side = BOTTOM, fill = X, expand = 1)
	#line = Frame(thoth.root)
	#line.grid(row=index)
	#thoth.Llist.append(Sentence(line, sen, just))
	#Llist[index].pack()
	#print index
	#print len(thoth.Llist)
	#thoth.Llist[index].grid(row=0)
	#print "test2"
	
	#line = Sentence(proof, sen, just, Lcount, Llist)
	#line.grid(row=Lcount)
	
	Llist, cList = getCurrData()
	box = Frame(proof)
	line = Sentence(box, sen, just, Lcount, proof, Llist, cList)
	line.grid(row = 0, column = 0)
	#print Lcount
	box.grid(row = Lcount-1, column = 0)
	
def addPreset(sen, just, proof, Lcount):
	Llist, cList = getCurrData()
	box = Frame(proof)
	line = Preset(box, sen, just, Lcount, proof, Llist, cList)
	line.grid(row = 0, column = 0)
	#print len(cList)
	box.grid(row = Lcount-1, column = 0)
	
def addDeduction(sen, just, proof, Lcount):
	global tar
	tar = Lcount
	addInfrence(sen, just, proof, Lcount)
		
def mpInfrence(a, b, Llist):
	#print a
	#print b
	alpha = Llist[a]
	betta = Llist[b]
	return parcer.modusPonens(alpha, betta)
		#print s
	#else print error
	
def clear():
	global curr
	curr = None
	
def getCurrData():
	if curr == None:
		return [], []
	else:
		return curr.Llist, curr.cList
#	global GlList
#	global checkL
#	GlList = []
#	checkL = []
	
#def getProof():
#	if len(GlList) != 0:
#		return GlList[len(GlList)-1].proof
#	else:
#		return None
	
#file = tkFileDialog.askopenfilename(initialdir = os.path.dirname(os.path.realpath(__file__)+"\config"),title = "Select file")
config = open("config.txt", 'r')
global ruleL
ruleL = []
rule = 'modus ponens'
while rule != "":
	ruleL.append(rule)
	rule = config.readline().strip("\n\r")
	#print rule
ruleL.append("Q.E.D.")
config.close

global curr
global tar
tar = None

#global checkL
#checkL = []

#GlList =[]