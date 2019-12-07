import geopandas
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
cities = geopandas.read_file(geopandas.datasets.get_path('naturalearth_cities'))

pt_x, pt_y = np.asarray(boroughs["geometry"].x).reshape(-1,1), np.asarray(boroughs["geometry"].y).reshape(-1,1)
#pt_x, pt_y = np.asarray(cities["geometry"].x).reshape(-1,1), np.asarray(cities["geometry"].y).reshape(-1,1)

pts = np.concatenate((pt_x, pt_y), axis=1)



pts_df = pd.DataFrame(pts)
pts_df.to_csv("nyc_boroughs.txt", sep =" ", index=False, header=False)


fig, ax = plt.subplots()
ax.set_aspect('equal')
#world.plot(ax=ax, color='white', edgecolor='black')
#cities.plot(ax=ax, marker='o', color='red', markersize=5);
boroughs.plot(ax=ax, marker='o', color='red', markersize=5);
plt.show()
