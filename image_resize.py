import os
import sys
import math
import argparse
from PIL import Image


def resize_image(image, width, height):
    return image.resize(size=(width, height))


def validate_args(args):
    if os.path.isfile(args.inputfile):
        inputfile = args.inputfile
    else:
        sys.exit("Image file doesn't exist")
    if args.outputdir and os.path.isdir(args.outputdir):
        outputdir = args.outputdir
    else:
        outputdir = None
    if any([args.width, args.height, args.scale]):
        if args.scale and not any([args.width, args.height]):
            scale = args.scale
            width, height = args.width, args.height
        elif (args.width or args.height) and not args.scale:
            scale = args.scale
            width, height = args.width, args.height
        else:
            sys.exit('Width and height parameters are not compatible with the scale')
    else:
        sys.exit('No parameters was provided for image resizing')
    return inputfile, outputdir, scale,  width, height


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


def get_new_image_size(image, scale, width, height):
    old_width, old_height = image.size
    if scale and not any([width, height]):
        new_width, new_height = int(old_width * scale), int(old_height * scale)
    elif width and height and not scale:
        new_width, new_height = width, height
        if not math.isclose(width / old_width, height / old_height, rel_tol=1e-5):
            print('New image has different scale')
    elif width and not scale:
        scale = width / old_width
        new_width, new_height = int(old_width * scale), int(old_height * scale)
    elif height and not scale:
        scale = height / old_height
        new_width, new_height = int(old_width * scale), int(old_height * scale)
    return new_width, new_height


def get_new_filename(old_filename, new_width, new_height):
    filename, extension = os.path.splitext(old_filename)
    new_filename = '{filename}__{new_width}x{new_height}{extension}'.format(
        filename=filename,
        new_width=new_width,
        new_height=new_height,
        extension=extension
    )
    return new_filename


if __name__ == '__main__':
    argparser = create_argparser()
    inputfile, outputdir, scale, width, height = validate_args(argparser)
    image = Image.open(inputfile)
    new_width, new_height = get_new_image_size(image, scale, width, height)
    resized_image = resize_image(image, new_width, new_height)
    old_filename = os.path.split(inputfile)[-1]
    new_filename = get_new_filename(old_filename, new_width, new_height)
    if outputdir:
        outputfile = os.path.join(outputdir, new_filename)
    else:
        old_dir, _ = os.path.split(inputfile)
        outputfile = os.path.join(old_dir, new_filename)
    resized_image.save(outputfile)
    print('Image is saved as {}'.format(outputfile))
