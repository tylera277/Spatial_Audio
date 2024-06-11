
import serial
import json
import time


class Position:

    """
    Housing all of the position related components of the program, such as:
        - Creating the location of the UWB anchors that will be used in trilateration
        -
    """

    def __init__(self, picoPortString):


        anchor1_position = None
        anchor2_position = None
        anchor3_position = None

        
        self.port_of_pico_string = picoPortString
        self.ser = serial.Serial(port="{}".format(self.port_of_pico_string), baudrate=115200, bytesize=8, parity="N", stopbits=1)#, timeout=.001)
        self.temp_storage = "(0, 0, 0)"

        self.current_data = str()
        self.clear_status = False
        self.first_time = True
        self.distance_value = 0

    def set_anchors(self):
        pass
    def sift_distance_value(self, string):
        """ 
        Changing the raw value that comes printed from the UWB positioning
        module into something I can query for the main program to be able to use
        """

        # For some reason, putting the string into a multiline comment works 
        string = """{}""".format(self.current_data)

        # Convert the json string to a dictionary
        dict_from_string = json.loads(string)

        # Try to get the distance value from the dictionary, if its not there for some 
        # reason or if the formatting was messed up once, just return the previous value
        # it got and update it when its next possible
        newdict = dict(dict_from_string['results'][0])
        try:
            self.distance_value = newdict['D_cm']
            return self.distance_value
        except:
            return self.distance_value        


    def read(self, outputQueue):
        
        if self.clear_status == True:
            self.current_data = str()
            self.clear_status = False

        if self.ser.inWaiting:
            data = self.ser.readline().decode('utf-8')
            datas = data.split("\n")

            for i,  line in enumerate(datas):
                if self.first_time == False:
                    self.clear_status = True
                    self.current_data += str(line)

                if line.strip() == "":
                    if(self.first_time==False):
                        distance = self.sift_distance_value(self.current_data)
                        outputQueue.put((distance))
                        #return distance

        time.sleep(0.001)
        
        self.first_time = False
            