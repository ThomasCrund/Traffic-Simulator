from intersection import Road, Intersection, Light_Phase, Sensor
from typing import List
from LightColour import Light_Colour
from car import Car
import sys

def main():
    roads, sensors, intersection = setup_intersection()

    if len(sys.argv) < 2:
        print("ERROR: No File Provided")
    print("Open:", sys.argv[1])
    f = open(sys.argv[1], "r")
    if f.closed:
        print("ERROR: File open failed")
    output_file_name = sys.argv[1][:-len('.csv')] + "_output.csv"
    output = open(output_file_name, "w")
    if output.closed:
        print("ERROR: Output File open failed: " + output_file_name)
    output.write(get_header_row(4, roads) + "\n")
    for line in f:
        line_data = run_file_line(line, intersection)
        if line_data == None: continue
        sensor_data, time_stamp = line_data
        output_line = get_line_data(sensor_data, time_stamp, roads, sensors, intersection, False)
        print(get_line_data(sensor_data, time_stamp, roads, sensors, intersection))
        output.write(output_line + "\n")

    f.close()
    final_info = get_final_stats(intersection)
    output.write("\n\nCalculated Data,\n")
    for key in final_info:
        output.write(str(key) + "," + str(final_info[key]) + ",\n")
    print(final_info)
    output.close()


def run_file_line(line: str, intersection: Intersection):
    columns = line.split(',')
    try:
        time_stamp = int(columns[0])
    except ValueError:
        return None
    
    sensor_data: List[bool] = []
    for i in range(1, 5):
        sensor_data.append(bool(int(columns[i])))
    intersection.process_sensor_input(sensor_data, time_stamp)
    return (sensor_data, time_stamp)

def get_line_data(sensor_data, time_stamp, roads: List[Road], sensors: List[Sensor], intersection: Intersection, titles = True):
    # Time_stamp
    outputString = str(time_stamp) + ", "

    # sensor data
    for i in range(len(sensor_data)):
        if (titles): outputString += "sens" + str(i) + ": "
        if (sensor_data[i]): outputString += "1, "
        else: outputString += "0, "

    # road number of cars
    for road in roads:
        if (titles): outputString += "cars" + str(road.direction) + ": "
        outputString += str(len(road.current_cars)) + ", "
    
    # lights
    for road in roads:
        light = intersection.lights[road.direction]
        if (titles): outputString += "light" + str(road.direction) + ": "
        if (light == Light_Colour.RED): outputString += "RED, "
        if (light == Light_Colour.GREEN): outputString += "GRN, "
        if (light == Light_Colour.ORANGE): outputString += "ORN, "

    # phases
    if (titles): outputString += "current" + ": "
    outputString += intersection.current_phase.name + ", " 
    outputString += str(round(intersection.current_phase.getWeight(time_stamp), 1)) + ", "

    if (titles): outputString += "next" + ": "
    if (intersection.next_phase): outputString += intersection.next_phase.name + ", " + str(round(intersection.next_phase.getWeight(time_stamp), 1)) + ", "
    else: outputString += "None, 0, "

    return outputString

def get_header_row(sensor_num, roads: List[Road]):
     # Time_stamp
    outputString = "timestamp,"

    # sensor data
    for i in range(sensor_num):
        outputString += "sens" + str(i) + ","


    # road number of cars
    for road in roads:
        outputString += "cars" + str(road.direction) + ","

    
    # lights
    for road in roads:
        outputString += "light" + str(road.direction) + ","

    # phases
    outputString += "current_phase" + ",weight,"
    outputString += "next_phase" + ",weight,"

    return outputString
    

def get_final_stats(intersection: Intersection):
    finished_cars: List[Car] = []
    operating_cars: List[Car] = []
    final_info = {}
    for road in intersection.roads:
        finished_cars += road.past_cars
        operating_cars += road.current_cars
    final_info['num_cars_finished'] = len(finished_cars)
    final_info['num_cars_not_finished'] = len(operating_cars)
    sum_weight = 0.0
    for car in finished_cars:
        sum_weight += car.wait_time
    final_info['average_wait'] = sum_weight / len(finished_cars)
    return final_info

def setup_intersection():
    print("###Setup Intersection###")
    roads: List[Road] = []
    sensors: List[Sensor] = []
    for i in range(4):
        sensor = Sensor(num=i, time_to_intersection=6)
        road = Road(direction=i, sensors=[sensor])
        sensors.append(sensor)
        roads.append(road)
        print("\tDirection:", i, "initialised")

    phases: List[Light_Phase] = []
    phases.append(Light_Phase([roads[0], roads[2]], fixed_mode = True))
    phases.append(Light_Phase([roads[1], roads[3]], fixed_mode = True))

    intersection = Intersection(roads, phases)
    return (roads, sensors, intersection)


if __name__ == "__main__":
    main()