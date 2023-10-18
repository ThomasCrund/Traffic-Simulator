from LightColour import Light_Colour

class Car:
  
  def __init__(self, direction_from: int, start_time: int, light: Light_Colour, time_to_intersection: float):
    self.dir = direction_from
    self.start_time = start_time
    self.weight = 0.0
    self.wait_time = 0
    self.initial_light = light
    self.time_to_intersection = time_to_intersection
    self.update_weight(light, start_time)
    self.passed_sensors = 1
    self.through_intersection = False
    self.wait_time = 0

  def update_weight(self, light: Light_Colour, current_time: int):
    if light == Light_Colour.GREEN or light == Light_Colour.ORANGE:
      self.weight = 2.0
    else:
      self.weight = 1.0
    
    if current_time >= self.start_time + self.time_to_intersection and light == Light_Colour.RED:
      self.wait_time = (current_time - self.start_time - self.time_to_intersection)

    self.weight += (0.2) * self.wait_time 

    return self.weight

  