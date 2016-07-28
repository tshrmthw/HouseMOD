import random
import json

class parse_label_data(object):
	def __init__(self, filepath):
		self.filepath = filepath
		self.data = []
		self._data_from_file()

	def get_room_occupied(self, room_type, time_start, time_end):
		# if room was occupied more than half the time
		return self.get_room_occupied_likelihood(room_type, time_start, time_end) >= 0.5

	def get_room_occupied_rounded_likelihood(self, room_type, time_start, time_end):
		# only to first decimal place
		return round(self.get_room_occupied_likelihood(room_type, time_start, time_end), 1)

	def get_room_occupied_likelihood(self, room_type, time_start, time_end):
		previous_point = None
		found_start = False
		time_length = time_end - time_start
		time_in_room = 0

		for point in self.data:
			if point[2] >= time_end:
				subtract_time = time_end
				if not found_start and previous_point != None and previous_point[0] == room_type:
					subtract_time = time_start
				elif previous_point != None and previous_point[0] == room_type:
					subtract_time = previous_point[2]
				time_in_room += time_end - subtract_time

				break

			if not found_start:
				found_start = point[2] >= time_start
				if found_start and previous_point != None and previous_point[0] == room_type:
					time_in_room += point[2] - time_start
			else:
				if previous_point[0] == room_type:
					time_in_room += point[2] - previous_point[2]

			previous_point = point

		return float(time_in_room) / float(time_length)

	def get_constant_room_state_from_time(self, room_type, time_start):
		previous_point = None
		found_start = False
		room_occupied = False
		time_end = time_start

		for point in self.data:
			if not found_start:
				found_start = point[2] >= time_start
				if found_start:
					room_occupied = (previous_point != None and previous_point[0] == room_type) or (previous_point == None and point[0] == room_type)

			if found_start:
				if room_occupied != (point[0] == room_type):
					time_end = point[2]
					break

			previous_point = point

		return (room_occupied, time_start, time_end)


	def _data_from_file(self):
		with open(self.filepath, "r") as file:
			for line in file:
				parsed_json = json.loads(line)
				data_line = (parsed_json['type'], parsed_json['typeString'], parsed_json['time'])
				self.data.append(data_line)

class parse_sensor_data(object):
	def __init__(self, filepath):
		self.filepath = filepath
		self.data = []
		self.sensors = {}
		self._data_from_file()

	def get_sensor_occurences(self, time_start, time_end):
		previous_point = None
		start_point = None
		time_length = time_end - time_start
		sensor_sums = {}

		for key in self.sensors.keys():
			sensor_sums[key] = 0

		for point in self.data:
			if point[2] >= time_start and point[2] <= time_end:
				point_key = (point[0], point[1])
				value = sensor_sums.get(point_key, 0) + 1
				sensor_sums[point_key] = value

		occurences = []

		for key in sensor_sums.keys():
			value = sensor_sums[key]
			occurence = (key[0], key[1], value)
			occurences.append(occurence)

		return occurences

	def _data_from_file(self):
		with open(self.filepath, "r") as file:
			for line in file:
				parsed_json = json.loads(line)
				data_line = (parsed_json['id'], parsed_json['type'], parsed_json['date'])
				self.data.append(data_line)
				sensor_key = (data_line[0], data_line[1])
				value = self.sensors.get(sensor_key, 0) + 1
				self.sensors[sensor_key] = value

class parse_generated_data(object):
	def __init__(self, filepath):
		self.filepath = filepath
		self.data = []
		self._data_from_file()

	def test_train_split_data(self, test_perc):
		x_train, y_train, x_test, y_test = self.split_data(1 - test_perc)

		return x_train, y_train, x_test, y_test

	def split_data(self, prob):
		label_one = []
		label_two = []
		features_one = []
		features_two = []

		for row in self.data:
			if random.random() < prob:
				label_one.append(row['testLabel'])
				features_one.append(row['features'])
			else:
				label_two.append(row['testLabel'])
				features_two.append(row['features'])

		return features_one, label_one, features_two, label_two

	def get_data(self):
		labels = []
		features = []

		for row in self.data:
			labels.append(row['testLabel'])
			features.append(row['features'])

		return features, labels

	def get_most_common_data(self):
		labels = []
		features = []

		for row in self.data:
			labels.append(row['majRoomType'])
			features.append(row['features'])

		return features, labels

	def _data_from_file(self):
		with open(self.filepath, "r") as file:
			for line in file:
				if line:
					self.data.append(json.loads(line))

class parse_generated_varying_data(object):
	def __init__(self, filepath):
		self.filepath = filepath
		self.data = []
		self._data_from_file()

	def test_train_split_data(self, test_perc):
		x_train, y_train, x_test, y_test = self.split_data(1 - test_perc)

		return x_train, y_train, x_test, y_test

	def split_data(self, prob):
		label_one = []
		label_two = []
		features_one = []
		features_two = []

		for row in self.data:
			if random.random() < prob:
				label_one.append(row['y'])
				features_one.append(row['x'])
			else:
				label_two.append(row['y'])
				features_two.append(row['x'])

		return features_one, label_one, features_two, label_two

	def get_data(self):
		labels = []
		features = []

		for row in self.data:
			labels.append(row['y'])
			features.append(row['x'])

		return features, labels

	def _data_from_file(self):
		with open(self.filepath, "r") as file:
			for line in file:
				if line:
					self.data.append(json.loads(line))

