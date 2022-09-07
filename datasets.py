import os
from PIL import Image, ImageEnhance
import pandas as pd
import argparse
from torch.utils.data import Dataset,DataLoader,SubsetRandomSampler
from torchvision import transforms

class imageDataset(Dataset):
	"""
	A custom PyTorch dataset that can be fed into a DataLoader.
	"""
	def __init__(self, dataframe: pd.DataFrame, root_dir: str, transform=None):
		"""
		:param dataframe: dataframe with respective label
		:param root_dir: location of image dataset
		:param transform: function
		"""
		self.dataframe = dataframe
		self.root_dir = root_dir
		self.transform=transform

	def __len__(self):
		return len(self.dataframe)

	def __getitem__(self, idx):
		label = self.dataframe.label.values[idx]
		im = Image.open(self.root_dir+"/frame"+str(self.dataframe.frame.values[idx])+".jpg")
		#TODO: normalize image according to its own mean by channel
		if self.transform:
			im = self.transform(im)

		return im, label
