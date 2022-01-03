	

import matplotlib.pyplot as plt
import csv
import warnings #porque
import pandas as pd
import numpy as np
def main():
	trackingDir = "C:\\Users\\chawmm\\Desktop\\Worm_Untwisting\\091521_RW10742\\Pos5\\For_Tracking\\RegB"
	startVol = 6
	endVol = 97


	data = {'Volume': [], 'Name': [], 'X Voxel': [], 'Y Voxel': [], 'Z Voxel': [], 'Group': []}

	for volume in range(startVol, endVol+1):
		f = open(trackingDir+"\\Decon_reg_{}\\Decon_reg_{}_results\\straightened_annotations\\straightened_annotations.csv".format(volume, volume))
		file = csv.reader(f)

		for line in file:
			if line == None or len(line) < 1:
				continue
			elif line[0] == 'name' or line[0] == '' or line[0] == 'Unnamed: 0':
				continue
			try:
				data['Volume'].append(volume)
				data['Name'].append(line[0])
				data['X Voxel'].append(float(line[1]))
				data['Y Voxel'].append(line[2])
				data['Z Voxel'].append(line[3])
				data['Group'].append(line[0][:1])
			except IndexError:
				continue

	df = pd.DataFrame(data)
	#print(df)



	cellList = (pd.unique(df['Name']))

	for cell in cellList:
		top = '-'*25+' '+cell+' '+'-'*25
		bottom = '-'*(len(cell)+52)

		celldf = df[df['Name'] == cell]
		celldf = celldf[['X Voxel']]
		if len(celldf) < 3: #Extranneous, possibly erroneous annotations
			pass
		else:
			print(celldf)
			hampel_filter_pandas(celldf, 10, 3)	





def hampel_filter_pandas(input_series, window_size, n_sigmas=3):

    k = 1.4826 # scale factor for Gaussian distribution
    new_series = input_series.copy()

    # helper lambda function 
    MAD = lambda x: np.median(np.abs(x - np.median(x)))
    
    rolling_median = input_series.rolling(window=2*window_size, center=True).median()
    rolling_mad = k * input_series.rolling(window=2*window_size, center=True).apply(MAD)
    diff = np.abs(input_series - rolling_median)

    indices = list(np.argwhere(diff > (n_sigmas * rolling_mad)).flatten())
    new_series[indices] = rolling_median[indices]
    
    return new_series, indices





def hampel_filter(input_series, window_size, n_sigmas):
    
    n = len(input_series)
    new_series = input_series.copy()
    k = 1.4826 # scale factor for Gaussian distribution
    
    indices = []
    
    # possibly use np.nanmedian 
    for i in range((window_size),(n - window_size)):
        x0 = np.median(input_series[(i - window_size):(i + window_size)])
        S0 = k * np.median(np.abs(input_series[(i - window_size):(i + window_size)] - x0))
        if (np.abs(input_series[i] - x0) > (n_sigmas * S0)):
            new_series[i] = x0
            indices.append(i)
    
    return new_series, indices



main()