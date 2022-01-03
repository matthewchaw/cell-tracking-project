import os



"""
Checks for duplicate annotations or lattices
"""

def main():

	start = 6
	end = 97
	regB = "C:\\Users\\chawmm\\Desktop\\091521_RW10742\\Pos5\\For_Tracking\\RegB"









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

main()


