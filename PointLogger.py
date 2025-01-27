import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from PIL import Image
import numpy as np
import argparse

AUTHOR = "the-z3ron3"
VERSION = 1.0

# ? Create argument parser
parser = argparse.ArgumentParser(
    prog="py PointLogger.py",
    description="Python program to extract pixel locations from an image and provides their coordinates in provided coordinate space.",
    add_help=False
)

# ? Add arguments
parser.add_argument(
    "-h", "--help", action="help", help="Show this help message and exit.",
)

parser.add_argument(
    "-i", metavar="<image>", dest="image", type=str, required=True, help="The name of image file."
)

parser.add_argument(
    "-r", nargs=4, metavar="<range>", default=[-1, +1, -1, +1], dest="range", type=int, help="The range of the image in the form of (-X +X -Y +Y). (-1 +1 -1 +1) is default value."
)

parser.add_argument(
    "-l", metavar="<filename>", dest="log", type=str, help="Write co-ordinates in given file."
)

parser.add_argument(
    "-ps", metavar="<size>", dest="pointSize", type=float, default=2.5, help="Size of red point which will be drawn on image. 2.5 is default value."
)

parser.add_argument(
    "-v", "--version", action="version", help="Show program's version number and exit.", version=f"PointLogger v{VERSION} by {AUTHOR}"
)

# ? Parse the arguments
args = parser.parse_args()

# ? Mouse move and Mouse click event handlers
def onMove(event):
    if (event.xdata != None) and (event.ydata != None):
        if ((event.inaxes) and (event.button == MouseButton.LEFT)):
            plt.plot(event.xdata, event.ydata, 'ro', markersize=MARKERSIZE)
            fig.canvas.draw_idle()  # redraw
            
            print(f"({event.xdata}, {event.ydata})")
            
            # ? Write points in log file
            if (args.log != None):
                logFile.write(f"({event.xdata}, {event.ydata})\n")

def onClick(event):
    if (event.xdata != None) and (event.ydata != None):
        if (event.button == MouseButton.LEFT):
            plt.plot(event.xdata, event.ydata, 'ro', markersize=MARKERSIZE)
            fig.canvas.draw_idle()  # redraw

            print(f"({event.xdata}, {event.ydata})")
            
            # ? Write points in log file
            if (args.log != None):
                logFile.write(f"({event.xdata}, {event.ydata})\n")

# ? Setup matplotlib window
fig = plt.gcf()
fig.canvas.manager.set_window_title("PointLogger")
np.set_printoptions(threshold=np.inf)

# ? Open and read image
image = Image.open(args.image)
data = np.asarray(image)    # store image in array

# ? Get width and height of image
# imageHeight = data.shape[0]
# imageWidth = data.shape[1]

# ? Set title, labels, and markersize
plt.title(image.filename)
plt.ylabel("Height (px)")
plt.xlabel("Width (px)")
MARKERSIZE = args.pointSize

# ? Connect with mouse move and mouse click event handlers
binding_id = plt.connect('motion_notify_event', onMove)
binding_id = plt.connect('button_press_event', onClick)

# ? Display image
# ? extend=(-X, +X, -Y, +Y)
show = plt.imshow(data, origin="upper", extent=tuple(args.range))

# ? Create log file
if (args.log != None):
    logFile = open(args.log, "w")

# ? Display matplotlib window
plt.show()

# ? Close log file handle
if (args.log != None):
    logFile.close()
