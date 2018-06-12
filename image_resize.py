import os
import sys
import argparse
from PIL import Image


def resize_image(inputfile, outputdir, width, height, scale):
    im = Image.open(inputfile)
    old_width, old_height = im.size
    old_filename, extension = os.path.split(inputfile)[-1].split('.')
    if scale and width is None and height is None:
        new_width, new_height = int(old_width * scale), int(old_height * scale)
    elif width and height and scale is None:
        new_width, new_height = width, height
        if width / old_width != height / old_height:
            print('New image has different scale')
    elif width and scale is None:
        scale = width / old_width
        new_width, new_height = int(old_width * scale), int(old_height * scale)
    elif height and scale is None:
        scale = height / old_height
        new_width, new_height = int(old_width * scale), int(old_height * scale)
    else:
        return None, None
    new_name = '{old_filename}__{new_width}x{new_height}.{extension}'.format(
        old_filename=old_filename,
        new_width=new_width,
        new_height=new_height,
        extension=extension
    )
    im = im.resize(size=(new_width, new_height))
    return im, new_name


def create_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--inputfile',
        help='full path to image file',
        required=True,
    )
    parser.add_argument(
        '--width',
        help='width of the image',
        type=int,
    )
    parser.add_argument(
        '--height',
        help='height of the image',
        type=int,
    )
    parser.add_argument(
        '--scale',
        help='scale of the image',
        type=float,
    )
    parser.add_argument(
        '--outputdir',
        help='full path to output directory',
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    argparser = create_argparser()
    kwargs = vars(argparser)
    if os.path.isfile(kwargs['inputfile']):
        resized_image, resized_image_name = resize_image(**kwargs)
    else:
        print("File doesn't exist!")
    if resized_image is None:
        sys.exit('Incorrect or no arguments provided')
    old_dir = os.path.split(kwargs['inputfile'])[0]
    outputdir = kwargs['outputdir']
    if kwargs['outputdir']:
        resized_image.save(os.path.join(outputdir, resized_image_name))
        print('Image is saved as {}'.format(
            os.path.join(
                outputdir,
                resized_image_name
            )
        ))
    else:
        resized_image.save(os.path.join(old_dir, resized_image_name))
        print('Image is saved as {}'.format(
            os.path.join(
                old_dir,
                resized_image_name
            )
        ))
