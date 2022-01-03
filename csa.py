"""
Matthew Chaw
NIBIB
10/28/2021
Version 1.0
"""



import numpy as np 
import pandas as pd 
import os
import matplotlib.pyplot as plt

"""
The purpose of this script is to allow the user to check their tracked cell positions in the straightened space. 
It will cell tracking names as inputs and output graphs drawn by matplotlib. 
Multiple cell names can be specified by using commas to separate cells. 

11/9/21
User can now choose from three functions relating to annotation cleaning. These options include:
1) Graphical representation of annotations in straightened space
2) statistical representation of annotations in straightened space -- if C0 in v45 is significantly different than in v46, then there's an issue. 
3) Duplicate check -- if there are instances in which a volume contains multiple of the same annotation, then the volume and annot. will be returned. 
"""


def config():

	regB = "C:\\Users\\chawmm\\Desktop\\091521_RW10742\\Pos5\\For_Tracking\\RegB" ### Change this to your respective path to RegB. Further filepaths are not necessary. 
	startVol = int(6)
	endVol = int(97)

	return regB, startVol, endVol


def csaGraphical(regB, startVol, endVol):
	"""
	Option 1

	input: path to regB, cells to track
	function: Uses matplotlib to create visual representations of the cell's position in straightened space across all volumes. 
	output: three graphs representing x, y, z vs. volume number. 
	"""

	os.chdir(regB)

	print("\n\n\n\n\n\n\nWelcome.\n\nEnter any number of cell name(s) below.")
	print("To examine a single cell across volumes, enter the tracking name. Ex: A1")
	print("To track multiple cells, enter the tracking names separated by commas. Ex: A1, B2, A0, etc.")
	cellNameList = input("\nEnter here: ").upper().split(",")

	length = len(cellNameList)


	for cellName in cellNameList:
		length -= 1
		cellName = cellName.strip()
		data = {"Volume": [], "X Voxel": [], "Y Voxel": [], "Z Voxel": []}


		for volume in range(startVol,endVol+1):
			annot_csv = "\\Decon_reg_{}\\Decon_reg_{}_results\\straightened_annotations\\straightened_annotations.csv".format(volume, volume)
			f = open(regB+annot_csv)
			boolVal = False
			for row in f:
				rowls = row.split(",")
				if rowls[0] == cellName:
					#print(x)
					boolVal = True
					data["Volume"].append(float(volume))
					data["X Voxel"].append(float(rowls[1]))
					data["Y Voxel"].append(float(rowls[2]))
					data["Z Voxel"].append(float(rowls[3]))
					break
			f.close()

		df = pd.DataFrame(data)

		if len(df) == 0: #<-- if empty cell (e.g. wrong cell input)
			continue

		else:
			X_plot = df.plot(y = "X Voxel", x = "Volume", kind = 'line', title = "{}: Volume Number vs. X Voxel".format(cellName))
			Y_plot = df.plot(y = "Y Voxel", x = "Volume", kind = 'line', title = "{}: Volume Number vs. Y Voxel".format(cellName))
			Z_plot = df.plot(y = "Z Voxel", x = "Volume", kind = 'line', title = "{}: Volume Number vs. Z Voxel".format(cellName))
			inp = ""


			while inp != "Q":
				plt.show(block=False)

				if length == 0:
					print("\nThere are no remaining cells in your query. Enter 'Q' to close all plots.")

				else:
					formText = "\nEnter 'Q' to close subplots for {} and move on to the next cell in your query.\nTo keep the plots for {} open while also moving to the next cell, enter any key.".format(cellName, cellName)
					print(formText)

				inp = input("Enter here\t").upper()
				if inp == "Q":
					plt.close()
					plt.close()
					plt.close()
					break
				else:
					break

