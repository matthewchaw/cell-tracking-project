"""

Annotation Master Program
Check your annotations in multiple spaces -- straightened and unstraightened spaces. 

Developed by Matthew Chaw @ NIH/NIBIB

12/09/2021

"""



################# Imports ####################

import os
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
import csv 
import plotly.express as px


def main():
	"""
	Input: None
	Output: None
	
	Runs volumeRange() to determine range for volumes. 
	Uses function, isStrd() to determine whether the data has been straightened or not.
	Depending on the boolean output of isStrd(), straightened() or unstraightened() will be run. 
	Both straightened() and unstraightened() are looping functions, allowing user to stay in the functions
	"""

	#trackingDir = 'C:\\Users\\chawmm\\Desktop\\Worm_Untwisting\\091521_RW10742\\Pos5\\For_Tracking\\RegB - Copy'
	trackingDir = 'C:\\Users\\chawmm\\Desktop\\Worm_Untwisting\\RW10742_Hyp_Screen_Pos_5\\RegB'

	os.chdir(trackingDir)
	startVol, endVol = volumeRange()

	checkStrd = isStrd(trackingDir, startVol, endVol)

	if checkStrd == True:
		#Activate list of functions for straightened space
		straightened(trackingDir, startVol, endVol)

	elif checkStrd == False:
		#Activate list of functions for unstraightened space
		unstraightened(trackingDir, startVol, endVol)

	else:
		print("Error: Straightening check failed in main().") 


################# General Functions ####################

def volumeRange():
	"""
	Input: None
	Output: startVol and endVol

	Takes input from the user, which correspond to the indicated starting and ending volumes
	for the chosen dataset. These selections are then passed to main(). 
	"""

	try:
		startVol = int(input("Enter the FIRST volume where twitching begins in your data: "))
	except ValueError:
		print("Please enter an integer")

	try:
		endVol = int(input("Enter the LAST volume before hatching in your data: "))
	except ValueError:
		print("Please enter an integer")


	return startVol, endVol


def isStrd(trackingDir, startVol, endVol):
	"""
	Input: Directory, starting volume, ending volume
	Output: Boolean

	Using the informations from main() and volumeRange(),
	this function determines whether the super-majority of the data has been 
	straightened or has yet to be straightened. 
	This boolean is determined by the presence of straightened files 
	that are created by MIPAV after straightening. 
	Since these files are not present in unstraightened volumes, 
	this metric is used to form a boolean. 
	Boolean is then passed back to main to determine which suite of functions to use. 
	"""

	strCounter = 0
	for volume in range(startVol, endVol+1):

		if os.path.exists(trackingDir+'\\Decon_reg_{}\\Decon_reg_{}_results\\straightened_annotations'.format(volume, volume)) == True: #Volume has been straightened
			strCounter += 1
		else:
			continue

	if strCounter < (endVol+1 - startVol):
		checkStrd = False
	elif strCounter >= (endVol+1 - startVol):
		checkStrd = True 

	return checkStrd


################# CLASSES ####################


################# Pre-straightening ####################

def unstraightened(trackingDir, startVol, endVol):
	"""
	Input: Directory, starting volume, end volume
	Output: None

	Utilizes a while loop to allow the user to select which functions to choose. 
	This path will only be activated if the vast majority of volumes have not been straightened. 
	User is given 4 options and can select by inputting their responses. 
	Giving an invalid response will either trigger a ValueError or close the program. 
	"""


	go = True
	print("Data indicate that the majority of the volumes are unstraightened.\nRunning unstraightened packages.\nChoose from the options below.")
	while go == True:
		print("1) Check for duplicates\n2) Check annotations\n3) Run both 1 and 2 \n4) Quit")
		try:
			select = input("Enter selection here: ")

			select.strip()

			select = int(select)


		except ValueError:
			print("Please input a number as the selection")

		if select == 1:

			dupCheckFin = dupCheck(trackingDir, startVol, endVol)

			if len(dupCheckFin) == 0:
				print('There were no duplicate annotations!')
			else:
				print(dupCheckFin)

			print("... ... Completed ... ...\n")

		elif select == 2: 
			print('\n... ... Checking Annotations ... ...\n')

			unstrAnnotFin = unstr_annot(trackingDir, startVol, endVol)

			print(unstrAnnotFin)
			print("... ... Completed ... ...\n")

		elif select == 3:

			print("\n... ...Checking annotations and duplicates ... ...\n")

			dupCheckFin = dupCheck(trackingDir, startVol, endVol)
			unstrAnnotFin = unstr_annot(trackingDir, startVol, endVol)
			print(dupCheckFin, unstrAnnotFin)
			print("... ... Completed ... ...\n")

		else:
			print("\n... ... Exiting ... ...\n")

			go = False


