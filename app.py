from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Helper: find event by id
def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None

# GET /events - List all events so /events works in browser
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200

# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    
    new_id = max([e.id for e in events], default=0) + 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)
    
    return jsonify(new_event.to_dict()), 201 # Created

# PATCH /events/<id> - Update the title of an event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)
    
    if not event:
        return jsonify({"error": "Event not found"}), 404 # Not Found
    
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
        
    event.title = data["title"]
    return jsonify(event.to_dict()), 200 # OK

# DELETE /events/<id> - Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    
    if not event:
        return jsonify({"error": "Event not found"}), 404 # Not Found
    
    events.remove(event)
    return '', 204 # No Content

if __name__ == "__main__":
    app.run(debug=True)