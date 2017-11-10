# -*- coding: utf-8 -*-
#auxiliary_functions

# all imports here
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

#==============================================================================

def show_slices(slices):
    """ Function to display row of image slices """
    fig, axes = plt.subplots(1, len(slices))
    for i, current_slice in enumerate(slices): #slice to też keyword
        axes[i].imshow(current_slice.T, cmap="gray", origin="lower")
    plt.suptitle("Center slices for EPI image")
        
        
#==============================================================================

def slicer(img, index0=14, title="Merged kindey mask"):  
    """Slider to show a 3D image.
    Input:
        - img - the image, 3D numpy array,
        - index0 (def. 14) - index of the initial slice to be shown (int),
        - title - plot suptitle (string)."""
        
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.subplots_adjust(bottom=0.2)
    
    current_slice = img[:,:,index0]
    im=ax.imshow(current_slice.T, cmap='gray', origin="lower")
    
    slidercolor = 'lightgoldenrodyellow'
    slideraxes = fig.add_axes([0.2, 0.1, 0.6, 0.05], axisbg = slidercolor)
    
    slider = Slider(slideraxes, 'Slice', 0, img.shape[2]-1, valinit=index0, valfmt='%d')
    
    plt.suptitle(title, fontsize=16)
    
    def update(val):
        current_slice = img[:,:,int(slider.val)]
        im.set_array(current_slice.T)
        fig.canvas.draw()
        
    slider.on_changed(update)
    plt.show()


#==============================================================================