def csaStatistical(regB, start, end):
	os.chdir(regB)
	currVol = {"Volume": [], "Cell Name": [], "X Voxel": [], "Y Voxel": [], "Z Voxel": []}
	prevVol = {}
	for volume in range(start, end+1):
		currVol = {"Volume": [], "Cell Name": [], "X Voxel": [], "Y Voxel": [], "Z Voxel": []}
		annot_csv = "\\Decon_reg_{}\\Decon_reg_{}_results\\straightened_annotations\\straightened_annotations.csv".format(volume, volume)
		f = open(regB+annot_csv)

		for row in f:
			if len(row) < 2:
				continue
			else:
				rowls = row.split(',')
				try:
					currVol["Volume"].append(volume)
					if rowls[0] == "name":
						pass
					elif rowls[1] == "":
						currVol["Cell Name"].append(rowls[0])
						currVol["X Voxel"].append(prevVol["X Voxel"][-1])
						currVol["Y Voxel"].append(prevVol["Y Voxel"][-1])
						currVol["Z Voxel"].append(prevVol["Z Voxel"][-1])
					else:
						currVol["Cell Name"].append(rowls[0])
						currVol["X Voxel"].append(float(rowls[1]))
						currVol["Y Voxel"].append(float(rowls[2]))
						currVol["Z Voxel"].append(float(rowls[3]))
				except ValueError:
					pass
	
		for i in range(len(currVol[cellName])):
			if currVol



"""







		for row in f:

			rowls = row.strip().split(",")
			if len(rowls) < 4:
				continue


			if volume == start:
				try:
					currVol["Volume"].append(volume)
					currVol["Cell Name"].append(rowls[0])
					currVol["X Voxel"].append(float(rowls[1]))
					currVol["Y Voxel"].append(float(rowls[2]))
					currVol["Z Voxel"].append(float(rowls[3]))
				except ValueError:
					pass
				except IndexError:
					pass
		
		oldVol = currVol
		currVol = {"Volume": [], "Cell Name": [], "X Voxel": [], "Y Voxel": [], "Z Voxel": []}

		try:
			currVol["Volume"].append(volume)
			currVol["Cell Name"].append(rowls[0])
			currVol["X Voxel"].append(float(rowls[1]))
			currVol["Y Voxel"].append(float(rowls[2]))
			currVol["Z Voxel"].append(float(rowls[3]))
		except ValueError:
			pass
		except IndexError:
			pass

		print("prevVol: ",oldVol, "\n", "currVol: ",currVol)

"""
def dupCheck(regB, start, end):

	"""
	Option 3

	input: Path to regB
	function: uses a set of nested for loops to determine whether there are duplicate annotations in a given volume. Also checks lattices. 
	output: printed notes on volumes that contain duplicate annotations. 

	"""
	os.chdir(regB)
	err_counter = []
	for i in range(start, end+1): 
		annot_file = open(regB+"\\Decon_reg_{}\\Decon_reg_{}_results\\integrated_annotation\\annotations.csv".format(i, i), "r")
		lattice_file = open(regB+"\\Decon_reg_{}\\Decon_reg_{}_results\\lattice_final\\lattice.csv".format(i, i), "r")
		annotList = []
		latticeList = []
		for line in annot_file:
			#print("Annot - Decon Reg #{}".format(i))
			ls = line.split(",")
			if ls[0] not in annotList:
				print("annot", i, ls[0])
				annotList.append(ls[0])
			else:
				print("\n*** ***\n", "in annotations", ls[0]+" is a duplicate in volume {}.".format(i))
				err_counter.append("{}, {}").format(i, ls[0])
		print(err_counter)



	#lattice
		for line in lattice_file:
			#print("Lattice - Decon Reg #{}".format(i))
			ls = line.split(",")
			if ls[0] not in latticeList:
				print("lattice", i, ls[0])
				latticeList.append(ls[0])
			else:
				print("\n*** ***\n", "In lattices", ls[0]+" is a duplicate in volume {}.".format(i))
				err_counter.append("{}, {}").format(i, ls[0])

		print(err_counter)



def main():


	regB, startVol, endVol = config()

	dia = "0"
	diaopt = "0123"

	while dia:
		print("\nChoose from option below:\n1) Check Straightened Annotations via graphical interpretation")
		print("2) Check Straightened Annotations via statistical interpretation\n3) Check for duplicate annotations")


		dia = input("Enter Option #: ").strip()

		if dia not in diaopt:
			print("\nPlease enter a valid input. '{}' is not a valid input. ".format(dia))
			continue

		elif dia == '1':
			csaGraphical(regB, startVol, endVol)
			break

		elif dia == '2':
			csaStatistical(regB, startVol, endVol)
			break
			

		elif dia == '3':
			dupCheck(regB, startVol, endVol)
			break

		elif dia == '0': 
			print("There is no option 0... ")
			continue

		else:

			print("Please enter a valid input.")

main()






