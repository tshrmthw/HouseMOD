import random
import json
from parse import *

class generate_varying_labeled_data:
	def __init__(self, room_type, label_file, sensor_file, output_file):
		self.room_type = room_type
		self.label_data = parse_label_data(label_file)
		self.sensor_data = parse_sensor_data(sensor_file)
		self.output_file = output_file

	def generate(self, num_points=10000, max_time_series=200, time_delta=5000, alpha=0.001):
		start_time = max(self.sensor_data.data[0][2], self.label_data.data[0][2])
		end_time = min(self.sensor_data.data[-1][2], self.label_data.data[-1][2])

		counter = 0
		last_shown_percent = -1.0

		with open(self.output_file, 'w') as file:
			while counter < num_points:
				point_time = random.randint(start_time, end_time)
				time_series = []
				time_series_counter = 0
				point_occupied, point_start, point_end = self.label_data.get_constant_room_state_from_time(self.room_type, point_time)

				if point_start != point_end:
					for time_start in xrange(point_start, point_end, time_delta):
						time_series_counter += 1
						if time_series_counter > max_time_series:
							break
						new_time_series = [occurence[2] for occurence in self.sensor_data.get_sensor_occurences(time_start, time_start + time_delta - 1)]
						time_series.append(new_time_series)

					time_series_length = len(time_series)

					if time_series_length == max_time_series:
						feature_size = len(time_series[0])
						json_line = json.dumps({'y' : int(point_occupied), 'x' : time_series, 'x_size' : feature_size, 'x_length' : time_series_length, 'start' : point_start, 'end' : point_end, 'room_type' : self.room_type}) + "\n"
						file.write(json_line)
						counter += 1
						percent = 100.0 * float(counter) / float(num_points)

						if percent - last_shown_percent >= 1:
							print str(percent) + '% complete'
							last_shown_percent = percent

