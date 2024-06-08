

class SoundSource:

    def __init__(self, filename, positionOfSound):
        self.filename = filename
        self.positionOfSound = positionOfSound

    def get_fileName(self):
        return self.filename;

    def get_vector_position_of_sound(self):
        return self.positionOfSound

    def get_x_position_of_sound(self):
        return self.positionOfSound[0]
    def get_y_position_of_sound(self):
        return self.positionOfSound[1]
    def get_z_position_of_sound(self):
        return self.positionOfSound[2]
