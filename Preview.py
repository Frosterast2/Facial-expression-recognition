#I dont really write comments for my code, but for the ease of understanding, I have written it

#importing the modules
from fer import FER
import cv2
from tkinter import *
import tkinter.filedialog as tkf

#setting up the GUI(the window)
win = Tk()
#setting up the facial expression detector
detector = FER(mtcnn=True)

#the main code
def brain(img):
	#reading the image(to perform operations on it)
	img = cv2.imread(img)
	#detecting the expressions from the image
	e = detector.detect_emotions(img)[0]["emotions"]
	#creating a new window for results
	resultwin = Toplevel()
	#Writing the results to the results window
	for i in e:
		Label(resultwin, text=f"{i}: {e[i] * 100}%").pack()
	
#the text in the actual window
Label(win, text="Choose your file").pack()
#the button to select the file
Button(win, text="Select file", command = lambda: brain(tkf.askopenfilename())).pack()
#the command to make the gui keep running until closed
mainloop()
