import sys
import getopt

from generate_varying import *

def main(argv):
	room_type = 1
	sensor_file = ""
	label_file = ""
	generate_file = ""
	data_length = 10000
	max_time_series = 200
	time_delta = 5000 # five seconds
	alpha = 0.0

	try:
		opts, args = getopt.getopt(argv, "r:s:l:g:t:d:a:m:")
	except getopt.GetoptError, e:
		print e
		print 'generator.py -r <roomTypeInt> -s <sensorFilePath> -l <labelFilePath> -g <generateFilePath> -d <dataLength> -m <maxTimeSeries> -t <timeDeltaMillis> -a <alpha>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'generator.py -r <roomTypeInt> -s <sensorFilePath> -l <labelFilePath> -g <generateFilePath> -d <dataLength> -m <maxTimeSeries> -t <timeDeltaMillis> -a <alpha>'
			sys.exit(2)
		elif opt == '-r':
			room_type = int(arg)
		elif opt == '-s':
			sensor_file = arg
		elif opt == '-l':
			label_file = arg
		elif opt == '-g':
			generate_file = arg
		elif opt == '-d':
			data_length = int(arg)
		elif opt == '-m':
			max_time_series = int(arg)
		elif opt == '-t':
			time_delta = int(arg)
		elif opt == '-a':
			alpha = float(arg)

	if sensor_file == '' or label_file == '' or generate_file == '':
		print 'generator.py -r <roomTypeInt> -s <sensorFilePath> -l <labelFilePath> -g <generateFilePath> -d <dataLength> -m <maxTimeSeries> -t <timeDeltaMillis> -a <alpha>'
		sys.exit(2)

	print 'Starting data generation...'
	generate = generate_varying_labeled_data(room_type, label_file, sensor_file, generate_file)
	generate.generate(data_length, max_time_series, time_delta, alpha)

if __name__ == "__main__":
	main(sys.argv[1:])