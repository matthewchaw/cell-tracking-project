import pandas as pd 
import numpy as np 
import os 
import matplotlib.pyplot as plt


def main():

##########################################################

	regB = "C:\\Users\\chawmm\\Desktop\\091521_RW10742\\Pos5\\For_Tracking\\RegB"
	DataFrame = pd.DataFrame()
	startVol = int(6)
	endVol = int(97)

##########################################################
	os.chdir(regB)

	print("Enter cell name below. Example: A0")
	cellName = input("Enter here: ").upper()

	data = {"Volume": [], "X Voxel": [], "Y Voxel": [], "Z Voxel": []}


	for volume in range(startVol,endVol+1):
		annot_csv = "\\Decon_reg_{}\\Decon_reg_{}_results\\straightened_annotations\\straightened_annotations.csv".format(volume, volume)
		f = open(regB+annot_csv)
		boolVal = False
		for row in f:
			x = row.split(",")
			if x[0] == cellName:
				print(x)
				boolVal = True
				data["Volume"].append(float(volume))
				data["X Voxel"].append(float(x[1]))
				data["Y Voxel"].append(float(x[2]))
				data["Z Voxel"].append(float(x[3]))
				break
			else:
				boolVal = False
		if boolVal == False:
			pass
		f.close()

	df = pd.DataFrame(data)
	#df.dropna(axis = 0, inplace = True)
	X_plot = df.plot(y = "X Voxel", x = "Volume", kind = 'line', title = "{}: Volume Number vs. X Voxel".format(cellName))
	Y_plot = df.plot(y = "Y Voxel", x = "Volume", kind = 'line', title = "{}: Volume Number vs. Y Voxel".format(cellName))
	Z_plot = df.plot(y = "Z Voxel", x = "Volume", kind = 'line', title = "{}: Volume Number vs. Z Voxel".format(cellName))

	print(df)
	plt.show()
main()






