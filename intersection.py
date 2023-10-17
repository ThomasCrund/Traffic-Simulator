from typing import List
from car import Car
from LightColour import Light_Colour
class Sensor:
  def __init__(self, num: int, time_to_intersection: int, sensor_order_num = 0):
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
      sensor.update(sensors_data[sensor.num], time_stamp)
      if (sensor.triggered and sensor.sensor_order_num == 0):
        car = Car(self.direction, time_stamp, light, sensor.time_to_intersection)
        self.current_cars.append(car)
      elif(sensor.sensor_order_num != 0):
        print("### Multiple Sensors Not Yet Implemented  ###")
        exit(1)
    
    for car in self.current_cars:
      car.update_weight(light, time_stamp)
      if (light != Light_Colour.RED and time_stamp >= car.start_time + car.time_to_intersection):
        car.through_intersection = True
        car.wait_time = time_stamp - (car.start_time + car.time_to_intersection)
        self.past_cars.append(car)
        self.current_cars.remove(car)


class Light_Phase:
  def __init__(self, roads: List[Road], min_green = 3, max_green = 150, orange_time = 3, red_time = 3, fixed_mode = False):
    self.roads = roads
    self.orange_time = 3
    self.current_colour = Light_Colour.RED
    self.time_last_change = -3 # seconds 
    self.min_green = min_green
    self.max_green = max_green
    self.orange_time = orange_time
    self.red_time = red_time
    self.name = "PH("
    self.fixed_mode  = fixed_mode
    for road in roads:
      self.name += str(road.direction) + " "
    self.name = self.name.strip()
    self.name += ")"
    if (len(self.roads) == 0):
      self.orange_time = 0

  def getWeight(self, time_stamp: int = 0):
    total_weight = 0.0
    if (time_stamp - self.time_last_change) > 30 and self.current_colour == Light_Colour.RED:
      total_weight += 0.1
    if not self.fixed_mode:
        for road in self.roads:
          for car in road.current_cars:
            total_weight += car.weight
    return total_weight

  def setPhase(self, colour: Light_Colour, time_stamp: int):
    time_since_change = time_stamp - self.time_last_change
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
  
  def needToEnd(self, time_stamp: int):
    if self.current_colour == Light_Colour.GREEN and (time_stamp - self.time_last_change) >= self.max_green:
      return True
    return False

class Intersection:
  def __init__(self, roads: List[Road], phases: List[Light_Phase]):
    self.roads = roads
    self.lights = {}
    self.current_phase = phases[0]
    self.current_phase.setPhase(Light_Colour.GREEN, time_stamp=0)
    self.next_phase = None
    for road in roads:
      self.lights[road.direction] = Light_Colour.RED
    self.phases = phases

  def process_sensor_input(self, sensors_data: List[bool], time_stamp: int):
    for road in self.roads:
      road.update_sensors(sensors_data, self.lights[road.direction], time_stamp)
    self.change_phase(time_stamp)
    self.change_lights()

  def change_phase(self, time_stamp: int):

    # find if a new phase is needed
    if self.next_phase == None:

      # Calculate the highest weighting phase
      highest_phase = None
      highest_weighting = 0
      for phase in self.phases:
        new_weight = phase.getWeight(time_stamp)
        if new_weight > highest_weighting:
          highest_weighting = new_weight
          highest_phase = phase
      
      # Set the next phase
      if highest_phase == self.current_phase:
        # Account for the current phase being the best
        if self.current_phase.needToEnd(time_stamp):
          # Switch phase when it reaches the max time
          highest_phase = None
          highest_weighting = -1
          for phase in self.phases:
            if phase.getWeight() > highest_weighting and phase != self.current_phase:
              highest_weighting = phase.getWeight()
              highest_phase = phase
          self.next_phase = highest_phase
        else:
          return
      elif highest_phase == None:
        return
      else:
        # Set the next phase
        self.next_phase = highest_phase

    # Change Phase
    if self.current_phase.setPhase(Light_Colour.RED, time_stamp) == Light_Colour.RED:
      # Current Phase is Red
      if (time_stamp - self.current_phase.time_last_change) >= self.current_phase.red_time:

        # Set new phase green
        if self.next_phase.setPhase(Light_Colour.GREEN, time_stamp) == Light_Colour.GREEN:
          self.current_phase = self.next_phase
          self.next_phase = None
    else:
      # Current Phase is Green or Orange, trying to make it Red once timers allow
      self.next_phase.setPhase

  def change_lights(self):
    for road in self.roads:
      if road in self.current_phase.roads:
        self.lights[road.direction] = self.current_phase.current_colour
      else:
        self.lights[road.direction] = Light_Colour.RED
    pass
