#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  arabic_word_cloud.py
#  License: MIT
#  Source : https://github.com/amueller/word_cloud
#  Copyright 2025
#  
#  Modified by : Yassine M'rabet 
#  

"""
 Description: This script genrate Masked arabic wordcloud using a mask image
 ideally a silouhette, you can generate wordclouds in arbitrary shapes.
 
"""

# Import needed libraries 
# Use pip to install missing ones
from os import path, chdir
from wordcloud import WordCloud
from matplotlib import font_manager
from PIL import Image, ImageChops, ImageEnhance, ImageFilter
import numpy as np
import re

class ArabicWordCloud:
    def __init__(self, input_dir):
        """
        Initialize the ArabicWordCloud class with necessary parameters.

        :param input_dir: Root directory containing subdirectories: Fonts, Masks, Texts, and Outputs
        """
        self.input_dir = input_dir
        self.font_dir = path.join(input_dir, "Fonts")
        self.mask_dir = path.join(input_dir, "Masks")
        self.text_dir = path.join(input_dir, "Texts")
        self.output_dir = path.join(input_dir, "Outputs")
        self.stopwords_file = path.join(input_dir, "stopwords.txt")  # Default stopwords file

    @staticmethod
    def remove_diacritics(text):
        """
        Removes Arabic diacritics from the given text.

        :param text: Input Arabic text
        :return: Text without diacritics
        """
        arabic_diacritics = re.compile(
            r"[\u064B-\u0652\u0670\u0671]"  # Arabic diacritic Unicode range
        )
        return re.sub(arabic_diacritics, "", text)

    @staticmethod
    def reduce_opacity(im, opacity):
        """
        Returns an image with reduced opacity.
        
        :param im: Input image
        :param opacity: Opacity level (0 to 1)
        :return: Image with reduced opacity
        """
        assert 0 <= opacity <= 1, "Opacity must be between 0 and 1"
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        else:
            im = im.copy()
        alpha = im.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        im.putalpha(alpha)
        return im

    def generate_word_cloud(
        self, 
        text_file, 
        font_file, 
        mask_file, 
        stopwords=None, 
        overlay_alpha=0.6, 
        overlay_mode=None, 
        blur_radius=1, 
        mask_opacity=0.2, 
        background_color="black",  # Default background color
        contour_color=None,       # Default contour color
        color_palette ="viridis",  # Default colormap
        export_format="png"       # Default export format
    ):
        """
        Generates and exports a word cloud based on the provided text and parameters.

        :param text_file: Name of the text file (in the Texts directory)
        :param font_file: Name of the font file (in the Fonts directory)
        :param mask_file: Name of the mask image file (in the Masks directory)
        :param stopwords: Optional set of stop words to filter out
        :param overlay_alpha: Alpha value for overlaying the mask image (default: 0.6)
        :param overlay_mode: Blend mode for overlaying the mask on the word cloud (default: None)
        :param blur_radius: Radius for Gaussian blur applied to the mask (default: 1)
        :param mask_opacity: Opacity for the mask overlay (default: 0.2)
        :param background_color: Background color for the word cloud (default: "black")
        :param contour_color: Contour color for the word cloud (default: None)
        :param color_palette : Colormap for the word cloud (default: "viridis")
        :param export_format: File format for exporting the word cloud (default: "png")
        """
        # Read and prepare the text
        text_path = path.join(self.text_dir, text_file)
        with open(text_path, encoding="utf-8") as file:
            text = file.read()

        # Remove diacritics from the text
        text = self.remove_diacritics(text)

        # Extract title from the text file name
        title_wc = path.splitext(path.basename(text_file))[0]
        print(f'Processing "{title_wc}" text, this may take a while, depending on your text length and complexity...')

        # Read the mask image
        mask_path = path.join(self.mask_dir, mask_file)
        mask = np.array(Image.open(mask_path))

        # Load stop words if a file exists and no set is provided
        if stopwords is None and path.exists(self.stopwords_file):
            with open(self.stopwords_file, encoding="utf-8") as sw_file:
                stopwords = set(sw_file.read().splitlines())

        # Configure WordCloud
        font_path = path.join(self.font_dir, font_file)
        wc = WordCloud(
            background_color=background_color,  # User-defined or default
            max_words=300,
            mask=mask,
            font_path=font_path,
            contour_width=2,
            contour_color=contour_color,  # User-defined or default
            colormap=color_palette,  # User-defined or default
            stopwords=stopwords,
        )

        # Generate the word cloud
        wc.generate(text)

        # Save the word cloud to a file
        output_file = path.join(self.output_dir, f'{title_wc}.{export_format}')
        if export_format == "svg":
            wc.to_svg(output_file)
        elif export_format == "png":
            wc.to_file(output_file)
        elif export_format == "pdf":
            wc.to_file(output_file)  # Matplotlib export can be used for PDF
        else:
            raise ValueError("Unsupported export format. Use 'png', 'svg', or 'pdf'.")

        print(f'Result exported to {output_file}')

        # Overlay the mask or original image on the word cloud if overlay_mode is specified
        if overlay_mode:
            wc_image = Image.open(output_file).convert("RGBA")
            mask_image = Image.open(mask_path).convert("RGBA").resize(wc_image.size)
            mask_image = self.reduce_opacity(mask_image, mask_opacity)
            mask_image = mask_image.filter(ImageFilter.GaussianBlur(blur_radius))

            if overlay_mode == "Difference":
                blended_image = ImageChops.difference(wc_image, mask_image)
            elif overlay_mode == "Add":
                blended_image = ImageChops.add(wc_image, mask_image)
            elif overlay_mode == "Subtract":
                blended_image = ImageChops.subtract(wc_image, mask_image)
            elif overlay_mode == "Multiply":
                blended_image = ImageChops.multiply(wc_image, mask_image)
            elif overlay_mode == "Screen":
                blended_image = ImageChops.screen(wc_image, mask_image)
            else:
                raise ValueError("Invalid overlay_mode. Supported modes: 'Difference', 'Add', 'Subtract', 'Multiply', 'Screen'.")

            # Save the final blended image
            blended_output_file = path.join(self.output_dir, f'{title_wc}_blended.png')
            blended_image.save(blended_output_file)
            print(f'Result exported to {blended_output_file}')



