from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import time

# Initialize Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traffic_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# TrafficLight Model for storing state in the database
class TrafficLight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intersection_name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<TrafficLight {self.intersection_name} - {self.color}>"

# Initialize the database (run this once to create tables)
@app.before_first_request
def create_tables():
    db.create_all()

# Traffic light cycle durations (seconds)
CYCLE_TIMES = {
    'Red': 10,      # Time in seconds the light stays red
    'Green': 8,     # Time in seconds the light stays green
    'Yellow': 2     # Time in seconds the light stays yellow
}

# Initialize traffic light states
traffic_lights = {
    'Intersection1': 'Red',
    'Intersection2': 'Red',
    'Intersection3': 'Red',
}

# Helper function to change light color
def change_color(intersection_name):
    current_color = traffic_lights[intersection_name]
    if current_color == 'Red':
        traffic_lights[intersection_name] = 'Green'
    elif current_color == 'Green':
        traffic_lights[intersection_name] = 'Yellow'
    elif current_color == 'Yellow':
        traffic_lights[intersection_name] = 'Red'

    # Log the change in the database
    new_light = TrafficLight(intersection_name=intersection_name, color=traffic_lights[intersection_name])
    db.session.add(new_light)
    db.session.commit()

# API Endpoint to get the current state of traffic lights
@app.route('/api/traffic-lights', methods=['GET'])
def get_traffic_lights():
    """Returns the current state of all traffic lights"""
    return jsonify(traffic_lights)

# API Endpoint to change the state of a traffic light manually
@app.route('/api/traffic-lights/<intersection_name>/change', methods=['POST'])
def change_traffic_light(intersection_name):
    """Change the state of the given traffic light"""
    if intersection_name not in traffic_lights:
        return jsonify({'error': 'Intersection not found'}), 404
    change_color(intersection_name)
    return jsonify({intersection_name: traffic_lights[intersection_name]})

# API Endpoint to simulate a traffic light cycle for a given intersection
@app.route('/api/traffic-lights/<intersection_name>/cycle', methods=['POST'])
def cycle_traffic_light(intersection_name):
    """Simulate a cycle of the traffic light for a given intersection"""
    if intersection_name not in traffic_lights:
        return jsonify({'error': 'Intersection not found'}), 404

    # Simulate traffic light cycle
    for color, duration in CYCLE_TIMES.items():
        traffic_lights[intersection_name] = color
        # Log the state change to the database
        change_color(intersection_name)
        time.sleep(duration)  # Simulate time delay

    return jsonify({intersection_name: traffic_lights[intersection_name]})

# API Endpoint to get all traffic light logs (database)
@app.route('/api/traffic-logs', methods=['GET'])
def get_traffic_logs():
    """Returns all traffic light state logs"""
    logs = TrafficLight.query.all()
    log_data = [{"intersection": log.intersection_name, "color": log.color, "timestamp": log.timestamp} for log in logs]
    return jsonify(log_data)

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
