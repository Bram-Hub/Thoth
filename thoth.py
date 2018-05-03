from Tkinter import *
import sys
import sen, mem

if __name__ == "__main__":
	if len(sys.argv) > 1:
		mem.load(sys.argv[1])
	else:
		mem.start()
	