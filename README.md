February 18, 2020

David A. Holland

This python3 script lets you find bounding boxes in an image file for use in a mapbox map.  The script outputs the json required for the sprite sheet manifest file.  The script works by organically growing a set of bounding boxes for icons contained within an image, using a four-directional recursive search algorithm.

The script uses open CV version 2 for the image processing.

Usage:

./sprite-bb.py <inputFile> <outputFile>

e.g., ./sprite-bb.py tlm_master_legend_spritemap_2.png output.json

The program displays the result of the recursive search.  To dismiss the display, click on the image and press any key.

The program can be run twice, effectively running recursive search on the bounding boxes them selves, after the first pass iteration.  This will generate a set of new bounding boxes in the cases where no single box was found for an icon.  In these cases, you will have multiple, possibly over-lapping bounding boxes that can be consolidates by running the script in a second pass.  

Follow the steps in the comments to set up the first vs. second iteration logic.

NOTE:

On some systems you may need to issue this command at the terminal command line:

export QT_X11_NO_MITSHM=1

This avoids strange hardware errors such as "BadDrawable (invalid Pixmap or Window parameter)."