def dupCheck(trackingDir, startVol, endVol):
	"""
	Input: Directory, starting volume, end volume
	Output: List of volume/annotation pairs

	Parses through annotation and lattice files to determine 
	if there are duplicate annotations or lattice points
	If there are erroneous duplicates, then they are 
	appended to the error counter as a string. 
	This list is then outputted to unstraightened or straightened. 
	"""
	

	err_counter = []
	for volume in range(startVol, endVol+1): 
		annot_file = open(trackingDir+"\\Decon_reg_{}\\Decon_reg_{}_results\\integrated_annotation\\annotations.csv".format(volume, volume), "r")
		lattice_file = open(trackingDir+"\\Decon_reg_{}\\Decon_reg_{}_results\\lattice_final\\lattice.csv".format(volume, volume), "r")
		annotList = []
		latticeList = []
		for line in annot_file:
			#print("Annot - Decon Reg #{}".format(i))
			ls = line.strip().split(",")
			if ls[0] == "":
				continue

			if ls[0] not in annotList:
				#print("annot", volume, ls[0])
				annotList.append(ls[0])
			else:
				print("\n*** ***\n", "in annotations", ls[0]+" is a duplicate in volume {}.".format(volume))
				err_counter.append("{}, {}".format(volume, ls[0]))
		for line in lattice_file:
			if ls[0] == "":
				continue
			ls = line.strip().split(",")
			if ls[0] not in latticeList:
				#print("lattice", volume, ls[0])
				latticeList.append(ls[0])
			else:
				print("\n*** ***\n", "In lattices", ls[0]+" is a duplicate in volume {}.".format(volume))
				err_counter.append("{}, {}".format(volume, ls[0]))

	return err_counter


def unstr_annot(trackingDir, startVol, endVol):
	"""
	Input: Directory, starting volume, end volume
	Output: None

	Parses through integrated annotations if there are no straightened annotations. 
	Dictionary is created with format {cell: volume, volume, ...}.
	If an annotation only occurs in fewer than 50% of volumes, then those 
	annotations are highlighted to the user. 
	Information is conveyed through print statements
	"""
	

	for volume in range(startVol, endVol+1):

		os.chdir(trackingDir+'\\Decon_reg_{}\\Decon_reg_{}_results\\integrated_annotation'.format(volume, volume))
		file = csv.reader(open('annotations.csv', 'r'))

		cellKey = {}
		for line in file: 
			try:

				if len(line) == 0 or 'name' in line:
					continue

				if line[0] not in cellKey: 			#Encountered new cell that is not yet added to key
					cellKey[line[0]] = [volume]		#create new addition to dictionary for that key, start a new list
					continue

				elif line[0] in cellKey:			#There is an instance of this cell in the key
					cellKey[line[0]].append(volume) #Append to the existing list in the corresponding dict
					continue

				else:
					print("an error occurred for volume {}".format(volume))

			except IndexError:
				print("IndexError at volume {}".format(volume))


	print("Annotated cells in the volumes include:", cellKey.keys())
	print("Counts include:")
	for key in cellKey:
		if len(cellKey[key]) > ((endVol-startVol) / 2):
			print(key, ":", len(cellKey[key]))
		else:
			print("'{}'only occurred {} time(s) in volumes: {}".format(key, len(cellKey[key]), cellKey[key])) 


