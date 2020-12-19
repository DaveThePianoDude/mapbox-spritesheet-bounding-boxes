RELEASE NOTES:

December 19, 2020

WARNING:  Code is JANKY!  Read this document first!!!

This code was written for a very narrow use case, with particular (or peculiar?) spacing required between sprites in the
sprite map in order for it to work.  It can be improved.

May 26, 2020

The nome branch of the project included the NOME sprite resources.  Please note following changes:

1. The file tlm-master-sprites.png was renamed to vtms-master-spritessheet.png
2. The vtms-master-spritesheet dimensions were enlarged to 3100 by 600 pixels.

February 18, 2020

David A. Holland

This python3 script lets you find bounding boxes in an image file for use in a mapbox map.  The script outputs the json required for the sprite sheet manifest file.  The script works by organically growing a set of bounding boxes for icons contained within an image, using a four-directional recursive search algorithm.

The script uses open CV version 2 for the image processing.

Usage:

./sprite-bb.py <inputFile> <outputFile> <iteration>

e.g., First you do a:

 ./sprite-bb.py vtms-master-spritesheet.png output.json 1

 THEN...

 ./sprite-bb.py vtms-master-spritesheet.png output.json 2

That first pass will write an intermediate file that begins with 'v-blue'.  You can delete this when you're done. :)

The program displays an image showing the result of the recursive search.  To dismiss the display, CLICK ON THE
IMAGE AND PRESS ANY KEY (LINUX OS).

You run the program twice, effectively running recursive search on the bounding boxes themselves after the first pass iteration.  The first pass generates a set of new bounding boxes in the cases where no single box was found for an icon.  In these cases, you will have multiple, possibly over-lapping bounding boxes that can be consolidates by running the script in a second pass.  


KNOWN ISSUES:

1. On some systems you may need to issue this command at the terminal command line: or, better yet, to your .bashrc file.

  export QT_X11_NO_MITSHM=1

  This avoids strange hardware errors such as "BadDrawable (invalid Pixmap or Window parameter)."

2. You may get a core dump if the boxes resulting from the first pass overlap too much across individual icons.  This

  code does not work well on icons spaced too closely together!
