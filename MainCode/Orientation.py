
import serial
import numpy as np
import time


class Orientation:
    """
    Class which will house all related materials used in determining a users
    orientation in space
    (Mainly interacting with the "Adafruit BNO055 Absolute Orientation Sensor" module
    that I will be using in order to get this information from/about the user)
    """
    def __init__(self, picoPortString):
        self.port_of_pico_string = picoPortString
        self.ser = serial.Serial("{}".format(self.port_of_pico_string), 9600, 8, "N", 1, timeout=.001)
        self.temp_storage = "(0, 0, 0)"




    def clean_up_orientation_vector(self, data):
        # I will clean up this disgrace of a parser eventually with something that looks more
        # professional

        chunks = data
        chunks = chunks.replace(",", "")
        chunks = chunks.replace("(", "")
        chunks = chunks.replace(")", "")

        try:
            chunks.split()[2]
            return chunks.split()
        except:
            return False


    def read(self):
        # Used for getting the orientation data from my Raspberry Pi Pico 
        # which is hooked up to the BNO055 sensor that gets the orientation data

        if self.ser.in_waiting:
            data = self.ser.readline().decode('utf-8').strip()
            #self.temp_storage = data

            result = self.clean_up_orientation_vector(data)
            if (result == False):
                return self.temp_storage
            else:
                self.temp_storage = result
        
        
        return self.temp_storage

    
    def getUserOrientation(self):
        pass