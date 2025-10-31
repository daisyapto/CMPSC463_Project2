import pickle
import os

if os.path.exists("/Users/andrewherman/CMP463/Project 2/Data/evacuation_graph.pkl"):
    with open("/Users/andrewherman/CMP463/Project 2/Data/evacuation_graph.pkl", "rb") as f:
        G = pickle.load(f)

if G:
    print(type(G))
