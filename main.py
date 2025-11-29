import pickle
from shapely.geometry import Point
from Visualization.Full_Map import draw_full_map
from Algorithms.K_Nearest import k_nearest_evacuation_centers
from Algorithms.Prims import prim_mst
from flask import Flask, render_template, request, redirect, url_for

"""
References:
https://www.geeksforgeeks.org/python/flask-creating-first-simple-application/
https://flask.palletsprojects.com/en/stable/quickstart/#a-minimal-application
https://www.w3schools.com/html/html_forms.asp
https://www.w3schools.com/html/tryit.asp?filename=tryhtml_form_submit
Chat GPT-- Flask explanation
"""

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])

def main():
    with open("", "rb") as f: # Load hazard_graph.pkl with path
        graph = pickle.load(f)

    with open("", "rb") as f: # Load evac_kdtree.pkl with path
        tree, evacuation_coords, snapped_centers = pickle.load(f)

    #center_city = (-75.1575, 39.9509)
    if request.method == "POST":
        longitude = float(request.form.get("longitude"))
        latitude = float(request.form.get("latitude"))
        source = Point(longitude, latitude)

        # Random source
        # random_lat = random.uniform(39.95, 40.04)
        # random_lon = random.uniform(-75.05, -75.00)
        # source = Point(random_lon, random_lat)


        # K nearerst evacuation centers
        K = 8
        routes = k_nearest_evacuation_centers(graph, source, snapped_centers, K, tree)

        # Get MST edges
        mst_edges = prim_mst(evacuation_coords)

        print("Drawing full map...")
        draw_full_map(source, routes, mst_edges, save_file="") # full_map.html with path
        return redirect(url_for(render_template("full_map.html", longitude=longitude, latitude=latitude)))

    return render_template("input.html")

if __name__ == "__main__":
    app.run(debug=True)
