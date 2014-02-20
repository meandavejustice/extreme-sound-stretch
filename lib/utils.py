import os
import subprocess
from pydub import AudioSegment


def convert_track(filename, wav_name):
    filename_chunk = os.path.splitext(filename)
    converted_track = AudioSegment.from_file(data['filename'],
                                                 filename_chunk[1][1:])
    converted_track.export(wav_name, format='wav')

def super_stretch(window=0.25, stretch=1.5, wav_name, finished_name):
    subprocess.call(["python", "./lib/paulstretch_stereo.py", window,
                         stretch, wav_name, finished_name])
