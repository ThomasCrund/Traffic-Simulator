from intersection import Road, Intersection, Light_Phase, Sensor
from typing import List

def main():
    roads: List[Road] = []
    sensors: List[Sensor] = []
    for i in range(1,5):
        sensor = Sensor(num=i, time_to_intersection=6)
        road = Road(direction=i, sensors=[sensor])
        sensors.append(sensor)
        roads.append(road)
        
        print(i)

    



if __name__ == "__main__":
    main()