################# Post-straightening ####################

def straightened(trackingDir, startVol, endVol):
	"""
	Input: Directory, starting volume, end volume
	Output: None

	Uses while loop to give the user autonomy in which functions to use.
	This path is only activated if the majority of volumes have been straightened. 
	User has four options: 
	Check location of straightened annotations via graphical or visual interpretation
	Check duplicates, or quit. 
	As of 12/13/21, statistical interpretation is not yet running. 
	"""

	go = True
	print("Data indicate that the majority of the volumes are straightened.\nRunning straightened packages.\nChoose from the options below.")
	while go == True:
		
		print("\n1) Check Straightened Annotations via graphical interpretation\n2) Check Straightened Annotations via statistical interpretation")
		print("3) Check for duplicate annotations\n4) Swap annotations")
		print("5) Run as though straightening has not occurred\n6) Quit")
		try:
			select = input("Enter selection here: ")

			select.strip()

			select = int(select)


		except ValueError:
			print("Please input a number as the selection")

		if select == 1:
			print('\n... ... Checking annotations via graphical interpretation ... ...\n')
			csaGraphical(trackingDir, startVol, endVol)
			print('... ... Completed ... ...\n')

		elif select == 2:
			print('\n... ... Checking annotations via statistical interpretation ... ...\n')
			csaStatistical(trackingDir, startVol, endVol)
			print('... ... Completed ... ...\n')

		elif select == 3:

			dupCheckFin = dupCheck(trackingDir, startVol, endVol)

			if len(dupCheckFin) == 0:
				print('There were no duplicate annotations!')
			else: 
				print(dupCheckFin)
			print("... ... Completed ... ...\n")
		elif select == 4:
			swapStrdAnnot(trackingDir, startVol, endVol)

		elif select == 5:
			unstraightened(trackingDir, startVol, endVol)

		elif select == 6:
			go = False

		else:
			print("\n... ... Exiting ... ...\n")

			go = False

def groupGraph(trackingDir, startVol, endVol):
	data = {'Volume': [], 'Name': [], 'X Voxel': [], 'Y Voxel': [], 'Z Voxel': [], 'Group': []}

	for volume in range(startVol, endVol+1):
		f = open(trackingDir+"\\Decon_reg_{}\\Decon_reg_{}_results\\straightened_annotations\\straightened_annotations.csv".format(volume, volume))
		file = csv.reader(f)

		for line in file:
			if line == None or len(line) < 1:
				continue
			elif line[0] == 'name':
				continue
			try:
				data['Volume'].append(volume)
				data['Name'].append(line[0])
				data['X Voxel'].append(line[1])
				data['Y Voxel'].append(line[2])
				data['Z Voxel'].append(line[3])
				data['Group'].append(line[0][:1])
			except IndexError:
				continue

	df = pd.DataFrame(data)


	print("\n\nView all cells as groups or view just a few cells (recommended)")
	try:

		select = int(input("1) View cells by group (Eg. 'A's, all 'B's)\n2) Select a few cells to view at a time (Eg. 'A0' and 'A2'\nEnter selection (1) or (2) here: ").strip())

		if select == 1:

			groups = (pd.unique(df['Group']))

			for group in groups:
				groupdf = df[df['Group'] == group]
				
				groupFig = px.line(groupdf, x='Volume', y = 'Y Voxel', color = 'Name', title = "Group {}: Y Voxel vs. volume".format(group))
				groupFig.show()
		else:
			print("To examine a single cell across volumes, enter the tracking name. Ex: A1")
			print("To track multiple cells, enter the tracking names separated by commas. Ex: A1, B2, A0, etc.")
			cellNameList = input("\nEnter here: ").upper().split(",")
			for i in range(len(cellNameList+1)):
				cellNameList[i] = cellNameList[i].strip()
			
			
			inddf = df[df['Name'].isin(cellNameList)]
			print(inddf)

			indFig = px.line(inddf, x='Volume', y = 'Z Voxel', color = 'Name', title = "Cell(s) {}: Z Voxel vs. volume".format(cellNameList))
			indFig.show()



	except ValueError:
			print("ValueError")
			pass
	except TypeError:
			print("TypeError")
			pass


