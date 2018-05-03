import mem
import sys, subprocess, Tkconstants, tkFileDialog, os

def shuck(s):
	if len(s) == 0 or s[0] != "(" or s[len(s)-1] != ")":
		return s
	p = 0
	for c in s[0:len(s)-1]:
		if c == "(":
			p += 1
		if c == ")":
			p -= 1
		if p == 0:
			return s
		
	if p == 1:
		return s[1:len(s)-1]
	return s
	
def senParce(s):
	s = shuck(s)
	i = 0
	o = True;
	for c in s:
		if o:
			if c == ">":
				return shuck(s[0:i]),shuck(s[i+1:len(s)])
			if c == "(":
				o = False
		if c == ")":
			o = True
		i += 1
	return "",""
		
def modusPonens(a,b):
	print "A"
	print a.sentenceData
	print a.antecedentData
	print a.consequentData
	print "B"
	print b.sentenceData
	print b.antecedentData
	print b.consequentData
	if a.sentenceData == b.antecedentData:
		return b.consequentData
	if b.sentenceData == a.antecedentData:
		return a.consequentData
	return None
	
def snowClone(sent, dic):
	for key in dic:
		#print key
		#print dic[key]
		sent = sent.replace(key, dic[key])
	#print sen
	return sent

def getSource(sent):
	a = ""
	b = ""
	tar = "none"
	#print sent
	for c in sent:
		if c.isdigit() and tar == "none":
			a += c
			tar = "a"
		elif c.isdigit() and tar == "a":
			a += c
		elif not c.isdigit() and tar == "a":
			tar = "b"
		elif c.isdigit() and tar == "b":
			b += c
		elif not c.isdigit() and tar == "b":
			tar = "done"
	return int(a), int(b)
	
def PisP(sent, tar):
	scrachPad = []
	scrachPad.append(snowClone("P>(Q>P)",{"P":sent, "Q":"("+sent+">"+sent+")"}))
	scrachPad.append("axiom 1")
	scrachPad.append(snowClone("(P>(Q>G))>((P>Q)>(P>G))",{"P":sent, "Q":"("+sent+">"+sent+")", "G":sent}))
	scrachPad.append("axiom 2")
	scrachPad.append(snowClone("(P>Q)>Q",{"P":sent, "Q":"("+sent+">"+sent+")"}))
	scrachPad.append("M.P. "+str(tar)+","+str(tar+1))
	scrachPad.append(snowClone("P>(Q>P)",{"P":sent, "Q":sent}))
	scrachPad.append("axiom 1")
	scrachPad.append(snowClone("P>P",{"P":sent}))
	scrachPad.append("M.P. "+str(tar+2)+","+str(tar+3))
	return scrachPad
	
def QisPQ(rule, parent, tar, dedut, ruleNum, parNum, tarNum):
	scrachPad = []
	scrachPad.append(snowClone("P>(Q>P)",{"P":"("+rule+")", "Q":dedut}))
	scrachPad.append("axiom 1")
	scrachPad.append(snowClone("P>(Q)",{"P":dedut, "Q":rule}))
	scrachPad.append("M.P. "+str(ruleNum)+","+str(tarNum))
	scrachPad.append(snowClone("(P>(Q))>((G)>(P>R))",{"P":dedut, "Q":rule, "G":parent, "R":tar}))
	scrachPad.append("axiom 2")
	scrachPad.append(snowClone("(P)>(Q>G)",{"P":parent, "Q":dedut, "G":tar}))
	scrachPad.append("M.P. "+str(tarNum+1)+","+str(tarNum+2))
	scrachPad.append(snowClone("P>Q",{"P":dedut, "Q":tar}))
	scrachPad.append("M.P. "+str(parNum)+","+str(tarNum+3))
	return scrachPad
	
def deduction(lList, tarList, dedut, parent):
	#l = open("temp.txt", "r")
	#lList = l.readlines()
	#l.close

	if len(tarList) == 0:
		s = open(tkFileDialog.asksaveasfilename(initialdir = os.path.dirname(os.path.realpath(__file__)),title = "Select file"),"w")
		for l in lList:
			#print l
			s.write(l+"\n")
		#mem.load("temp.txt")
	else:
		tar = tarList.pop()
		#print "==="+str(tar)+"==="
		nList = []
		
		#tarSen = lList[2*(tar-1)].strip("\n\r")
		#print tarSen
		
		i = 1
		offset = 0
		skip = 0
		fuzz = False
		for l in lList:
			nl = l.strip("\n\r")
			if skip == 0:
				#print nl
				if i <= 2*(tar-1):
					nList.append(nl)
					#print "test1"
				elif i == 2*(tar-1)+1:
					#print "test2"
					if parent == None:
						scrachPad = PisP(dedut, tar)
						for s in scrachPad:
							nList.append(s)
						offset += 4
						parent = tar+3
						skip = 2
					else:
						parent = tar - 1
						nList.append(nl)
						#i -= 1
						skip = 2
						fuzz = True
				elif "M.P." in nl:
					#print "test3"
					a, b = getSource(nl)
					#print a
					#print b
					if a == tar:
						ruleL = lList[2*(b-1)].strip("\n\r")
						#print ruleL
						parentL = nList[2*parent]
						#print parentL
						x,tarL = senParce(ruleL)
						#tarL = lList[i].strip("\n\r")
						#print tarL
						tarNum = (len(nList)+2)/2
						scrachPad = QisPQ(ruleL, parentL, tarL, dedut, b, parent+1, tarNum)
						for s in scrachPad:
							nList.append(s)
							#print s
						offset += 4
						tarList.append(((i+2)/2)+offset)
					elif b == tar:
						ruleL = lList[2*(a-1)].strip("\n\r")
						#print ruleL
						parentL = nList[2*parent]
						#print parentL
						x,tarL = senParce(ruleL)
						#tarL = lList[i].strip("\n\r")
						#print tarL
						tarNum = (len(nList)+2)/2
						scrachPad = QisPQ(ruleL, parentL, tarL, dedut, a, parent+1, tarNum)
						for s in scrachPad:
							nList.append(s)
							#print s
						offset += 4
						tarList.append(((i+2)/2)+offset)
					else:
						#nList.append("M.P. "+str(a+offset)+","+str(b+offset))
						if a > tar: a += offset
						if b > tar: b += offset
						nList.append("M.P. "+str(a)+","+str(b))
					#if a == tar:
						#ax2hp(b, tar, tarSen, nList)
						#offset 
					#print a
					#print b
				else:
					#print "test4"
					nList.append(nl)
				i += 1
			else:
				skip -= 1
				if fuzz:
					nList.append(nl)
					fuzz = False
					
		#s = open("temp.txt","w")
		#for l in nList:
		#	s.write(l+"\n")
		#s.close
		deduction(nList, tarList, dedut, parent)
		
def deductionS(sList, tar):
	lList = []
	#print tar
	#print sList[tar].sentenceData
	for s in sList:
		lList.append(s.sentenceData)
		lList.append(s.justData)
	
	deduction(lList, [tar+1], sList[tar].sentenceData, None)
	
	
		
if __name__ == "__main__":
	l = open("temp3.txt", "r")
	lList = l.readlines()
	l.close

	deduction(lList, [3], "a", None)
	#sp = QisPQ("a>b","a>a","b","a",2,7,8)
	#sp = QisPQ("b>c","a>b","c","a",1,12,13)
	
	#for s in sp:
	#	print s