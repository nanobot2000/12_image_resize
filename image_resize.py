import os
import math
import argparse
from PIL import Image


def resize_image(image, width, height):
    return image.resize(size=(width, height))


def validate_args(argparser):
    args = argparser.parse_args()
    if os.path.isfile(args.inputfile):
        inputfile = args.inputfile
    else:
        argparser.error("Image file doesn't exist")
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
            argparser.error('Incompatible arguments scale with width and height')
    else:
        argparser.error('No parameters was provided for image resizing')
    return inputfile, outputdir, scale, width, height


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
    return parser


def get_new_image_size(old_width, old_height, scale, width, height):
    if scale:
        new_width, new_height = int(old_width * scale), int(old_height * scale)
    elif width and height:
        new_width, new_height = width, height
    elif width:
        scale = width / old_width
        new_width, new_height = int(old_width * scale), int(old_height * scale)
    elif height:
        scale = height / old_height
        new_width, new_height = int(old_width * scale), int(old_height * scale)
    return new_width, new_height


def get_new_filename(inputfile, new_width, new_height):
    _, old_filename = os.path.split(inputfile)
    filename, extension = os.path.splitext(old_filename)
    new_filename = '{filename}__{new_width}x{new_height}{extension}'.format(
        filename=filename,
        new_width=new_width,
        new_height=new_height,
        extension=extension
    )
    return new_filename


def is_preserved_image_ratio(old_width, old_height, new_width, new_height):
    if not math.isclose(new_width / old_width, new_height / old_height, rel_tol=1e-5):
        print('New image has different ratio')


if __name__ == '__main__':
    argparser = create_argparser()
    inputfile, outputdir, scale, width, height = validate_args(argparser)
    image = Image.open(inputfile)
    old_width, old_height = image.size
    new_width, new_height = get_new_image_size(old_width, old_height, scale, width, height)
    is_preserved_image_ratio(old_width, old_height, new_width, new_height)
    resized_image = resize_image(image, new_width, new_height)
    new_filename = get_new_filename(inputfile, new_width, new_height)
    if outputdir:
        output_file_path = os.path.join(outputdir, new_filename)
    else:
        old_dir, _ = os.path.split(inputfile)
        output_file_path = os.path.join(old_dir, new_filename)
    resized_image.save(output_file_path)
    print('Image is saved as {}'.format(output_file_path))
