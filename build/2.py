import random
import time

class Intersection:
    def _init_(self, name, green_time=30, yellow_time=5, red_time=30):
        self.name = name
        self.green_time = green_time
        self.yellow_time = yellow_time
        self.red_time = red_time
        self.traffic_count = {'North': 0, 'South': 0, 'East': 0, 'West': 0}
        self.current_light = 'Green'  # Default initial light
        self.current_direction = 'North'
    
    def update_traffic_count(self):
        # Simulate the traffic count for each direction
        for direction in self.traffic_count:
            self.traffic_count[direction] = random.randint(0, 50)  # Random traffic count for simulation
    
    def adjust_signal(self):
        # Dynamically adjust signal timings based on the traffic count
        max_direction = max(self.traffic_count, key=self.traffic_count.get)
        if self.traffic_count[max_direction] > 30:
            self.green_time = 40  # Increase green time for heavily trafficked direction
            self.red_time = 20   # Reduce red time for others
        else:
            self.green_time = 30
            self.red_time = 30
        
        # Change traffic light based on congestion
        if self.current_light == 'Green':
            print(f"{self.name} - {self.current_direction} is Green. Traffic count: {self.traffic_count[self.current_direction]}")
            time.sleep(self.green_time)
            self.current_light = 'Yellow'
        elif self.current_light == 'Yellow':
            print(f"{self.name} - {self.current_direction} is Yellow. Preparing to switch.")
            time.sleep(self.yellow_time)
            self.current_light = 'Red'
        else:
            print(f"{self.name} - {self.current_direction} is Red. Waiting for the next turn.")
            time.sleep(self.red_time)
            self.current_light = 'Green'
            # Switch direction for the next cycle
            directions = ['North', 'South', 'East', 'West']
            current_index = directions.index(self.current_direction)
            self.current_direction = directions[(current_index + 1) % len(directions)]
        
    def simulate_traffic(self, cycles=10):
        # Simulate the traffic management system for a number of cycles
        for _ in range(cycles):
            print(f"\n{'-'*30}\nCycle {_+1}")
            self.update_traffic_count()  # Simulate updated traffic data
            self.adjust_signal()  # Adjust traffic light based on current conditions


# Main program
if __name__ == "__main__":
    intersection = Intersection(name="Main Intersection")
    intersection.simulate_traffic(cycles=10)  # Simulate 10 traffic cycles
