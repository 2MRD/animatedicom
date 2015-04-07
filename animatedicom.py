# animatedicom - Visualise and Animate a DICOM data series
#
# Author: Iwan Cornelius <iwan@2mrd.com.au>
# Date:   1 April 2015


import argparse
import os

import vtk
import tvtk

from mayavi import mlab


# Process command line arguments.
parser = argparse.ArgumentParser()

parser.add_argument("--dicomdir",
        type=str,
        default="./",
        help="The directory containing the dicom series (default:./)")

parser.add_argument("--output",
        type=str,
        default="./animation/",
        help="The generated animation output directory (default:./animation/)")

parser.add_argument("--animate",
        action="store_true",
        default=False,
        help="Animate camera rotation about the azimuthal axis and save each frame")

args = parser.parse_args()

# VTK is used to read in the DICOM data series. By default will look in
# the current directory.
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(args.dicomdir)
reader.Update()

# Convert the VTK object to a TVTK object. This is what mayavi uses.
data = tvtk.api.tvtk.to_tvtk(reader.GetOutput())

# Create our viewing window.
fig = mlab.figure(size=(640, 360), bgcolor=(1,1,1))

# Show the data by adding it to the pipeline, and using a
# matplotlib colour map name.
mlab.pipeline.contour_surface(data,contours=4, colormap="Oranges", opacity=0.75)

# Perform our rotation animation. 
if args.animate is True:

    # We create the output directory if it doesn't already exist.
    odir = os.path.join(args.output, "png")
    if not os.path.exists(odir): os.makedirs(odir)
   
    # Tweak these to values to set the starting angles of elevation and
    # azimuth. If you run interactively, you can type mlab.view(figure=fig) to get
    # current settings of the camera.
    mlab.view(40, 70, focalpoint=(86, 110, 30), distance=200, figure=fig)

    # Configure the number of frames we require.
    frames = 100
    increment = 360.0 / frames

    for i in range(frames):
        print("Rendering frame number: {0}".format(i))
        fig.scene.camera.azimuth(increment)
        fig.scene.render()
        
        # Save the current frame.
        filename = os.path.join(odir, "frame{:03}.png".format(i))
        fig.scene.save_png(filename)

# Allow interaction with the viewer.
#mlab.show()