def csaGraphical(trackingDir, startVol, endVol):

	"""
	Input: Directory, starting volume, end volume
	Output: Graphs via matplotlib.pyplot

	Option 1
	
	Uses matplotlib to create visual representations of the cell's position
	 in straightened space across all volumes. 
	User can select multiple volumes and can keep multiple open at the same time. 
	Three graphs per volume are opened: X vs. time, Y vs. time, Z vs. time. 
	
	"""
	os.chdir(trackingDir)
	group = input("View graphical interpretation by group? Ex. all 'A's or all 'B's?\nNot recommended for groups with 5 or more cells.\nY/N ").upper()
	if group == 'Y':
		return groupGraph(trackingDir, startVol, endVol)
	else:
		pass


	print("To examine a single cell across volumes, enter the tracking name. Ex: A1")
	print("To track multiple cells, enter the tracking names separated by commas. Ex: A1, B2, A0, etc.")
	cellNameList = input("\nEnter here: ").upper().split(",")

	length = len(cellNameList)


	for cellName in cellNameList:
		length -= 1
		cellName = cellName.strip()
		data = {"Volume": [], "X Voxel": [], "Y Voxel": [], "Z Voxel": []}


		for volume in range(startVol,endVol+1):
			annot_csv = trackingDir+"\\Decon_reg_{}\\Decon_reg_{}_results\\straightened_annotations\\straightened_annotations.csv".format(volume, volume)
			f = open(annot_csv)
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


def csaStatistical(trackingDir, startVol, endVol):

	"""
	Hope to incorporate standard deviation to check whether cell is in correct position or not. 
	Should be relatively simple. 

	Create dataframe using data. 
	append rows to dataframe one at a time.
	Or create dictionary of lists and append to list for each volume. Then create dataframe to run stats on. 
	May need to be point to point for each name across volumes?
	"""

	data = {"Volume": [], "Cell Name": [], "X Voxel": [], "Y Voxel": [], "Z Voxel": []}

	#Generating dataframe consisting of all volumes
	for volume in range(startVol, endVol+1):
		f = open(trackingDir+'\\Decon_reg_{}\\Decon_reg_{}_results\\straightened_annotations\\straightened_annotations.csv'.format(volume, volume), 'r')
		file = csv.reader(f)
		currVol = {"Volume": [], "Cell Name": [], "X Voxel": [], "Y Voxel": [], "Z Voxel": []}

		for line in file: 

			try:
				if line[0] == 'name':
					continue
				elif line[0] not in currVol['Cell Name']: #Passes over duplicates
					currVol['Cell Name'].append(line[0])
					data['Cell Name'].append(line[0])
					data['X Voxel'].append(line[1])
					data['Y Voxel'].append(line[2])
					data['Z Voxel'].append(line[3])
					data['Volume'].append(volume)
				else:
					print('Something happened')
			except IndexError:
				continue
	df = pd.DataFrame(data)
	print(df)


