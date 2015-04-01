# animatedicom - Visualise and Animate a DICOM data series
#
# Author: Iwan Cornelius <iwan@2mrd.com.au>
# Date:   1 April 2015

from mayavi import mlab
import vtk
from vtk.util import numpy_support
import os
import numpy as np
from matplotlib import pyplot, cm
import argparse

#process command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--dicomdir", type=str, default="./", help="The directory containing the dicom series (default:./)")
parser.add_argument("--output", type=str, default="./animation/", help="The generated animation output directory (default:./animation/)")
parser.add_argument("--animate", action="store_true", default=False, help="Animate camera rotation about the azimuthal axis and save images to output directory")
args = parser.parse_args()

#vtk is used to read in the DICOM data series. by default will look in current directory
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(args.dicomdir)
reader.Update()

#we create numpy arrays to store coordinates of each voxel, accounting for varying pixel size in each direction
#this won't work if the pixel spacing varies between slices
_extent = reader.GetDataExtent()
ConstPixelDims = [_extent[1]-_extent[0]+1, _extent[3]-_extent[2]+1, _extent[5]-_extent[4]+1]
ConstPixelSpacing = reader.GetPixelSpacing()
x = np.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
y = np.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
z = np.arange(0.0, (ConstPixelDims[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])
yv,xv,zv = np.meshgrid(y[1:],x[1:],z[1:])

#convert the DICOM data to a numpy array
imageData = reader.GetOutput()
pointData = imageData.GetPointData()
assert (pointData.GetNumberOfArrays()==1)
arrayData = pointData.GetArray(0)
ArrayDicom = numpy_support.vtk_to_numpy(arrayData)
ArrayDicom = ArrayDicom.reshape(ConstPixelDims, order='F')

finalwidth = 640
finalheight = 360

#plot using mayavi (mlab)
fig = mlab.figure(size=(finalwidth,finalheight), bgcolor=(1,1,1))
mlab.contour3d(xv,yv,zv,ArrayDicom,contours=4, transparent=True, colormap="Oranges")#can be changed to any matplotlib colormap

#if animate flag has been set, we create the output directory if it doesn't already exist
if args.animate is True:
    odir = args.output+"/png"
    if not os.path.exists(odir): os.makedirs(odir)
    #configure the number of frames required for 
    engine = mlab.get_engine()
    scene = engine.current_scene
    nframes = 100
    increment = np.float(360.0/nframes)
    mlab.view(0,0)#tweak these to set the starting angles of elevation and azimuth. if you run interactively, you can type mlab.view() to get current settings of the camera
    mlab.view(distance=600)
    mlab.view(focalpoint=(100,150,80))

    for i in np.arange(nframes):
        print("frame number ", i)
        scene.scene.camera.azimuth(increment)
        scene.scene.render()
        scene.scene.save_png(odir+"/anim"+np.str(i).zfill(2)+".png")

    print("run the following commands at the command line to create an animated gif and mp4 movie")
    print("cd ./animation/png/")
    #this will convert all images to gifs, and will also force the canvas to desired size, mayavi was exporting cropped image
    print("mogrify -format gif  -resize "+np.str(finalwidth)+"x"+np.str(finalheight)+"^ -gravity center -extent "+np.str(finalwidth)+"x"+np.str(finalheight)+"^ *.png") 
    print("cd ..")
    print("mkdir gif")
    print("cp png/*.gif ./gif/")
    print("cd gif/")
    #create the gif animation using ImageMagick
    print("convert -delay 1 -loop 0 anim*.gif final.gif")
    #convert animated gif to mp4 movie
    print("ffmpeg -i final.gif final.mp4")


