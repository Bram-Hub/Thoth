# THOTH
## Authors
2018:
Matthias Krutz

## About
Requirements 
	Python 2.7
Operation:
	Line Checkbox: used in executing modus ponens.

	Premise Entry Field: input a sentence directly. Only available in the first line of the proof or a line created by ‘Add Premise’, for readabilities sake. The value in the field is set to lowercase (for parsing reasons) and is locked after either ‘Add premise’ or ‘Add step’.

	Add Premise: Add a new “premise line”. Only available in the first line of the proof or a line created by ‘Add Premise’. If successful locks the current line.

	Add Step: executes the operation chosen from the Step Dropdown Menu.

	Step Dropdown Menu:

		modus ponens: attempts to execute modus ponens on the lines with their Line Checkbox checked. The > symbol stands in for implication. If the wrong number of lines is selected or modus ponens cannot be used on the selected lines the execution will fail and nothing will happen. Order does not matter.

		deduction: opens an input box for the sentence to be deduced. All proceeding sentences will only have “modus ponens” and “end” in the Step Dropdown Menu.

		“end”: ends the current deduction. The user will be asked where to save the generated proof

		“Q.E.D”: hides Add Step and the Step Dropdown Menu, to more easily view the proof, this change is purely visual and is not saved

		Axioms: all other options in the Step Dropdown Menu call different axioms. Opens an input box for the sentences to be used in the axioms.

Reflection:

	Goal: a system for constructing proofs using arbitrary axiom systems. Specifically, tools for automating the sometimes difficult tasks of filling in variables when calling axioms and executing deduction.

	To do:

		The lack of a working scroll bar currently put a hard and entirely arbitrary limit on the maximum size of a given proof

		Loading a proof leaves a dummy window of the initial proof

		The deduction operation does not work in all cases

	Difficulties: 

		This was the first time I have ever attempted to build any kind of Graphical User Interface and it shows to a degree.


		Getting the modus ponens operation to work with in all cases (namely different valid configurations of parentheses) was surprisingly difficult.
