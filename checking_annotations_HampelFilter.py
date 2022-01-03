import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt 
import xlsxwriter 

#Annotaitons below need to be changed according to what youre looking for
annotations = ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'C0', 'C1']
#annotations = ['D1','D2','D3','D4','D6','R2','R3','R4','R5','R6']
data = {}
for annotation in annotations:
#volumes need to be changed according to the data set    
    for csvindex,csv_num in enumerate(range(6, 97)):
        if csvindex==0:
            data[annotation]=[]
        try:
#file path change below (variable = file)            
            csv_num = str(csv_num)
            #gabi1(7-85)
            #file = r'Z:\Cell_Tracking_Project\OD1599_NU\112619_OD1599_NU\OD1599_NU\OD1599_NU_1pt2_3\OD1599_NU_1pt2_3\Pos0\SPIMB\Decon_reg\SPIMB\Decon_reg_'+csv_num+r'\Decon_reg_'+csv_num+r'_results\straightened_annotations\straightened_annotations.csv'
            #gabi2 (15-108)
            file = r'C:\Users\chawmm\Desktop\Worm_Untwisting\091521_RW10742\Pos5\For_Tracking\RegB - Copy\Decon_reg_'+csv_num+r'\Decon_reg_'+csv_num+r'_results\straightened_annotations\straightened_annotations.csv'
            #daniel (8-112)
            #file = r'Z:\Cell_Tracking_Project\OD1599_NU\112719_OD1599_NU\OD1599_NU\OD1599_NU\OD1599_NU\Pos3\SPIMB\Reg_Sample\Decon_Reg\RegB\Decon_reg_'+csv_num+r'\Decon_reg_'+csv_num+r'_results\straightened_annotations\straightened_annotations.csv'
            #file = r'Z:\Cell_Tracking_Project\JCC596_NU\Untwisting\082619_JCC596_NU\JCC596_NU\Pos3\SPIMB_result\Reg_Sample\Decon_registered\RegB\Decon_reg_'+csv_num+'\Decon_reg_'+csv_num+'_results\straightened_annotations\straightened_annotations.csv'
            df = pd.read_csv(file)
            df_np = df.to_numpy() 

#file path change below (variable = file2)           
            #total length
            file2 = r'C:\Users\chawmm\Desktop\Worm_Untwisting\091521_RW10742\Pos5\For_Tracking\RegB - CopyDecon_reg_'+csv_num+'\Decon_reg_'+csv_num+'_results\straightened_lattice\straightened_lattice.csv'
            #file2 = r'Z:\Cell_Tracking_Project\JCC596_NU\Untwisting\082619_JCC596_NU\JCC596_NU\Pos3\SPIMB_result\Reg_Sample\Decon_registered\RegB\Decon_reg_'+csv_num+'\Decon_reg_'+csv_num+'_results\straightened_lattice\straightened_lattice.csv'
            df2 = pd.read_csv(file2)
            df2_np = df2.to_numpy() 
            
            index = np.argwhere(annotation ==df_np[:,0])[0,0]
            #index2 = df2_np[-1]
            
            coordinates = df[['x_voxels','y_voxels','z_voxels']]
            coordinates = coordinates.iloc[index,:]
            
            coordinates2 = df2[['z_voxels']]
            index2 = np.size(coordinates2)
            index2= index2-1
            coordinates2 = coordinates2.iloc[index2,:]
            
            insert_data = {}
            insert_data['volume'] = csv_num
            insert_data['x_voxels'] = coordinates['x_voxels']
            insert_data['y_voxels'] = coordinates['y_voxels']
            insert_data['z_voxels'] = coordinates['z_voxels']
            insert_data['total_length'] = coordinates2['z_voxels']
            
            data[annotation].append(insert_data)

        except:
            pass   
    
    data_df = pd.DataFrame(data[annotation],columns=['volume','x_voxels','y_voxels','z_voxels','total_length'])
    data_df_np = data_df.to_numpy()
    data_df_np = data_df_np.astype(int)

