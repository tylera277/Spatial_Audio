
# Date: 11 May 2024
# Program: Central program where user will interact with backend components
#   (the composer/maestro to the programs symphony)

from MainCode.Orientation import Orientation
from MainCode.Sound import Sound
from MainCode.Position import Position

import numpy as np

import time
import threading
import queue

orientation_pico_port = "/dev/cu.usbmodem14101"
position_uwb_port_string = "/dev/cu.usbmodemC9513A4E085C1"
#desiredOutputDevice = 3


outputSound1 = "../../Sound_Sources/flowing_stream.wav"
positionOfSound1 = np.zeros((1,3))
positionOfSound1[0,1] = 2

outputSound2 = "../../Sound_Sources/chirping_birds.wav"
positionOfSound2 = np.zeros((1,3))
positionOfSound2[0,1] = -2


# Instantiate each classes object
o = Orientation(orientation_pico_port)
p = Position(position_uwb_port_string)
s1 = Sound(buffer_size=512, outputDevice=2)
s2 = Sound(buffer_size=512, outputDevice=2)

# Define where are the 3x UWB location anchors that are being used 
# (will be used for position data eventually)
""" 
Position.set_anchors(position1)
Position.set_anchors(position2)
Position.set_anchors(position3) 
"""

# Define which file names to play, the locations of the sound sources,
# and where the users location is w.r.t. the sounds

s1.create_sound_source(1, outputSound1, positionOfSound1)
s2.create_sound_source(1, outputSound2, positionOfSound2)
"""
Sound.create_sound_source(filename, positionVectorOfItsLocation) 
.
.
.
"""
# For taking in the 
positionQueue = queue.Queue()
orientationQueue = queue.Queue()

s1.preliminary_computes()
s2.preliminary_computes()

threads = []
t = threading.Thread(target=p.read, args=(positionQueue,))
t.daemon = True
t.start()

s = threading.Thread(target=o.read, args=(orientationQueue,))
s.daemon = True
s.start()


while True:

    print(orientationQueue.get())
    #print(positionQueue.get())
    print('------------')
# Start the programs tracking and adjusting audio levels based on it
#while True:
    #user_Orientation = np.array(o.read())
    #user_Position = p.read()
"""
    t = threading.Thread(target=o.read, args=(positionQueue,))
    t.daemon = True
    t.start()
    print(positionQueue.get())
"""

    #s = threading.Thread(target=p.read())
    #s.daemon = True
    #s.start()
    #s1.output_sound_to_user(user_Orientation) 
    #s2.output_sound_to_user(user_Orientation)
    
    
    
    #print("-----------------")
