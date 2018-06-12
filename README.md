# Image Resizer

Script resize your image with provided size or scale

# Quickstart

The script requires the installed Python interpreter version 3.6

You have to run the script with the `--inputfile` argument with path to image.

You can provide optional arguments:\
`--width` - desired width of new image;\
`--height` - desired height of new image;\
`--scale` - scale of new image in relation to the old image\
`--outputdir` - output directory of new image

To call the help, run the script with the `-h` or `--help` option.

```bash
$ python3 image_resize.py -h
usage: image_resize.py [-h] --inputfile INPUTFILE [--width WIDTH]
                       [--height HEIGHT] [--scale SCALE]
                       [--outputdir OUTPUTDIR]

optional arguments:
  -h, --help            show this help message and exit
  --inputfile INPUTFILE
                        full path to image file
  --width WIDTH         width of the image
  --height HEIGHT       height of the image
  --scale SCALE         scale of the image
  --outputdir OUTPUTDIR
                        full path to output directory
```

# Examples 

```bash
$ python3 image_resize.py --inputfile /home/parallels/img.jpg --height 250 --width 250
New image has different scale
Image is saved as /home/parallels/img__250x250.jpg
```

```bash
python3 image_resize.py --inputfile /home/parallels/img.jpg --scale 2 --outputdir /home/parallels/test/
Image is saved as /home/parallels/test/img__664x600.jpg
```
# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
