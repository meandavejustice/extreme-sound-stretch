clean:
				rm -f uploads/*

start:	clean
				beanstalkd -l 127.0.0.1 -p 14711 & \
				python worker.py & \
				python main.py
