import cv2
import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageEnhance

def load_data_labels(filename: str) -> pd.DataFrame:
	"""loads the label data into a pandas.DataFrame object

	:param filename: file path of data 
	:return: dataframe with frame and label
	"""
	# Load the labels into python with using a pandas DataFrame
	data = pd.read_csv(filename, sep=",", header=None)
	# keep track of what frame corresponds to what speed
	data['frame'] = data.index
	# name the speed column "label"
	data.columns = ['label','frame']
	# swap the columns so that the dataframe reads, more conventionally, item name on the left and label on the right
	data = data[['frame','label']]
	# return the dataFrame object
	return data

def video_to_frames(video: str, destination='data') -> str:
	"""Turn video to frames

	:param video: path to the video, 'train.mp4'
	:param destination: the final folder in which you want to store the train folder
	:return: train path, 'data/train'
	"""
	vidcap = cv2.VideoCapture(video)
	success,image = vidcap.read()
	count = 0

	# make the directory to store the frames
	train_path = destination + '/train'
	Path(train_path).mkdir(parents=True, exist_ok=True)

	# write raw frames to local files
	while success:
		if not cv2.imwrite(destination + '/train/frame' + str(count) + '.jpg', image):    # save frame as JPEG file
			raise Exception("Could not write image")
		success,image = vidcap.read()
		print(f'Read frame {count}: {success}')
		count += 1
	return train_path

def enhance_frames(train_path='data/train', destination='data'):
	"""enhance the files, copy them into a different folder

	:param train_path: original path
	:param destination: new path of transformed images
	"""
	Path(destination + '/trainbright').mkdir(parents=True, exist_ok=True)
	for img in os.listdir(train_path):
		img_path = '{}/{}'.format(train_path, img)
		print("img_path", img_path)
		im = Image.open(img_path)

		brightness = ImageEnhance.Brightness(im)
		im = brightness.enhance(1.5)

		contrast = ImageEnhance.Contrast(im)
		im = contrast.enhance(2)

		sharpness = ImageEnhance.Sharpness(im)
		im = sharpness.enhance(2)

		im = im.save(destination + '/trainbright/%s' %img)

def opticalFlowDense(image_current, image_next):
	"""calculates optical flow magnitude and angle and places it into HSV image

	:param image_current: current frame (RGB image)
	:param image_next: next frame (RGB image)
	:return: RGB image with optical flow

	Steps:
	1. Set the saturation to the saturation value of image_next
	2. Set the hue to the angles returned from computing the flow params
	3. Set the value to the magnitude returned from computing the flow params
	4. Convert from HSV to RG
	"""
	
	gray_current = cv2.cvtColor(image_current, cv2.COLOR_RGB2GRAY)
	gray_next = cv2.cvtColor(image_next, cv2.COLOR_RGB2GRAY)
	
	hsv = np.zeros(image_current.shape)
	# set saturation
	hsv[:,:,1] = cv2.cvtColor(image_next, cv2.COLOR_RGB2HSV)[:,:,1]
 
	# Flow Parameters
	flow_mat = None
	image_scale = 0.5
	nb_images = 1
	win_size = 15
	nb_iterations = 2
	deg_expansion = 5
	STD = 1.3
	extra = 0

	# obtain dense optical flow paramters
	flow = cv2.calcOpticalFlowFarneback(gray_current, gray_next,  
										flow_mat, 
										image_scale, 
										nb_images, 
										win_size, 
										nb_iterations, 
										deg_expansion, 
										STD, 
										0)
										
		
	# convert from cartesian to polar
	mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])  
		
	# hue corresponds to direction
	hsv[:,:,0] = ang * (180/ np.pi / 2)
	
	# value corresponds to magnitude
	hsv[:,:,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
	
	hsv = np.asarray(hsv, dtype= np.float32)    

	rgb_flow = cv2.cvtColor(hsv,cv2.COLOR_HSV2RGB)
	
	return rgb_flow

def save_image(path,i, trainset):
	try:
		img = opticalFlowDense(trainset[i],trainset[i+1])
	except IndexError:
		return
	plt.figure()
	plt.axis("off")
	plt.imshow(img)
	plt.savefig(f'{path}{i}.jpg', bbox_inches='tight',pad_inches=0)
	plt.close()
