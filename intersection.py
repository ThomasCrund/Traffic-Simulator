from typing import List
from enum import Enum
from car import Car

class Light_Colour(Enum):
  GREEN = 1
  ORANGE = 2
  RED = 3

class Sensor:
  def __init__(self, num: int, time_to_intersection: int, sensor_order_num = True):
    self.num = num
    self.time_to_intersection = time_to_intersection
    self.past_data = {}
    self.triggered = False
    self.sensor_order_num = sensor_order_num

  def update(self, triggered: bool, time_stamp: int):
    self.past_data[time_stamp] = triggered
    self.triggered = triggered

class Road:
  def __init__(self, direction: int, sensors: List[Sensor]):
    self.direction = direction
    self.sensors = sensors
    self.current_cars: List[Car] = []
    self.past_cars: List[Car] = []

  def update_sensors(self, sensors_data: List[bool], light: Light_Colour, time_stamp: int):
    for sensor in self.sensors:
      sensor.update(sensors_data[sensor.num])
      if (sensor.triggered and sensor.sensor_order_num == 1):
        car = Car(self.direction, time_stamp, light, sensor.time_to_intersection)
        self.current_cars.append(car)
      else:
        print("### Multiple Sensors Not Yet Implemented  ###")
        exit(1)
    
    for car in self.current_cars:
      if (light != Light_Colour.RED and time_stamp <= car.start_time + car.time_to_intersection):
        car.through_intersection = True
        self.past_cars = car
        self.current_cars.remove(car)

class Light_Phase:
  def __init__(self, roads: List[Road], min_green = 3, max_green = 150, orange_time = 3, red_time = 3):
    self.roads = roads
    self.orange_time = 3
    self.current_colour = Light_Colour.RED
    self.time_last_change = -3 # seconds 
    self.min_green = min_green
    self.max_green = max_green
    self.orange_time = orange_time
    self.red_time = red_time
    if (len(self.roads) == 0):
      self.orange_time = 0

  def getWeight(self):
    total_weight = 0.0
    for road in self.roads:
      for car in road.current_cars:
        total_weight += car.weight

  def setPhase(self, colour: Light_Colour, time_stamp: int):
    time_since_change = time_stamp - self.time_since_change
    if (colour == Light_Colour.GREEN and self.current_colour == Light_Colour.RED and time_since_change >= self.red_time):
      self.time_last_change = time_stamp
      self.current_colour = Light_Colour.GREEN
    elif (colour == Light_Colour.RED and self.current_colour == Light_Colour.GREEN and time_since_change >= self.min_green):
      self.time_last_change = time_stamp
      self.current_colour = Light_Colour.ORANGE
    elif (colour == Light_Colour.RED and self.current_colour == Light_Colour.ORANGE and time_since_change >= self.orange_time):
      self.time_last_change = time_stamp
      self.current_colour = Light_Colour.RED
    return self.current_colour
  
  

class Intersection:
  def __init__(self, roads: List[Road], phases: List[Light_Phase]):
    self.roads = roads
    self.lights = {}
    self.current_phase = Light_Phase([])
    for road in roads:
      self.lights[road.direction] = Light_Colour.RED
    self.phases = phases

  def process_sensor_input(self, sensors_data: List[bool], time_stamp: int):
    for road in self.roads:
      road.update_sensors(sensors_data, self.lights[road.direction], time_stamp)
    

  def change_phase(self):
    pass