#file path change below (variable = workbook) 
    workbook = xlsxwriter.Workbook(r'C:\Users\chawmm\Desktop\Worm_Untwisting\091521_RW10742\Pos5\For_Tracking\Reg_Sample\Decon_registered\annotation_check'+annotation+r'.xlsx')   
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})
    
    headings=['volume','x_voxels','y_voxels','z_voxels','total_length']
    worksheet.write_row('A1', headings, bold)    
    worksheet.write_column('A2', data_df_np[:,0])  
    worksheet.write_column('B2', data_df_np[:,1])  
    worksheet.write_column('C2', data_df_np[:,2])
    worksheet.write_column('D2', data_df_np[:,3])
    worksheet.write_column('E2',data_df_np[:,4])
    
    max_row = len(data_df_np)
    
    chart = workbook.add_chart({'type':'scatter','subtype':'straight_with_markers'})
    chart.add_series({
            'name':       ['Sheet1', 0, 1],
            'categories': ['Sheet1', 1, 0, max_row, 0],  
            'values':     ['Sheet1', 1, 1, max_row, 1],
            })
    chart.add_series({
            'name':       ['Sheet1', 0, 2],
            'categories': ['Sheet1', 1, 0, max_row, 0],  
            'values':     ['Sheet1', 1, 2, max_row, 2], 
            })  
    chart.add_series({
             'name':       ['Sheet1', 0, 3],
             'categories': ['Sheet1', 1, 0, max_row, 0],  
             'values':     ['Sheet1', 1, 3, max_row, 3], 
            })  
    chart.add_series({
             'name':       ['Sheet1', 0, 4],
             'categories': ['Sheet1', 1, 0, max_row, 0],  
             'values':     ['Sheet1', 1, 4, max_row, 4], 
            })
    chart.set_title({'name': ''+annotation+r'.csv'})
    worksheet.insert_chart('F2', chart)
    workbook.close()

    volume = data_df_np[:,0]
    x_voxel = data_df_np[:,1]
    y_voxel = data_df_np[:,2]
    z_voxel = data_df_np[:,3]
    total_length = data_df_np[:,4]

        
    #for loop implementation of hampel filter
    def hampel_filter(input_series, window_size, n_sigmas=3):
        n = len(input_series)
        new_series = input_series.copy()
        k = 1.4826 # scale factor for Gaussian distribution
        indices = []
        # possibly use np.nanmedian 
        for i in range((window_size),(n - window_size)):
            x0 = np.median(input_series[(i - window_size):(i + window_size)])
            S0 = k * np.median(np.abs(input_series[(i - window_size):(i + window_size)] - x0))
            if (np.abs(input_series[i] - x0) > n_sigmas * S0):
                new_series[i] = x0
                indices.append(i)
        return new_series, indices
        
    x_res, x_outliers = hampel_filter(x_voxel, window_size=10, n_sigmas=2.2)
    y_res, y_outliers = hampel_filter(y_voxel, window_size=10, n_sigmas=2.2)
    z_res, z_outliers = hampel_filter(z_voxel, window_size=10, n_sigmas=2.2)
    total_length_res, total_length_outliers = hampel_filter(total_length, window_size=10, n_sigmas=2.2)
    
    
    plt.plot(volume,x_voxel, color ="Red",label='x_voxels')
    plt.plot(volume,y_voxel, color="Green",label='y_voxels')
    plt.plot(volume,z_voxel, color="Blue",label='z_voxels')
    plt.plot(volume,total_length,color="Black",label='total_length')
    plt.title(annotation)
    plt.xlabel('volume')
    plt.ylabel('voxels')
    plt.legend(loc ='upper left')
    plt.show()
    
    print('x_outlier_volumes = ')
    print(x_outliers)
    print('y_outlier_volumes = ')
    print(y_outliers)
    print('z_outlier_volumes = ')
    print(z_outliers)
    print('total_length_outlier_volumes')
    print(total_length_outliers)
    print('common volumes')
    print(np.intersect1d(x_outliers,y_outliers,z_outliers))
print('')    
print('common volumes amoung all annotations')
print(np.intersect1d(x_outliers,y_outliers,z_outliers))
      