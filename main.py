# KIDNEY SEGMENTATION PROJECT - main.py
# plan zabawy AKA pseudocode:

#1. load the data (4D = 3*spatial + 1*temporal)


#1a. (optional, only for demo - for faster computation):
# pick a smaller block within the volume to test the script on
# (ab. 1/5 - 1/4 in each of 3 spatial dimensions + full temporal?)


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


#7. save to Nifti
