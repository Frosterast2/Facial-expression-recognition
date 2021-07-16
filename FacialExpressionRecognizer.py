from fer import FER
import mediapipe as mp
import cv2
from tkinter import *
import tkinter.filedialog as tkf

win = Tk()
def brain(img):
	face = mp.solutions.face_detection
	draw = mp.solutions.drawing_utils
	detec = face.FaceDetection()

	detector = FER(mtcnn=True)

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
			cv2.putText(img, str(ressult), (x, y), cv2.FONT_HERSHEY_PLAIN, 2, color=(255, 255, 255), thickness=3)
		cv2.imshow("mat", img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

def camera():
	video = cv2.VideoCapture(0)
	ret, frame = video.read()
	return frame

Label(win, text="Choose your file").pack()
Button(win, text="Select file", command = lambda: brain(cv2.imread(tkf.askopenfilename()))).pack()

Label(win, text="Or take a pic").pack()
Button(win, text="Capture pic", command = lambda: brain(camera())).pack()
Button
mainloop()
