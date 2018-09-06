#!/usr/bin/python
import os, sys
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

label_lines = [line.rstrip() for line in tf.gfile.GFile("retrained_labels.txt")]#load labels

with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:# Load unpersists graph from file
	graph_def = tf.GraphDef()
	graph_def.ParseFromString(f.read())
	tf.import_graph_def(graph_def, name='')

def load_image_into_numpy_array(image):#Load image into numpy array
	(im_width, im_height) = image.size
	return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

PATH_TO_TEST_IMAGES_DIR = os.path.join(os.getcwd(), 'test_images')
TEST_IMAGE_PATHS = []
IMAGE_SIZE = (6, 4)

for file in os.listdir(PATH_TO_TEST_IMAGES_DIR):#finds the path for test images.
	if file.endswith('.jpg'):
		data = os.path.join(PATH_TO_TEST_IMAGES_DIR, file)
		TEST_IMAGE_PATHS.append(data)
		
with tf.Session() as sess:#predicts what image could be based on model
	for image_path in TEST_IMAGE_PATHS: 
		softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
		try:
			image = Image.open(image_path)
			image.convert('RGB')
			image_np = load_image_into_numpy_array(image)
	    	except:
			print 'Could not open image'
			continue

		predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0': tf.gfile.FastGFile(image_path, 'rb').read()})
	    
		top_k = predictions[0].argsort()[-len(predictions[0]):][:1:-1] #prints top 3 results
	    	
     		plt.figure(figsize=IMAGE_SIZE)

		if len(TEST_IMAGE_PATHS) > 0:	
			for node_id in top_k:
				human_string = label_lines[node_id]
				score = predictions[0][node_id]
			
				stuff = str(human_string) + ': ' + str(score)
				lbl = plt.plot(0, 0, label=stuff)
				#print('%s (score = %.5f)' % (human_string, score))

				legend = plt.legend(loc='lower left',handlelength=0, handletextpad=0)
				legend.get_frame().set_facecolor('#00ff00')
				legend.set_title("Predictions")

				#turns off legend markers
				for item in legend.legendHandles:
					item.set_visible(False)

		plt.imshow(image_np,interpolation='nearest', aspect='auto')
		plt.show()
		
