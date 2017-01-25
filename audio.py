#!/usr/local/bin/python3

# audio lib

# audio manipulation freely adapted from https://github.com/Zulko/pianoputer

import numpy as np
import pygame
from scipy.io import wavfile

class AudioPlayer():
    def __init__(self):
        fps, self.A4Sound = wavfile.read("piano_A.wav")
        self.sounds = {49: pygame.sndarray.make_sound(self.speedx(self.A4Sound, 49))}
        self.playing = {49: False}

    # def manipulate_audio(self, key_num):
    #     # 440 Hz A4
    #     offset = key_num - 49
    #     pitch = 2 ** (offset/12.0)
    #     # TODO play A4 track sped up/slowed down to correct pitch

    def get_sound_for(self, key_num):
        try: 
            # lazily construct this dict
            return self.sounds[key_num]
        except KeyError:
            pitched_note = pygame.sndarray.make_sound(self.speedx(self.A4Sound, key_num))
            pitched_note.play()
            self.sounds[key_num] = pitched_note
            return pitched_note

    def play_note(self, key):
        if key is None or (key.key_num in self.playing and self.playing[key.key_num]):
            return
        key.toggle_highlight()
        self.playing[key.key_num] = True
        # print('playing %s' % key.key_num)  # placeholder
        self.get_sound_for(key.key_num).play(fade_ms=50)


    def stop_note(self, key):
        if key is None:
            return
        key.toggle_highlight()
        self.playing[key.key_num] = False
        # print('stopping %s' % key.key_num)  # placeholder
        self.get_sound_for(key.key_num).fadeout(50)


    def pitchshift(self, snd_array, key_num, window_size=2**13, h=2**11):
        """ Changes the pitch of a sound by ``n`` semitones. """
        factor = 2**((key_num-49) / 12.0)
        stretched = self.stretch(snd_array, factor, window_size, h)
        return self.speedx(stretched[window_size:], factor)

    def speedx(self, sound_array, factor):
        """ Multiplies the sound's speed by some `factor` """
        indices = np.round( np.arange(0, len(sound_array), factor) )
        indices = indices[indices < len(sound_array)].astype(int)
        return sound_array[ indices.astype(int) ]

    def stretch(self, sound_array, f, window_size, h):
        """ Stretches the sound by a factor `f` """

        phase  = np.zeros(window_size)
        hanning_window = np.hanning(window_size)
        result = np.zeros( len(sound_array)) # // f + window_size)

        for i in np.arange(0, len(sound_array)-(window_size+h), h*f):

            # two potentially overlapping subarrays
            a1 = sound_array[i: i + window_size]
            a2 = sound_array[i + h: i + window_size + h]

            # resynchronize the second array on the first
            s1 =  np.fft.fft(hanning_window * a1)
            s2 =  np.fft.fft(hanning_window * a2)
            phase = (phase + np.angle(s2/s1)) % 2*np.pi
            a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))

            # add to result
            i2 = int(i/f)
            result[i2 : i2 + window_size] += hanning_window*a2_rephased

        result = ((2**(16-4)) * result/result.max()) # normalize (16bit)

        return result.astype('int16')