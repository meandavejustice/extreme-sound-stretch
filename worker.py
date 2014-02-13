import json
import os
import subprocess
import beanstalkc
from pydub import AudioSegment

q = beanstalkc.Connection(host='localhost', port=14711)

def stretch_it(job):
        """
        creates a subprocess and calls paulstretch_stereo.py
        with the proper args.
        assumes filepath is correct.
        """
        if job.body is not None:
            data = json.loads(job.body)

        filename_chunk = os.path.splitext(data['filename'])
        converted_track = AudioSegment.from_file(data['filename'],
                                                 filename_chunk[1][1:])
        wav_name = '%s.wav' % filename_chunk[0]
        finished_name = data['uniq_filename']
        converted_track.export(wav_name, format='wav')
        window = '--window=%f' % data['window']
        stretch = '--stretch=%f' % data['stretch']
        subprocess.call(["python", "./lib/paulstretch_stereo.py", window,
                         stretch, wav_name, finished_name])
        job.delete()

while True:
    item = q.reserve()
    stretch_it(item)
