from LightColour import Light_Colour

class Car:
  
  def __init__(self, direction_from: int, start_time: int, light: Light_Colour, time_to_intersection: float):
    self.dir = direction_from
    self.start_time = start_time
    self.weight = 0.0
    self.initial_light = light
    self.time_to_intersection = time_to_intersection
    self.update_weight(light, start_time)
    self.passed_sensors = 1
    self.through_intersection = False

  def update_weight(self, light: Light_Colour, current_time: int):
    if self.initial_light == Light_Colour.GREEN or self.initial_light == Light_Colour.ORANGE:
      self.weight = 2.0
    else:
      self.weight = 1.0
    
    if current_time >= self.start_time + self.time_to_intersection and light == Light_Colour.RED:
      self.weight += 0.2 * (current_time - self.start_time - self.time_to_intersection)

    return self.weight

  