#!/bin/env python
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
rmbimage.py - My image library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import subprocess as sp
import rmblogging
from rmblogging import debug, error
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from moviepy.editor import ImageSequenceClip

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def run_gegl(gegl_params):
    """
    Invoke the external gegl CLI process using the command line passed in from caller
    """

    gegl_full_command = ['gegl'] + gegl_params

    debug('')
    debug(f'Running gegl cli..')
    debug(f'{gegl_full_command = }')

    # Run the gegl command..

    try:
        completed_process = sp.run(gegl_full_command, timeout=300, check=True, capture_output=True, encoding="utf-8")

    except FileNotFoundError as e:
        error(f"Process failed because the executable could not be found.\n{e}")

    except sp.CalledProcessError as e:
        error(f"Process failed because did not return a successful return code. Returned {e.returncode}\n{e}")

    except sp.TimeoutExpired as e:
        error(f"Process timed out.\n{e}")

    debug(f"{completed_process = }")

    for line in completed_process.stdout:
        debug(f"{line[:188] = }")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def add_filename_to_image(input_filename, output_filename):
    """
    Writes the name of an image file in the top left corner of the image, using a small font.
    """

    debug(f'Adding filename {output_filename} to the top left corner..')

    x = y = 0
    font_name = 'kalimati.ttf'
    font_size = 8 
    color = (255, 255, 255)

    debug(f'{font_name = }')
    debug(f'{font_size = }')
    debug(f'{color = }')

    with Image.open(input_filename) as img:
        font = ImageFont.truetype(font_name, font_size)
        draw = ImageDraw.Draw(img)
        draw.text((x, y), f"[{output_filename}]", color, font=font)
        img.save(output_filename)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def image_sequence_to_mp4(clips_directory, fps, output_filename):
    """
    Uses moviepy.ImageSequenceClip to generate a single mp4 file from a sequence of images.

    Notes..

    • All images must be in a single directory.
    • There must not be anything other than the image sequence files in the sequence directory.
    • All images must be of the same dimension.

    """
    clip = ImageSequenceClip(clips_directory, fps=fps)
    clip.write_videofile(output_filename)

