# KIDNEY SEGMENTATION PROJECT - main.py

# imports here
import os
from inspect import getsourcefile

import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

#==============================================================================
# PATHS
#path='Segmentation_Images'
vol = 1 #1 for VOL1, or 2 for VOL2
data_folder = 'ProjectData\\Rejestracja_02\\VOL_' + str(vol) #folder with the images (I think we should handle VOL1 and VOL2 separately)
output_folder = 'OutputData' #folder with the output images

current_file_dir = os.path.dirname(os.path.abspath(getsourcefile(lambda:0))) #find current file path
parent_dir = os.path.normpath(os.path.join(current_file_dir, "..")) # go up one level
data_path = os.path.join(parent_dir, data_folder) #absolute path to the data
output_path = os.path.join(parent_dir, output_folder)

os.chdir(current_file_dir)
import auxiliary_functions as aux
#==============================================================================

# plan zabawy AKA pseudocode:

#1. load the data

# load the mask
maskfname = 'Kidney_Mask_VOL' + str(vol) + '.nii'
KidneyMask = nib.load(os.path.join(output_path, maskfname)).get_data()
#KidneyMaskData = KidneyMask.get_data()


# load the registration data (4D = 3*spatial + 1*temporal)
for niifilename in sorted(os.listdir(data_path), key=len):
    if niifilename[:2] != '._':
        Loaded_File = nib.load(os.path.join(data_path, niifilename))
        Data_from_file = Loaded_File.get_data()
        print(niifilename)
        
        if 'KidneyData' not in locals():
            Data_shape = Data_from_file.shape
            KidneyData = Data_from_file.reshape(tuple([1L])+Data_shape)
        else:
            KidneyData = np.concatenate((KidneyData, Data_from_file.reshape(tuple([1L]+list(Data_shape)))), axis=0)
            # time at axis=0
print("'KidneyData' array shape: %s, size: %d" %(KidneyData.shape, KidneyData.size))

# impose the mask on the 4D image
KidneyMaskTile = np.tile(KidneyMask,(KidneyData.shape[0],1,1,1))
KidneyData = KidneyData * KidneyMaskTile

kidney_frozen_fig = aux.slicer(KidneyData[50,:,:,:], slideaxis=2, title='Kidney at 50s, coronal view')
kidney_fixedslice_fig = aux.slicer(KidneyData[:,:,:,21], slideaxis=0, title='Kidney at coronal slice 21 of 30')
# works after kernel is restarted x)


######################    TO BE REMOVED!    ##########################
#1a. (optional, only for demo - for faster computation):
# pick a smaller block within the volume to test the script on
# (ab. 1/5 - 1/4 in each of 3 spatial dimensions + full temporal?)
KidneyData = KidneyData[:,75:125,75:125,10:20]
print("Restricted 'KidneyData' array shape: %s, size: %d" %(KidneyData.shape, KidneyData.size))
######################################################################

#==============================================================================
#2. compute time course vector for each voxel
# (jesli to dziala tak, jak mysle)
# -> 4D = 3*spatial + 1*TCV-dimension


#3. reshape to 2D = 1*spatial + 1*TCV
# (-> 2D array of shape (number_of_voxels, length_of_TCV) )
# method? By 'flattennig' the first 3 dimensions to 1?


#4. K-Means
# -> k.means_labels - 1D array of length of 'number_of_voxels',
# filled with values: 0, 1, 2 - cluster indices for each voxel;
# plot the K-Means - scatter plot


#5. Find groups of voxels belonging to each cluster (0, 1, 2);
# plot averaged intensity changes for each group
# (3 lines on a common plot?)


#6. Find the 3D positions of the point groups
# in the original (3D) data;
# create ROIs - 3 separate 3D images (spatial only)
# and maybe an additional image - 3 colours of labels
# superimposed on the original image?
# Like with the brain in the 4th semester
CortexData = KidneyData
MedullaData = KidneyData
PelvisData = KidneyData

#==============================================================================
#7. save to Nifti
aff = Loaded_File.affine
Cortex_nifti = nib.Nifti1Image(CortexData, aff)
Medulla_nifti = nib.Nifti1Image(MedullaData, aff)
Pelvis_nifti = nib.Nifti1Image(PelvisData, aff)

fnameend = '_VOL' + str(vol) + '.nii'
os.chdir(output_path) #change the path to the output folder for saving
nib.save(Cortex_nifti, 'Cortex'+fnameend)
nib.save(Medulla_nifti, 'Medulla'+fnameend)
nib.save(Cortex_nifti, 'Pelvis'+fnameend)
print('ROIs saved to %s' %output_path)