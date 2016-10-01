#Starting point of the program.

import sys
from PyQt4 import QtGui, QtCore
import cv2
from imagecrop import main_run
from PIL import Image
from ocr import perform_ocr
import os

class Window(QtGui.QMainWindow):

	upload_complete_signal = QtCore.pyqtSignal()
	loc_qlabel_signal = QtCore.pyqtSignal()
	img_crop_signal = QtCore.pyqtSignal()
	original_width = 0
	original_height = 0
	is_crop = False
	boundary_xy = (0, 0, 0, 0)
	location_name = "Unknown"

	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(50, 50, 1280, 720)
		self.setWindowTitle("Optical Character Recognintion")
		self.setWindowIcon(QtGui.QIcon("progicon.png"))
		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))
		
		#============================Menu Bar=============================================
		extractAction = QtGui.QAction("&Exit program",self)
		extractAction.setShortcut("Ctrl+Q")
		extractAction.setStatusTip("Quit Program")
		extractAction.triggered.connect(self.close_app)
		
		self.statusBar()
		
		mainMenu = self.menuBar()	#Need to make modifications so assign to a variable
		
		fileMenu = mainMenu.addMenu("&File")
		fileMenu.addAction(extractAction)
		
		editMenu = mainMenu.addMenu("&Edit")
		editMenu.addAction(extractAction)
		
		
		
		self.home()
	
	def home(self):
		
	#Quit Button Right
		quitbtn = QtGui.QPushButton("Quit",self)
		quitbtn.clicked.connect(self.close_app)
		quitbtn.setStatusTip("Quit Program")
		quitbtn.resize(quitbtn.sizeHint())
		#quitbtn.move(100, 100)
	
	
	#Select Image
		loadimgbtn = QtGui.QPushButton("Load image",self)
		loadimgbtn.clicked.connect(self.load_image)
		loadimgbtn.setStatusTip("Browse for image")
		loadimgbtn.resize(loadimgbtn.sizeHint())
		#quitbtn.move(100, 100)


	#Crop Image
		cropimgbtn = QtGui.QPushButton("Crop image",self)
		cropimgbtn.clicked.connect(self.crop_image)
		cropimgbtn.setStatusTip("Browse for image")
		cropimgbtn.setEnabled(False);
		self.upload_complete_signal.connect(lambda: cropimgbtn.setEnabled(True))
		
		cropimgbtn.resize(cropimgbtn.sizeHint())
		#quitbtn.move(100, 100)

	#Extract Image
		extracttxtbtn = QtGui.QPushButton("Extract text",self)
		
		extracttxtbtn.setStatusTip("Extract image from text")
		extracttxtbtn.resize(extracttxtbtn.sizeHint())
		extracttxtbtn.setEnabled(False);
		self.upload_complete_signal.connect(lambda: extracttxtbtn.setEnabled(True))
		#QtCore.QCoreApplication.processEvents()
		extracttxtbtn.clicked.connect(self.extract_text)
			
		#quitbtn.move(100, 100)
		
	#File location QLabel
		loc_qlabel = QtGui.QLabel(self)
		loc_qlabel.hide()
		[self.loc_qlabel_signal.connect(x) for x in [lambda: loc_qlabel.setText(self.location_name), lambda: loc_qlabel.show()]]
		loc_qlabel.move(1070,270)
		#self.loc_qlabel_signal.connect(lambda: loc_qlabel.show())
	
	#Crop boundary QLabel
		img_bound_qlabel = QtGui.QLabel(self)
		img_bound_qlabel.hide()
		#myString = ",".join(str(v) for v in self.boundary_xy)
		[self.img_crop_signal.connect(x) for x in [lambda: img_bound_qlabel.setText(",".join(str(v) for v in self.boundary_xy)),lambda: img_bound_qlabel.show()]]
		img_bound_qlabel.move(1070,360)
	
			
	#Vertical Box Right
		v_but_box = QtGui.QVBoxLayout()
		v_but_box.addWidget(loadimgbtn)
		v_but_box.addWidget(cropimgbtn)
		v_but_box.addWidget(extracttxtbtn)
		v_but_box.addWidget(quitbtn)
		
		v_but_box.setGeometry(QtCore.QRect(1064,175,150,450))
		
	#Insert OCR image	
		pic = QtGui.QLabel(self)
		pic.setGeometry(200, 20, 800, 100)
		#use full ABSOLUTE path to the image, not relative
		pic.setPixmap(QtGui.QPixmap("nn2.png"))
	
	
	
		self.show()
	
	def close_app(self):
		choice = QtGui.QMessageBox.question(self,"Exit","Are you sure you want to quit?",QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		if choice == QtGui.QMessageBox.Yes:
			print("Program Quit!!")
			sys.exit()
		else:
			pass
			#print "This is the end"
			#sys.exit()	
			
	
	def extract_text(self):
		if self.is_crop == False:
			self.extract_without_crop_message()
	
		else:
			self.extract_with_crop()
	
	
	def extract_without_crop_message(self):
		extract_choice = QtGui.QMessageBox.question(self,"Continue?","Are you sure you want to continue without cropping the image?",QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		if extract_choice == QtGui.QMessageBox.Yes:
			print("Proceeding without image crop........")
			print self.boundary_xy
			perform_ocr("original_img.jpg")
			os.startfile("output.txt")
		else:
			pass	
			
	def extract_with_crop(self):
		print "Extracting with cropped image........"
		print self.boundary_xy
		perform_ocr("original_cropped.jpg")
		os.startfile("output.txt")

		
		
	def load_image(self):
		
		
		name = QtGui.QFileDialog.getOpenFileName(self,"Select image","C:\\","Image files (*.jpg *.gif *.png)")
		self.location_name = name
		self.loc_qlabel_signal.emit()
		input_img = cv2.imread(str(name))
		#input_img = cv2.cvtColor(input_img, cv2.cv.CV_BGR2RGB)
		cv2.imwrite("original_img.jpg",input_img)
		print "Image Load Complete........"
		self.store_orgimg_data(input_img.shape)
		self.is_crop = False
		self.upload_complete_signal.emit()
		
		resized_img = self.resizeimg(input_img,1024,576)
		cv2.imwrite("to_crop.jpg",resized_img)
		
		res_height, res_width = resized_img.shape[0], resized_img.shape[1]
		#qImg = QtGui.QImage(resized_img.data, res_width, res_height, res_width*3, QtGui.QImage.Format_RGB888)
		qImg = QtGui.QImage(cv2.cvtColor(resized_img, cv2.cv.CV_BGR2RGB), res_width, res_height, res_width*3, QtGui.QImage.Format_RGB888)
		pix = QtGui.QPixmap(qImg)
		inputimg_label = QtGui.QLabel(self)
		inputimg_label = QtGui.QLabel(self)
		inputimg_label.setGeometry(20, 120, 1024, 576)
		inputimg_label.setPixmap(pix)
		
		
		
		#inputimg_label.clear()
		
		#file = open(name,'r')
		#print name
		#input_img.setPixmap(QtGui.QPixmap(name))
		inputimg_label.show()
		self.upload_complete_signal.connect(inputimg_label.hide)

	
	#============openCV input picture resize to 1024 * 576 for display
	
	def resizeimg(self,input_img,w,h):	
		#print "Hello"
		o_height = input_img.shape[0]
		o_width = input_img.shape[1]
		aspect_ratio = o_width/(o_height*1.0)
		
		if(aspect_ratio < 1.777): # aspect ratio less than 16:9
			#aspectRatio = o_width / (o_height*1.0)
			height = h
			width = int(height * aspect_ratio)
			input_img = cv2.resize(input_img, (width,height))
			
		elif(aspect_ratio > 1.777): # aspect ratio more than 16:9
					
			#aspectRatio = o_height / (o_width*1.0)	
			width = w
			height = int(width / aspect_ratio)
			input_img = cv2.resize(input_img, (width,height))
					
		else: # aspect ratio exactly 16:9
			input_img = cv2.resize(input_img, (h,h))
		print input_img.shape
		return input_img
	
	def store_orgimg_data(self, shape):
		self.original_height, self.original_width = shape[0], shape[1]
		self.boundary_xy = (0, 0, shape[1], shape[0])
		
	
	def crop_image(self):
		x1, y1, x2, y2, to_crop_width, to_crop_height = main_run()
		
		x1_final = x1*self.original_width/to_crop_width
		y1_final = y1*self.original_height/to_crop_height
		x2_final = x2*self.original_width/to_crop_width
		y2_final = y2*self.original_height/to_crop_height 
		
		self.store_crop_coordinates(x1_final, y1_final, x2_final, y2_final)
		
	def store_crop_coordinates(self,x1, y1, x2, y2):
		
		self.boundary_xy = (x1, y1, x2, y2)
		#print self.boundary_xy
		im1 = Image.open('original_img.jpg')
		box = (x1,y1,x2,y2)
		im1 = im1.crop(box)
		im1.save("original_cropped.jpg")
		print "Image Crop Complete........"
		self.img_crop_signal.emit()
		self.is_crop = True
		
		
		
def run():	
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())
	

run()	