
import math

import numpy as np


class Math:

    def __init__(self):
        pass


    def ITD(self, distance_from_listener, speed_of_sound, angle_in_rad):

        time = abs(distance_from_listener/speed_of_sound * (angle_in_rad + math.sin(angle_in_rad)))

        return time

    def ILD(self, angle_in_rad):
        return math.cos(angle_in_rad)

    def roll_rotation(self, angle):
        rotation_matrix = np.array((1, 0,              0            ),
                                   (0, np.cos(angle), -np.sin(angle)),
                                   (0, np.sin(angle),  np.cos(angle)))

        return rotation_matrix
    
    def pitch_rotation(self, angle):
        rotation_matrix = np.array((np.cos(angle), 0, np.sin(angle)),
                                   (0, 1, 0),
                                   (-np.sin(angle), 0,  np.cos(angle)))

        return rotation_matrix

    def yaw_rotation(self, angle):
        rotation_matrix = np.array(((np.cos(angle), -np.sin(angle), 0),
                                   (np.sin(angle), np.cos(angle), 0),
                                   (0, 0,  1)))

        return rotation_matrix    

    def angle_compute(self, sound_position_vector, orientationVector, soundSourceNumber=1):

        #print("Beep: ", sound_position_vector, ": ", orientationVector)
        
        heading_orientation_vector_raw = np.array((0,1,0))

        
        yaw_angle = np.radians(float(orientationVector[0]))
        heading_orientation_vector_rotated = np.matmul(heading_orientation_vector_raw, self.yaw_rotation(yaw_angle))
        
        heading_angle = np.arctan2(heading_orientation_vector_rotated[0], heading_orientation_vector_rotated[1])
        sound_angle = np.arctan2(sound_position_vector[0,0], sound_position_vector[0,1])

        
        return (sound_angle-heading_angle)