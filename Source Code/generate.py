import random
import json
from parse import *

class generate_labeled_data:
	def __init__(self, room_type, label_file, sensor_file, output_file):
		self.room_type = room_type
		self.label_data = parse_label_data(label_file)
		self.sensor_data = parse_sensor_data(sensor_file)
		self.output_file = output_file

	def generate(self, time_length, num_points, time_func, buckets_func, label_func, sensor_func):
		start_time = self.sensor_data.data[0][2]
		end_time = self.sensor_data.data[-1][2]
		counter = 0
		start_times = time_func(start_time, end_time, time_length, num_points)
		last_shown_percent = -1

		with open(self.output_file,"w") as file:
			while counter < num_points:
				label_feature = self._generate_label_feature(start_times[counter], time_length, buckets_func, label_func, sensor_func)
				json_line = json.dumps(label_feature) + "\n"
				file.write(json_line)
				counter += 1
				percent = 100 * float(counter) / float(num_points)

				if percent - last_shown_percent >= 1:
					print str(percent) + "% complete"
					last_shown_percent = percent

	def _generate_label_feature(self, time_from, time_length, buckets_func, label_func, sensor_func):
		time_to = time_from + time_length
		maj_room_type = majority_room_type_func(time_from, time_to, self.label_data)
		label = label_func(self.room_type, time_from, time_to, self.label_data)
		buckets = buckets_func(time_from, time_to)
		features = []

		for bucket in buckets:
			sensor = sensor_func(bucket[0], bucket[1], self.sensor_data)
			features.extend(sensor)

		return {'timeFrom' : time_from, 'timeTo' : time_to, 'features' : features, 'majRoomType' : maj_room_type, 'testRoomType' : self.room_type, 'testLabel' : label}

def random_millisecond_time_func(start_time, end_time, time_length, num_points):
	return random_inc_time_func(start_time, end_time, time_length, num_points, 1)

def random_second_time_func(start_time, end_time, time_length, num_points):
	return random_inc_time_func(start_time, end_time, time_length, num_points, 1000)

def random_minute_time_func(start_time, end_time, time_length, num_points):
	return random_inc_time_func(start_time, end_time, time_length, num_points, 60000)

def random_inc_time_func(start_time, end_time, time_length, num_points, inc):
	times = []

	for _ in range(0, num_points):
		rand_time = start_time + inc * random.randint(0, (end_time - start_time - time_length) / inc)
		times.append(rand_time)

	return times

def double_sec_series_bucket_func(time_from, time_to):
	return double_series_bucket_func(time_from, time_to, 1000)

def double_15sec_series_bucket_func(time_from, time_to):
	return double_series_bucket_func(time_from, time_to, 15000)

def double_30sec_series_bucket_func(time_from, time_to):
	return double_series_bucket_func(time_from, time_to, 30000)

def double_series_bucket_func(time_from, time_to, time_inc):
	current = time_from
	buckets = []

	while current + time_inc < time_to:
		bucket = (current, current + time_inc)
		buckets.append(bucket)
		current += time_inc
		time_inc *= 2

	f_bucket = (current, time_to)
	buckets.append(f_bucket)

	return buckets

def double_sec_parallel_bucket_func(time_from, time_to):
	return double_parallel_bucket_func(time_from, time_to, 1000)

def double_15sec_parallel_bucket_func(time_from, time_to):
	return double_parallel_bucket_func(time_from, time_to, 15000)

def double_30sec_parallel_bucket_func(time_from, time_to):
	return double_parallel_bucket_func(time_from, time_to, 30000)

def double_parallel_bucket_func(time_from, time_to, time_inc):
	buckets = []

	while time_from + time_inc < time_to:
		bucket = (time_from, time_from + time_inc)
		buckets.append(bucket)
		time_inc *= 2

	f_bucket = (time_from, time_to)
	buckets.append(f_bucket)

	return buckets

def majority_room_type_func(time_from, time_to, label_data):
	maj_time = 0
	maj_room_type = 0

	for room_type in range(1, 6):
		time = label_data.get_room_occupied_likelihood(room_type, time_from, time_to)
		if time > maj_time:
			maj_time = time
			maj_room_type = room_type

	return maj_room_type

def boolean_label_func(room_type, time_from, time_to, label_data):
	return int(label_data.get_room_occupied(room_type, time_from, time_to))

def single_decimal_label_func(room_type, time_from, time_to, label_data):
	return label_data.get_room_occupied_rounded_likelihood(room_type, time_from, time_to)

def exact_decimal_label_func(room_type, time_from, time_to, label_data):
	return label_data.get_room_occupied_likelihood(room_type, time_from, time_to)

def sum_sensor_data_func(time_from, time_to, sensor_data):
	occurences = sensor_data.get_sensor_occurences(time_from, time_to)

	return [occurence[2] for occurence in occurences]
