from re import template
from fer import FER
import mediapipe as mp
import cv2
from tkinter import *
import tkinter.filedialog as tkf
#import multiprocessing
#from tkinter import PhotoImage
from PIL import ImageTk, Image
import webbrowser

win = Tk()
face = mp.solutions.face_detection
draw = mp.solutions.drawing_utils
detec = face.FaceDetection()

#detector = FER(mtcnn=True)
def brain(img):
	detector = FER(mtcnn=True)

	resultwin = Toplevel()

	def innerbrain(img):
		rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		results = detec.process(rgb)

		if results.detections:
			e = detector.detect_emotions(img)[0]["emotions"]

			list = []
			for detection in results.detections:
				h, w, channels = img.shape
				x, y = int(detection.location_data.relative_bounding_box.xmin * w), int(detection.location_data.relative_bounding_box.ymin * h)
				draw.draw_detection(img, detection)
				percent = max([e["angry"], e["disgust"], e["fear"], e["happy"], e["sad"], e["surprise"], e["neutral"]])
				emotion = ""
				for i in e:
					if e[i] == percent:
						emotion = i
				ressult = f'{percent * 100}% {emotion}'
				#cv2.putText(img, str(ressult), (x, y), cv2.FONT_HERSHEY_PLAIN, 1.3, color=(255, 255, 255), thickness=3)
				actualresult = Label(resultwin, text=ressult)

				resultsHTML = f"""<html>
			<head>
				<meta charset="utf-8">
				<meta http-equiv="X-UA-Compatible" content="IE=edge">
				<title></title>
				<meta name="description" content="">
				<meta name="viewport" content="width=device-width, initial-scale=1">
				<link rel="stylesheet" href="">
				<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
				<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
				<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
				<link rel="preconnect" href="https://fonts.googleapis.com">
				<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
				<link href="https://fonts.googleapis.com/css2?family=Ubuntu:wght@300&display=swap" rel="stylesheet">
				<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
				<style rel="stylesheet">
					body{'''{
						font:Ubuntu;
					}'''}
				</style>
			</head>
			<body>
				<div class="jumbotron">
					<h1 class="display-3">Facial Expression Recognizer</h1>
					<p class="lead">Reports</p>
					<hr class="my-2">
				</div>
				<img src="FER_Result.png", height=300, width=300 alt="Results">
				<div>
					<ul>
						<li>Angry: {e["angry"] * 100}%</li>
						<li>Disgust: {e["disgust"] * 100}%</li>
						<li>Fear: {e["fear"] * 100}%<li>
						<li>Happy: {e["happy"] * 100}%</li>
						<li>Sad: {e["sad"] * 100}%</li>
						<li>Surprise: {e["surprise"] * 100}%</li>
						<li>Neutral: {e["neutral"] * 100}%</li>
					</ul>
				</div>
			</body>
		</html>"""
				
				with open("D_Report_FER.html", "wt") as file:
					file.write(resultsHTML)

				

				cv2.imwrite("FER_Result.png", img)

		reportlabel = Label(resultwin, text="----------Reports----------")

		def nothing():
			pass

		reports = Button(resultwin, text="Get Detailed Report", command=lambda: webbrowser.open("D_Report_FER.html"))


		img = ImageTk.PhotoImage(Image.open("FER_Result.png"))
		panel = Label(resultwin, image = img)
		panel.image=img
		panel.pack()

		actualresult.pack()

		reportlabel.pack()
		reports.pack()
	
	innerbrain(img=img)

def camera():
	video = cv2.VideoCapture(0)
	ret, frame = video.read()
	return frame

Label(win, text="Choose your file").pack()
Button(win, text="Select file", command = lambda: brain(cv2.imread(tkf.askopenfilename()))).pack()

Label(win, text="Or take a pic").pack()
Button(win, text="Capture pic", command = lambda: brain(camera())).pack()

mainloop()
