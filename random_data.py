from intersection import Road, Intersection, Light_Phase, Sensor
from typing import List
from LightColour import Light_Colour
from car import Car
from traffic import setup_intersection, get_header_row, run_file_line, get_line_data, get_final_stats
import sys
import random
import os

def main():

    num_runs = int(sys.argv[1])
    vph = int(sys.argv[2])
    length = 1000
    if sys.argv[3]: length = int(sys.argv[3])

    if (not os.path.isdir("random_output")):
        os.mkdir('random_output')
    folder_dir = f'random_output/{vph}vph-L{length}-#{num_runs}_{random.randint(1,1000)}'
    os.mkdir(folder_dir)
    
    for run_num in range(num_runs):
        output_file_name = f'{folder_dir}/{run_num}.csv'
        run_output(output_file_name, vph, length)

def run_random_line(time_stamp: int, intersection: Intersection, vph):

    sensor_data: List[bool] = []
    for i in range(4):
        random_sensor_data = round(random.uniform(0.0, 1.0) + ((vph/3600)-0.5))
        sensor_data.append(random_sensor_data)
    intersection.process_sensor_input(sensor_data, time_stamp)
    return (sensor_data, time_stamp)

def run_output(output_file_name, vph, length):
    roads, sensors, intersection = setup_intersection(False)

    output = open(output_file_name, "w")
    if output.closed:
        print("ERROR: Output File open failed: " + output_file_name)
    output.write(get_header_row(4, roads) + "\n")
    for line in range(1, length+1):
        line_data = run_random_line(line, intersection, vph)
        if line_data == None: continue
        sensor_data, time_stamp = line_data
        output_line = get_line_data(sensor_data, time_stamp, roads, sensors, intersection, False)
        output.write(output_line + "\n")

    final_info = get_final_stats(intersection)
    output.write("\n\nCalculated Data,\n")
    for key in final_info:
        output.write(str(key) + "," + str(final_info[key]) + ",\n")
    print(output_file_name, final_info)
    output.close()

if __name__ == "__main__":
    main()