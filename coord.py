import logging
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd

from geovoronoi import coords_to_points, points_to_coords, voronoi_regions_from_coords
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area

logging.basicConfig(level=logging.INFO)
geovoronoi_log = logging.getLogger('geovoronoi')
geovoronoi_log.setLevel(logging.INFO)
geovoronoi_log.propagate = True


N_POINTS = 100
COUNTRY = 'Italy'

np.random.seed(123)

print('loading country `%s` from naturalearth_lowres' % COUNTRY)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
area = world[world.name == COUNTRY]
assert len(area) == 1

print('CRS:', area.crs)   # gives epsg:4326 -> WGS 84

area = area.to_crs(epsg=3395)    # convert to World Mercator CRS
area_shape = area.iloc[0].geometry   # get the Polygon

# generate some random points within the bounds
minx, miny, maxx, maxy = area_shape.bounds

randx = np.random.uniform(minx, maxx, N_POINTS)
randy = np.random.uniform(miny, maxy, N_POINTS)
coords = np.vstack((randx, randy)).T

print(coords)
