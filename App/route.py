from flask import Flask, request, render_template
from shapely.geometry import Point
from Algorithms.K_Nearest import k_nearest_evacuation_centers
from Algorithms.Prims import prim_mst
from Visualization.Flask_Fullmap import draw_flask_full_map
import pickle, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "Data", "Pickle")
app = Flask(__name__)

with open(os.path.join(DATA_DIR, "hazard_graph.pkl"), "rb") as f:
    graph = pickle.load(f)

with open(os.path.join(DATA_DIR, "evac_kdtree.pkl"), "rb") as f:
    tree, evacuation_coords, snapped_centers = pickle.load(f)


@app.route("/map")
def map_route():
    print("Fetching user input...")
    lat = float(request.args.get("lat"))
    lon = float(request.args.get("lon"))
    k = int(request.args.get("k"))
    print("User input successfully fetched")

    source = Point(lon, lat)

    # k nearest evacuation centers and their route
    print("Running KNN algorithm...")
    results = k_nearest_evacuation_centers(graph, source, snapped_centers, k, tree)

    # Run prims algorithm to get MST edges
    print("Running Prim's algorithm...")
    mst_edges = prim_mst(evacuation_coords)

    # Return full map
    print("Returning full map...")
    return draw_flask_full_map(source, results, mst_edges)


@app.route("/")
def index():
    print("Index route")
    return render_template("index.html")
