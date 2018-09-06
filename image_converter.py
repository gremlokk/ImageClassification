#!/usr/bin/python
# -*- coding: utf-8 -*-

#install pyqt: sudo apt-get install python-qt4
#https://github.com/Werkov/PyQt4/blob/master/examples/tools/regexp.py
import os, errno, sys
import time
import PythonMagick
from wand.image import Image
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class window(QWidget):
	
	# Initializing GUI components
	def __init__(self, parent = None):
		super(window, self).__init__(parent)

		self.initUI()

	def initUI(self):
		main_layout = QFormLayout()

		hbox1 = QHBoxLayout()
		hbox2 = QHBoxLayout()
		hbox3 = QHBoxLayout()

		#Form widget creation
		self.filepath_label = QLabel('Enter a filepath')
		self.path_entry = QLineEdit()
		self.convert_button = QPushButton('Convert')
		
		self.convert_button.clicked.connect(self.convert_button_pressed)

		#self.rename_radio_button = QRadioButton("Rename")
		self.single_file_radio_button = QRadioButton("Single")
		self.multi_file_radio_button = QRadioButton("Multi")
	  	self.multi_file_radio_button.setChecked(True)

		self.progess_bar_label = QLabel('Progress Bar:')
		self.progress_bar = QProgressBar()
		self.progress_bar.setValue(0)
		
		self.types = ('.jpg', '.png', '.tiff', '.pdf')

		self.filetypes = QComboBox()
		self.filetypes.addItems(self.types)
			
		#type_dialog = QInputDialog.getText()
	
		# Child form widget layout placement
		hbox1.addWidget(self.filepath_label)
		hbox1.addWidget(self.path_entry)
		hbox1.addWidget(self.filetypes)
		hbox1.addWidget(self.convert_button)

		#hbox2.addWidget(self.rename_radio_button)
		hbox2.addWidget(self.single_file_radio_button)
		hbox2.addWidget(self.multi_file_radio_button)

		hbox3.addWidget(self.progess_bar_label)
		hbox3.addWidget(self.progress_bar)

		# Adding widges to master form
		main_layout.addRow(hbox1)
		main_layout.addRow(hbox2)
		main_layout.addRow(hbox3)
		main_layout.setAlignment(hbox2, Qt.AlignCenter)

		# Main window configuration
		self.setLayout(main_layout)
		self.setFixedSize(500,100)
		self.setWindowTitle("Image Converter")
	
	def convert_button_pressed(self):
		self.progress_bar.setValue(0)
		if self.path_entry.text().isEmpty() and self.single_file_radio_button.isChecked(): # Checks if path_entry is empty when single button is clicked
			text = str(self.filetypes.currentText())
			entry = self.path_entry.setText(str(QFileDialog.getOpenFileName(self,"Select a file")))
		
		elif self.path_entry.text().isEmpty() and self.multi_file_radio_button.isChecked(): # Checks if path_entry is empty when multiple button is clicked
			self.path_entry.setText(str(QFileDialog.getExistingDirectory(self,"Select a Directory")))

		else:
			print 'converting files'
			self.convert_files()

			self.path_entry.setText('')
	

	def create_ouput_dir(self): #get single file to work
		self.saved_output_path = unicode(self.path_entry.text())+'/output'

		if os.path.isdir(self.path_entry.text()): 
			try:
				os.makedirs(self.saved_output_path)
			except OSError as e:
				if e.errno != errno.EEXIST:
					raise 		

	def rename_file(self):
		#ask if they are sure they want to change name		
		#create a dialog box that tells user to enter name
		new_filename = unicode(self.path_entry.text())
		
		filepath = str(QFileDialog.getExistingDirectory(self,"Select a Directory"))
		
		file_count = 0

		# split dir, filename, ext
		for file in os.listdir(unicode(filepath)):
			if file.lower().endswith(self.types):
				os.rename(os.path.join(filepath, file), os.path.join(new_filename, str(file_count+1)+'.jpg'))


	
	def convert_files(self):
			
		file_directory = (unicode(self.path_entry.text()))
		file_count = 0
		
		# converts a single image file
		if os.path.isfile(file_directory) and self.single_file_radio_button.isChecked():
				
			split_path = os.path.split(file_directory)[0]
			#print split_path
		
			file_name =  os.path.split(file_directory)[1]	
			#print file_name
	
			if os.path.isfile(file_directory) and file_name.lower().endswith(self.types):		
				file_location = str(os.path.join(split_path,str(file_name)))
				image = PythonMagick.Image(file_location)
					
				if image.size().width() >= 1024 and image.size().height() >= 1024:#1024 originally 		
					w, h = image.size().width(), image.size().height()
					image.resize("{}x{}".format(w/2, h/2))
													
					print 'File is large' #divide by 4 or 3

				converted_image_name = 'image_'+str(file_count+1)+str(self.filetypes.currentText())

				image.write("{}".format(str(os.path.join(split_path,converted_image_name))))	

		# converts image files in directory (Test pdf conversion)
		elif os.path.isdir(file_directory) and self.multi_file_radio_button.isChecked():

			length_of_valid_filetypes = len([file for file in os.listdir(file_directory) if file.lower().endswith(self.types)])
			self.create_ouput_dir()

			if length_of_valid_filetypes <= 0:
				self.progress_bar.setMaximum(1)
			else:
				self.progress_bar.setMaximum(length_of_valid_filetypes)

			for file in os.listdir(file_directory):

				if file.lower().endswith(self.types):
					file_location = str(os.path.join(file_directory,str(file)))
					
					image = PythonMagick.Image(file_location)
					
					if image.size().width() >= 1024 and image.size().height() >= 1024:#1024 originally 
						w, h = image.size().width(), image.size().height()
						image.resize("{}x{}".format(w/2, h/2))							
						print 'File is large' #divide by 4 or 3

					converted_image_name = 'image_'+str(file_count+1)+str(self.filetypes.currentText())

					image.write("{}".format(str(os.path.join(self.saved_output_path,converted_image_name))))
			
					file_count = file_count + 1

					self.progress_bar.setValue(file_count)
					QCoreApplication.processEvents()
			#Check if user would like to rename file 
		
						
def main():
	app = QApplication(sys.argv)
	gui = window()
	gui.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
