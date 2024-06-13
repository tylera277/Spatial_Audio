
import math
import pyaudio
import wave
import time

import numpy as np

from MainCode.SoundSource import SoundSource
from MainCode.Math import Math

class Sound:
    """ 
    Housing all of the sound related components to the project,
    including:
        - Placing sound sources at locations and specifying which files to play
        - Calculating users position relative to those sound sources
        - Adjusting volume level and for which channel the sounds go to
        - Outputting these final calculation results to the users specified earbuds/headphones
        - Doing all of it quick enough so as to not cause too much latency or in other words,
        for the sound not to be laggy and cause a poor/unpleasant experience.
    """

    def __init__(self, buffer_size, outputDevice):

        self.buffer_size = buffer_size
        self.outputDevice = outputDevice

        self.sound_source_1 = None
        self.sound_source_2 = None
        self.sound_source_3 = None

        self.SPEED_OF_SOUND = 343
        self.mix = np.zeros(2*self.buffer_size, dtype=np.int16)
        self.data_out = np.zeros(2*self.buffer_size, dtype=np.int16)
        self.left_channel_current_place = 0
        self.right_channel_current_place = 0

        # Will change amplitude of sound based on distance soon
        self.amp_left = 1
        self.amp_right = 1

        self.angle = 0
        self.total_delay_left = 0
        self.total_delay_right = 0
        self.frame_delay = 0
        
        self.wf = None
        self.stream_out = None
        
        self.whole_audio_data_left = None
        self.whole_audio_data_right = None
        

    def open_wave(self, soundSourceNumber):
        if soundSourceNumber == 1:
            self.wf = wave.open("{}".format(self.sound_source_1.get_fileName()), "rb")

    def open_stream(self):
        self.pa = pyaudio.PyAudio()
        
        self.stream_out = self.pa.open(
            rate=self.wf.getframerate(),
            channels=2,
            format=self.pa.get_format_from_width(self.wf.getsampwidth()),
            output=True,
            output_device_index=3,
            frames_per_buffer=self.buffer_size
        )

    def preload_waveforms(self):
        # Read the entire .wav file into memory once before the stream
        whole_audio_data_source1 = self.wf.readframes(self.wf.getnframes())
        print("Length: ", len(whole_audio_data_source1))

        # Convert the whole file into a workable numpy array
        whole_audio_data = np.frombuffer(whole_audio_data_source1, dtype=np.int16)

        # Splitting the interleaved file into each channel for (hopefully)
        # better independent control of each
        self.whole_audio_data_left = whole_audio_data[0::2]
        self.whole_audio_data_right = whole_audio_data[1::2]

    def preliminary_computes(self):
        self.open_wave(1)
        self.open_stream()
        self.preload_waveforms()

    def create_sound_source(self, sound_source_number, file_path, source_position_vector):

        # Only doing one sound at the moment
        if(sound_source_number == 1):
            self.sound_source_1 = SoundSource(file_path, source_position_vector)
        

   
    
    def compute(self, users_orientation_vector):
        start_time = time.time()
        angle = Math().angle_compute(self.sound_source_1.get_vector_position_of_sound(), users_orientation_vector)
        #print("ANGLE: ", np.degrees(angle))
        time_delay = Math().ITD(1, self.SPEED_OF_SOUND,  angle)

        frame_delay = int(time_delay * self.wf.getframerate())
        #print("FRAME DELAY: ", frame_delay)
        distance = np.linalg.norm(self.sound_source_1.get_vector_position_of_sound())
        amp_falloff_distance = 1/np.power(distance, 2)

        self.amp_left =1# amp_falloff_distance
        self.amp_right =1# amp_falloff_distance

        amp_diff = np.abs(Math().ILD(angle))
        print('---------------')
        print("Delay: ", frame_delay)
        direction_of_sound = angle
        if frame_delay != self.frame_delay:
            diff = frame_delay - self.frame_delay
            
            
            delay = np.zeros((abs(diff)))
            print("DIFF: ", diff, "ANGLE: ", np.degrees(angle))
            time.sleep(1)
        
            
            if (direction_of_sound >= 0) and (direction_of_sound < np.pi):
                if diff > 0:
                    self.total_delay_left += time_delay
                    self.whole_audio_data_left = np.insert(self.whole_audio_data_left, 0, delay, axis=0)
                    self.amp_left = (amp_diff * self.amp_right) + 0.1
                elif diff < 0:
                    self.total_delay_right += time_delay
                    self.whole_audio_data_right = np.insert(self.whole_audio_data_right, 0, delay, axis=0)
                    self.amp_right = (amp_diff * self.amp_left)


            elif (direction_of_sound < 0) and (direction_of_sound >= -np.pi):
                if diff > 0:
                    self.total_delay_right += frame_delay
                    self.whole_audio_data_right = np.insert(self.whole_audio_data_right, 0, delay, axis=0)
                    self.amp_right = (amp_diff * self.amp_left) + 0.1
                elif diff < 0:
                    self.total_delay_left += frame_delay
                    self.whole_audio_data_left = np.insert(self.whole_audio_data_left, 0, delay, axis=0)
                    self.amp_left = (amp_diff * self.amp_right) + 0.1
            else:
                print("PANIC!")
        #print("ENd time: ", time.time() - start_time)
        #print("Delays: ", self.total_delay_left/1E3, ", ", self.total_delay_right/1E3)
        self.frame_delay = frame_delay


    def output_formatting(self):
        # This needs to be at the end of the execution so it sends the right 
        # format to be played out on the speakers
        self.mix[0::2] = self.amp_left * self.whole_audio_data_left[self.left_channel_current_place:self.left_channel_current_place + self.buffer_size]
        self.mix[1::2] = self.amp_right * self.whole_audio_data_right[self.right_channel_current_place:self.right_channel_current_place + self.buffer_size]
        data_out = np.chararray.tobytes(self.mix.astype(np.int16))
        self.stream_out.write(data_out)

        # Moving the markers ahead by a full buffer size
        self.left_channel_current_place += self.buffer_size
        self.right_channel_current_place += self.buffer_size

    
    def output_sound_to_user(self, orientationVector):
        self.compute(orientationVector)        
        self.output_formatting()