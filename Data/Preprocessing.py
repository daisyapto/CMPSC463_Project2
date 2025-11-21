import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, Point


def preprocess_roads():
    roads = gpd.read_file("/Users/andrewherman/CMP463/SafetyGPS/Data/Raw Data/Street_Centerline.geojson")
    roads = roads.to_crs(26918)
    roads.to_file("/Users/andrewherman/CMP463/SafetyGPS/Data/Processed Data/Street_Centerline.geojson",
                  driver="GeoJSON")


def preprocess_floods():
    flood = gpd.read_file(
        "/Users/andrewherman/CMP463/SafetyGPS/Data/Raw Data/420757_20250718 7.09.00 PM/S_FLD_HAZ_AR.shp")
    flood = flood.to_crs(26918)
    flood.to_file("/Users/andrewherman/CMP463/SafetyGPS/Data/Processed Data/Floods.geojson", driver="GeoJSON")


def preprocess_evacuation_centers():
    facilities = gpd.read_file("/Users/andrewherman/CMP463/SafetyGPS/Data/Raw Data/City_Facilities_pub.geojson")
    evac_keywords = [
        "Recreation Center",
        "Recreation Building",
        "Recreation Other",

        "School and Grounds",

        "Library Branch",
        "Library Central",
        "Library Regional",
        "Library Specialized",
        "Library Operations",

        "Fire Station",
        "Fire Station Marine",
        "Police Station",
        "Police Sub-Station",
        "Police Operations\\Unit",

        "Older Adult Center",
        "Health Center",
        "Heatlh SubCenter",
    ]
    evac = facilities[facilities["ASSET_SUBT1_DESC"].isin(evac_keywords)]
    evac = evac.to_crs(26918)
    evac.to_file("/Users/andrewherman/CMP463/SafetyGPS/Data/Processed Data/Facilities.geojson", driver="GeoJSON")


def preprocess_hurricanes():
    df = pd.read_csv("/Users/andrewherman/CMP463/SafetyGPS/Data/Raw Data/ibtracs.NA.list.v04r01.csv",
                     keep_default_na=False,
                     low_memory=False,
                     skiprows=[1])
    df = df[df["BASIN"] == "NA"]

    # Drop rows missing coordinates
    df = df.dropna(subset=["LAT", "LON"])
    df["LAT"] = pd.to_numeric(df["LAT"], errors="coerce")
    df["LON"] = pd.to_numeric(df["LON"], errors="coerce")
    df = df.dropna(subset=["LAT", "LON"])

    gdf_hurricanes = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["LON"], df["LAT"]),
        crs=4326
    ).to_crs(26918)

    philly = Point(485888.6885861533, 4422509.200764658)
    buffer = philly.buffer(85_000)  # 85 km buffer

    gdf_hurricanes = gdf_hurricanes[gdf_hurricanes.geometry.within(buffer)]

    tracks = (
        gdf_hurricanes
        .sort_values(["SID", "ISO_TIME"])
        .groupby("SID")["geometry"]
        .apply(lambda g: LineString(g.tolist()) if len(g) > 1 else None)
    ).dropna()

    gdf_tracks = gpd.GeoDataFrame(
        {"SID": tracks.index, "geometry": tracks.values},
        crs="EPSG:26918"
    )
    gdf_tracks = gdf_tracks[gdf_tracks["SID"].str[:4].astype(int) >= 1900]

    print(len(gdf_tracks))
    print(gdf_tracks.head())

    gdf_tracks.to_file("/Users/andrewherman/CMP463/SafetyGPS/Data/Processed Data/Hurricanes.geojson", driver="GeoJSON")
