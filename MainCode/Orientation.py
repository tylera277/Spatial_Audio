
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

        self.running = True



    def clean_up_orientation_vector(self, data):
        # I will clean up this disgrace of a parser eventually with something that looks more
        # professional

        chunks = data
        chunks = chunks.replace(",", "").replace("(", "").replace(")", "")

        try:
            chunks.split()[2]
            return chunks.split()
        except:
            return False


    def read(self, outputQueue):
        # Used for getting the orientation data from my Raspberry Pi Pico 
        # which is hooked up to the BNO055 sensor that gets the orientation data
        #time.sleep(0.001)
        while self.running:
            if self.ser.inWaiting:
                data = self.ser.readline().decode('utf-8').strip()
                #self.temp_storage = data
                #print(data)
                #print('----------')
                result = self.clean_up_orientation_vector(data)
                if (result == False):
                    #return self.temp_storage
                    #print(self.temp_storage)
                    outputQueue.put((self.temp_storage))
                else:
                    self.temp_storage = result
            #print(self.temp_storage)
            outputQueue.put((self.temp_storage))

            #print(self.temp_storage)
            #return self.temp_storage
        time.sleep(0.001)

    def stop(self):
        self.running = False
        self.ser.close()
    
    def getUserOrientation(self):
        pass