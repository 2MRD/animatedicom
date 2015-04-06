# animatedicom
Visualise and animate a dicom data series

This simple python script allows you to create an interactive 3D visualisation of a DICOM series; moreover, it animates the scene with a camera rotation about the azimuth. 

It is aimed at medical physics students who work with DICOM for their research, and who are looking for an eye catching animation for a conference presentation, or are just interested in exploring their data in 3D. 

For further details on usage, please refer to the <a href="https://2mrd.com.au/blog">2MRD blog</a>.

### Usage
Use `animatedicom.py` to produce a series of frames as `.png` images.

    animatedicom.py [-h] [--dicomdir DICOMDIR] [--output OUTPUT] [--animate]
    optional arguments:
        -h, --help              show this help message and exit
        --dicomdir=DICOMDIR     The directory containing the dicom series (default:./)
        --output=OUTPUT         The generated animation output directory (default:./animation/)
        --animate               Animate camera rotation about the azimuthal axis and save images to output directory

The collection of frames can be rendered to a movie with the following steps:

    $> cd ./animation/png/
    $> mogrify -format gif  -resize <width>x<height>^ -gravity center -extent <width>x<height>^ *.png 
    $> cd .. 
    $> mkdir gif
    $> cp png/*.gif ./gif/"
    $> cd gif/

    # Create the gif animation using ImageMagick.                               
    $> convert -delay 1 -loop 0 anim*.gif final.gif

    # Convert the animated gif to mp4 movie.                                    
    $> ffmpeg -i final.gif final.mp4

