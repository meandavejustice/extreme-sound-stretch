# Extreme Sound Stretch Web

Stretch any audio to extreme lengths

utilizes [@paulNasca's](github.com/paulnasca) brilliant Stretching algorithm.

Currently uses the python port. [here](https://github.com/paulnasca/paulstretch_python)
Which is released under Public Domain, more info on Public Domain [here](http://www.gnu.org/licenses/license-list.html#PublicDomain)


## Development
* `apt-get install beanstalkd scipy numpy`
* `mkvirtualenv --system-site-packages extreme`
* `pip install -r requirements.txt`
* `beanstalkd -l 127.0.0.1 -p 14711 &`
* `python worker.py &`
* `python main.py`
* `open localhost:5000`

There are a couple of audio files you can play with in `/examples/`

## TODOS
* add download option.
* functionality to delete a song within half an hour.(cron job)
* add an audio analyzer to player
* get nginx serving static and downloads
* add bower for pure dependency(currently using the cdn)
* add drag n drop support for files
* remove jQuery (currently only being used for parsing file from form, which will be unneccessary after writing the drag n drop handler)
* add file viewer/player for recently uploaded files(similiar to [slskr](https://github.com/meandavejustice/slskr))
* create dockerfile
* deploy that bad boy
