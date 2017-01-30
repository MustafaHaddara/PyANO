#!/usr/local/bin/python
# audio lib
import time

import pyo

SAMPLE_RATE = 44100
A4_KEY_NUM = 49

class AudioPlayer():
    def __init__(self):
        self.sounds = {}
        self.pyo_server = pyo.Server().boot().start()

    def get_sound_for(self, key_num):
        try: 
            # lazily construct this dict
            return self.sounds[key_num]
        except KeyError:
            semitone_diff = key_num - A4_KEY_NUM
            pitch_shift = 2**(semitone_diff/12.0)
            sound = pyo.SfPlayer('piano_A.wav', speed=[pitch_shift,pitch_shift], mul=0.5)
            self.sounds[key_num] = sound
            return sound

    def play_note(self, key):
        if key is None or (key.key_num in self.sounds and self.sounds[key.key_num].isPlaying()):
            return
        key.toggle_highlight()
        self.get_sound_for(key.key_num).out()


    def stop_note(self, key):
        if key is None:
            return
        key.toggle_highlight()
        self.get_sound_for(key.key_num).stop()

    def close(self):
        self.pyo_server.stop()
        # The server takes some time to stop
        # https://groups.google.com/d/msg/pyo-discuss/LdZR3MNIjq4/22Pc20hczLgJ
        time.sleep(1)  
        # and this way we don't crash when we shutdown
        self.pyo_server.shutdown()
