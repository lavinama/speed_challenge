import argparse
from utils import video_to_frames, enhance_frames
import os

MACHINE = "Mac"
def preprocess_data(data_folder_path):
	train_video = data_folder_path + "train.mp4"
	# Turn video to frames
	train_path = video_to_frames(train_video)
	enhance_frames(train_path='data/train', destination="data")

def label_data(data_folder_path):
	# TODO:
		# 1. Load train.txt data and turn into a dataframe
		# 2. Add as first column the frame number (line number of txt file)
		# 3. Add as second column the label (speed of car)
	pass

if __name__ == "__main__":
	# command argument parser
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--data_path', type=str, default='data/',
	help='Path to the data folder.')
	args = parser.parse_args()
	
	data_folder_path = args.data_path
	preprocess_data(data_folder_path)
	if MACHINE == "Mac":
		os.system("say 'Data preprocessing finished'")