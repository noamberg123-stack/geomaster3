import random
from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'replit_secret'

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

LOCS = [
    {"n": "Eiffel Tower", "lat": 48.8584, "lon": 2.2945},
    {"n": "Statue of Liberty", "lat": 40.6892, "lon": -74.0445},
    {"n": "Pyramids", "lat": 29.9792, "lon": 31.1342},
]

@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
</head>
<body style="margin:0">
<div id="map" style="height:100vh"></div>

<script>
var socket = io();
var map = L.map('map').setView([20,0],2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

var target;

socket.emit("get");

socket.on("target", t => target = t);

map.on("click", e=>{
    let d = map.distance(e.latlng, L.latLng(target.lat,target.lon));
    alert("Distance: " + Math.round(d/1000) + " km");
    socket.emit("get");
});
</script>
</body>
</html>
""")

@socketio.on("get")
def get():
    emit("target", random.choice(LOCS))

socketio.run(app, host="0.0.0.0", port=3000)
