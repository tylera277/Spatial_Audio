
import serial


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
        self.ser = serial.Serial("{}".format(self.port_of_pico_string), 115200, 8, "N", 1, timeout=.001)
        self.temp_storage = "(0, 0, 0)"


    def set_anchors(self):
        pass
    def clean_up(self, string):
        """{"Block":3948, "results":[{"Addr":"0x0001","St
        atus":"Ok","D_cm":71,"LPDoA_deg":0.00,"LAoA_deg":0.00,"LFoM":0,"
        RAoA_deg":0.00,"CFO_100ppm":622},{"Addr":"0x0002","Status":"Err"
        }]}"""

        


    def read(self):
        #line = self.ser.readline()
        #print("Line: ", line.decode("utf-8"))

        if self.ser.in_waiting:
            data = self.ser.readall().decode('utf-8')
            print(data)
            #print("----------")