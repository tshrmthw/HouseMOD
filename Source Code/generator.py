import sys
import getopt

from generate import *

def main(argv):
	room_type = 1
	sensor_file = ""
	label_file = ""
	generate_file = ""
	time_range = 900000 # fifteen minutes
	data_length = 100000

	try:
		opts, args = getopt.getopt(argv, "r:s:l:g:t:d:")
	except getopt.GetoptError, e:
		print e
		print 'generator.py -r <roomTypeInt> -s <sensorFilePath> -l <labelFilePath> -g <generateFilePath> -t <timeRangeMillis> -d <dataLength>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'generator.py -r <roomTypeInt> -s <sensorFilePath> -l <labelFilePath> -g <generateFilePath> -t <timeRangeMillis> -d <dataLength>'
			sys.exit(2)
		elif opt == '-r':
			room_type = int(arg)
		elif opt == '-s':
			sensor_file = arg
		elif opt == '-l':
			label_file = arg
		elif opt == '-g':
			generate_file = arg
		elif opt == '-t':
			time_range = int(arg)
		elif opt == '-d':
			data_length = int(arg)

	if sensor_file == '' or label_file == '' or generate_file == '':
		print 'generator.py -r <roomTypeInt> -s <sensorFilePath> -l <labelFilePath> -g <generateFilePath> -t <timeRangeMillis> -d <dataLength>'
		sys.exit(2)

	time_func = random_second_time_func
	bucket_func = double_sec_series_bucket_func
	label_func = boolean_label_func
	sensor_func = sum_sensor_data_func

	print 'Starting data generation...'
	generate = generate_labeled_data(room_type, label_file, sensor_file, generate_file)
	generate.generate(time_range, data_length, time_func, bucket_func, label_func, sensor_func)

if __name__ == "__main__":
	main(sys.argv[1:])