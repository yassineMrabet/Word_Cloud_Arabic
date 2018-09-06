#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  arabic_word_cloud.py
#  Source : https://github.com/amueller/word_cloud
#  Copyright 2018
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

"""
 Description: This script genrate Masked arabic wordcloud using a mask image
 ideally a silouhette, you can generate wordclouds in arbitrary shapes.
"""

# Import needed libraries 
# Use pip to install missing ones
import os
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from wordcloud import WordCloud, STOPWORDS

d = path.dirname(__file__)


# Import bidi and arabic resphape
# pip install python-bidi
# 'arabic_reshaper'
# Source https://github.com/edx/edx-certificates/blob/master/arabic_reshaper.py
# and copy it in the current working directory

from bidi.algorithm import get_display
import arabic_reshaper

'''

Function arguments explanation : 
 text = text file, must be cleaned from common redundant words (prepositions, coordination etc.) 
 to get better result. Limits : diacritics are not supported
 # TODO corpus of common words to clean the text automatically
 path_to_font = indicate the path to the font to be used 
 # Tested with KacstOne fonts
 path_to_mask = indicate the path to the mask image (see the samples)
 output_image_dir = indicate the folder to export results  

'''
def generate_word_cloud(text, path_to_font, path_to_mask_image, output_image_dir):
	# Path to the desired font style
	# font_path = '/usr/share/fonts/truetype/kacst/KacstTitle.ttf'
	font_prop = font_manager.FontProperties(fname=path_to_font)
	
	# Read the text file
	txt = open(path.join(d, text)).read().decode('utf8')
	
	# Get the title for the output
	base=os.path.basename(text)
	title_wc=(os.path.splitext(base)[0])
	print('Processing "'+title_wc+'" text, this may take a while ..')
	
	# Reshape the text
	reshaped_text = arabic_reshaper.reshape(txt)
	artext = get_display(reshaped_text)
	
	# Read the mask image
	wc_mask = np.array(Image.open(path.join(d, path_to_mask_image)))
	
	# Set the word cloud parameters
	wc = WordCloud(background_color="black", 
	               max_words=1000, 
	               mask=wc_mask,
                   stopwords=STOPWORDS.add("said"), 
                   font_path=path_to_font,
                   contour_width=3, 
                   contour_color="white")
	# Generate word cloud
	wc.generate(artext)

	# Store to 'png' file
	os.chdir(output_image_dir)
	wc.to_file(path.join(d, ''+title_wc+'.png',))
	print ('Result exported to '+output_image_dir)



# Usage example
'''

Sample texts (cleaned) 
1001_nights.txt - One Thousand and One Nights, Part 1
Ibn-yakdhan.txt  - "Hayy ibn Yaqdhan" (Philosophical novel) 
Jaber.txt - "Jabir ibn Hayyan" alchemical text
Al-Atlal.txt - Lyrics of "Al-Atlal" song by "Oum Kalthoum"


Corresponding masks :
Scheherazade.png
Ibn_Yaqdhan.png
Jeber.png
Oum_Kalthoum.png

Suggested arguments for WordCloud() :
background_color='#050948ff'
contour_color='#f6f2b8ff'


'''
generate_word_cloud('/home/hpl1906/Documents/Arabic_word_cloud/Texts/Al-Atlal.txt',
                     '/usr/share/fonts/truetype/kacst/KacstPen.ttf',
                     '/home/hpl1906/Documents/Arabic_word_cloud/Masks/Oum_Kalthoum.png',
                     '/home/hpl1906/Documents/Arabic_word_cloud/Outputs/')


