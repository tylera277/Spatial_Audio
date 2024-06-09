
import serial
import json

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
        self.ser = serial.Serial("{}".format(self.port_of_pico_string), 115200, 8, "N", 1)#, timeout=.001)
        self.temp_storage = "(0, 0, 0)"

        self.current_data = str()
        self.clear_status = False
        self.first_time = True

    def set_anchors(self):
        pass
    def sift_distance_value(self, string):
        """{"Block":3948, "results":[{"Addr":"0x0001","St
        atus":"Ok","D_cm":71,"LPDoA_deg":0.00,"LAoA_deg":0.00,"LFoM":0,"
        RAoA_deg":0.00,"CFO_100ppm":622},{"Addr":"0x0002","Status":"Err"
        }]}"""

        # One way of (eventually) getting the info I need (the distance value)
        #print(string.find("D_cm"))
        #print(string[58:72])
        
        string = string.replace(" ", "")
        
        dict_from_string = json.loads(string)
        #print(dict_from_string)
        


    def read(self):
        #line = self.ser.readline()
        #print("Line: ", line.decode("utf-8"))
        if self.clear_status == True:
            self.current_data = str()
            self.clear_status = False

        if self.ser.in_waiting:
            data = self.ser.readline().decode('utf-8')
            datas = data.split("\n")

            for i,  line in enumerate(datas):

                if line.strip() == "":
                    if self.first_time == False:
                        self.clear_status = True
                        self.current_data += str(line)
                        #return distance

            self.first_time = False
            

            #return data