# Example usage 1
# wc = ArabicWordCloud("input_dir")
# wc.generate_word_cloud("example_text.txt", "example_font.ttf", "example_mask.png", overlay_alpha=0.6, overlay_mode="Difference")

# Example usage 2
# wc = ArabicWordCloud("input_dir")
# wc.generate_word_cloud("Ahmed_Shawqi_selected_poems.txt", "Bahij-Nazanin-Regular.ttf", "Ahmed_Shawqi.png", overlay_alpha=0.6, overlay_mode="Difference")

# Example usage 3
# wc = ArabicWordCloud("input_dir")
# wc.generate_word_cloud("Al-Atlal.txt", "Arslan.ttf", "Oum_Kalthoum.png", color_palette ="plasma", overlay_alpha=0.4, overlay_mode="Difference")

# Example usage 4
# wc = ArabicWordCloud("input_dir")
# wc.generate_word_cloud("1001_nights.txt", "Ruqaa.ttf", "arabian_nigths_2_mask.png", color_palette ="rainbow", contour_color= "#FFFDFC", export_format="svg")

# Example usage 5
# wc = ArabicWordCloud("input_dir")
# wc.generate_word_cloud("Ibn-yakdhan.txt", "KacstDecorative.ttf", "Ibn_Yaqdhan.png", color_palette ="hsv", contour_color= "white")

# # Example usage 6
# wc = ArabicWordCloud("input_dir")
# wc.generate_word_cloud("Canon_of_Medicine_extract.txt", "Nastaleeq.ttf", "Avicenna_mask.png", color_palette ="Dark2", contour_color= "#431600", background_color="#efefef")

