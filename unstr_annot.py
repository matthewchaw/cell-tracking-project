"""
Check the number of annotations across timepoints before straightening
"""
import csv
import os
#Cell Key


def main():

	regB = 'C:\\Users\\chawmm\\Desktop\\Worm_Untwisting\\RW10711_Pos3\\For_Tracking\\RegB'

	startVol = 19
	endVol = 107
	cellKey = {}

	for volume in range(startVol, endVol+1):

		os.chdir(regB+'\\Decon_reg_{}\\Decon_reg_{}_results\\integrated_annotation'.format(volume, volume))
		file = csv.reader(open('annotations.csv', 'r'))

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






main()


