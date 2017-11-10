# -*- coding: cp1250 -*-
import os
from inspect import getsourcefile

import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

import auxiliary_functions as aux

#==============================================================================
# PATHS
#path='Segmentation_Images'
data_folder = 'ProjectData\\Segmentation_Images\\VOL1' #folder with the images (I think we should handle VOL1 and VOL2 separately)
output_folder = 'OutputData' #folder with the output images
current_file_dir = os.path.dirname(os.path.abspath(getsourcefile(lambda:0))) #find current file path
parent_dir = os.path.normpath(os.path.join(current_file_dir, "..")) # go up one level
data_path = os.path.join(parent_dir, data_folder) #absolute path to the data
output_path = os.path.join(parent_dir, output_folder)

#==============================================================================

for niifilename in os.listdir(data_path):

    Loaded_File = nib.load(os.path.join(data_path, niifilename))
    Data_from_file = Loaded_File.get_data()
    print(niifilename),
    print np.unique(Data_from_file),
    Data_max = np.max(np.abs(Data_from_file))
    if Data_max !=0: Data_from_file = Data_from_file / Data_max #normalisation - get rid of the 1 vs 222 problem
    print np.unique(Data_from_file)
    
    if 'Merged_Segmentation' not in locals():
        Data_shape = Data_from_file.shape
        Merged_Segmentation = np.zeros(Data_shape)
        
    """
    for index_x, data_1 in enumerate(Data_from_file):
        for index_y, data_2 in enumerate(data_1):
            for index_z,data_3 in enumerate(data_2):
                if Data_from_file[index_x,index_y,index_z] >= Merged_Segmentation[index_x,index_y,index_z]:
                    Merged_Segmentation[index_x, index_y, index_z] = Data_from_file[index_x,index_y,index_z]
    """
    
    #Merged_Segmentation = Merged_Segmentation + Data_from_file #shows overlaps, but in the end we should use the one below
    Merged_Segmentation = np.maximum(Merged_Segmentation, Data_from_file) #should do the same job as the triple loop

slice_0 = Merged_Segmentation[:, :, 7]
slice_1 = Merged_Segmentation[:, :, 14]
slice_2 = Merged_Segmentation[:, :, 21]
aux.show_slices([slice_0, slice_1, slice_2])

aux.slicer(Merged_Segmentation)


os.chdir(output_path) #change the path to the output folder for saving
#nib.save(Merged_Segmentation, 'Merged_Segmentation.nii') # z jakiegoś powodu nie działą :|
#Merged_Segmentation[Merged_Segmentation<1] = 0 #Kacper coś mówił, że czasem są 0-1, a czasem 0-255 zdjęcia # nope. Albo 0 i 1, albo 0 i 222. Nic pomiedzy.
#Merged_Segmentation[Merged_Segmentation>1] = 1
#nib.save(Merged_Segmentation, 'Merged_Segmentation_Processed.nii')