def swapStrdAnnot(trackingDir, startVol, endVol):

	print("Swapping cells can be difficult to revert and may result in eternal damnation.\nContinue? Y/N")
	cont = input("Select Y to continue or N to revert to menu.\n--> ").upper()

	if cont == 'Y': 
		cellA = input("Enter the name of the first cell to swap\n").upper().strip()
		cellB = input("Enter the name of the cell to swap with\n").upper().strip()

		print("First version of this code will only allow for a range of volumes to switch annotations.")
		try:
			volInput = input("Enter the volumes in range separated by '-'\nExample: '50-70'\nEnter Here: ")

			vols = volInput.strip().split('-')
			ls = []
			ls.extend(range(int(vols[0]), int(vols[-1])+1))
			print(ls)
		except TypeError:
			print("TypeError. Try again.")
		except ValueError:
			print("ValueError. Try again.")

		print("Swapping '{}' with '{}'. Correct?".format(cellA, cellB))
		cont = input("Y/N ").upper()

		if cont != 'Y':
			print("... ... Cancelling ... ...")
			return None

		for volume in ls:
			
			df = pd.read_csv(trackingDir+'\\Decon_reg_{}\\Decon_reg_{}_results\\straightened_annotations\\straightened_annotations.csv'.format(volume, volume))
			swapIntegAnnot(trackingDir, volume, cellA, cellB)
			aRow = df.loc[df['name'] == cellA] 					#row for cellA
			aIndex = df.index[df['name'] == cellA].tolist()		#Index for cellA
			bRow = df.loc[df['name'] == cellB] 					#row for cellB
			bIndex = df.index[df['name'] == cellB].tolist() 	#Index for cellB

			print("\n"+"-----"*2+'Strd_annot'+"-----"*2+'\n')



			try:
				aIndexOrig = df.at[aIndex[0], 'name']
				bIndexOrig = df.at[bIndex[0], 'name']
				print(df.loc[df['name'] == cellA])

				df.at[aIndex[0], 'name'] = cellB #switch cellA with cellB
				df.at[bIndex[0], 'name'] = cellA  #switch cellB with cellA

				aIndexNew = df.at[aIndex[0], 'name']
				bIndexNew = df.at[bIndex[0], 'name']
				print(df.loc[df['name'] == cellA])
				print("Straightened Annotation --> At volume {}, '{}' was swapped with '{}'.".format(volume, aIndexOrig, aIndexNew))

				df.to_csv(trackingDir+'\\Decon_reg_{}\\Decon_reg_{}_results\\straightened_annotations\\straightened_annotations.csv'.format(volume, volume), index = False)

			except IndexError:
				print("!!! !!! Index Error in volume {} for straightened_annotations.csv !!! !!!".format(volume))
				print(aRow)
				print(bRow)
				print("!!! !!! End of IndexError !!! !!!\n\n")



	else:
		print("... ... Exiting ... ...")


def swapIntegAnnot(trackingDir, volume, cellA, cellB):


	df = pd.read_csv(trackingDir+'\\Decon_reg_{}\\Decon_reg_{}_results\\integrated_annotation\\annotations.csv'.format(volume, volume))	
	aRow = df.loc[df['name'] == cellA] 					#row for cellA
	aIndex = df.index[df['name'] == cellA].tolist()		#Index for cellA
	bRow = df.loc[df['name'] == cellB] 					#row for cellB
	bIndex = df.index[df['name'] == cellB].tolist() 	#Index for cellB

	print("\n"+"-----"*2+'Integ_anot'+"-----"*2+'\n')


	try:
		aIndexOrig = df.at[aIndex[0], 'name']
		bIndexOrig = df.at[bIndex[0], 'name']

		df.at[aIndex[0], 'name'] = cellB #switch cellA with cellB
		df.at[bIndex[0], 'name'] = cellA  #switch cellB with cellA


		aIndexNew = df.at[aIndex[0], 'name']
		bIndexNew = df.at[bIndex[0], 'name']
		print("Integrated Annotation --> At volume {}, '{}' was swapped with '{}'.".format(volume, aIndexOrig, aIndexNew))

		df.to_csv(trackingDir+'\\Decon_reg_{}\\Decon_reg_{}_results\\integrated_annotation\\annotations.csv'.format(volume, volume), index = False)

	except IndexError:
		print("!!! !!! Index Error in volume {} for integrated_annotations\\annotations.csv !!! !!!".format(volume))
		print(aRow)
		print(bRow)
		print("!!! !!! End of IndexError !!! !!!\n\n")

main()
	