import logging
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import pandas as pd
from geovoronoi import coords_to_points, points_to_coords, voronoi_regions_from_coords
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area

logging.basicConfig(level=logging.INFO)
geovoronoi_log = logging.getLogger('geovoronoi')
geovoronoi_log.setLevel(logging.INFO)
geovoronoi_log.propagate = True


N_POINTS = 100
COUNTRY = 'Spain'

np.random.seed(123)

print('loading country `%s` from naturalearth_lowres' % COUNTRY)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
area = world[world.name == COUNTRY]
assert len(area) == 1

print('CRS:', area.crs)   # gives epsg:4326 -> WGS 84

area = area.to_crs(epsg=3395)    # convert to World Mercator CRS
area_shape = area.iloc[0].geometry   # get the Polygon

points = np.asarray(area_shape.exterior)


spain_pts = np.concatenate((np.asarray(points[:,0]).reshape(-1,1), np.asarray(points[:,1]).reshape(-1,1)), axis=1)
spain_pts_df = pd.DataFrame(spain_pts)
spain_pts_df.to_csv("spain.txt", sep =" ", index=False, header=False)
plt.scatter(points[:,0], points[:,1])
plt.show()
# generate some random points within the bounds
minx, miny, maxx, maxy = area_shape.bounds

randx = np.random.uniform(minx, maxx, N_POINTS)
randy = np.random.uniform(miny, maxy, N_POINTS)
coords = np.vstack((randx, randy)).T


pts = [p for p in coords_to_points(coords) if p.within(area_shape)]  # converts to shapely Point

print('will use %d of %d randomly generated points that are inside geographic area' % (len(pts), N_POINTS))
coords = points_to_coords(pts)   # convert back to simple NumPy coordinate array

del pts

#
# calculate the Voronoi regions, cut them with the geographic area shape and assign the points to them
#

poly_shapes, pts, poly_to_pt_assignments = voronoi_regions_from_coords(coords, area_shape)

#
# plotting
#

fig, ax = subplot_for_map()

plot_voronoi_polys_with_points_in_area(ax, area_shape, poly_shapes, coords, poly_to_pt_assignments)
#plot_voronoi_polys_with_points_in_area(ax, area_shape, poly_shapes, coords)   # monocolor

ax.set_title('%d random points and their Voronoi regions in %s' % (len(pts), COUNTRY))

plt.tight_layout()
plt.savefig('random_points_across_italy.png')
plt.show()


pts = np.concatenate((np.asarray(coords[:,0]).reshape(-1,1), np.asarray(coords[:,1]).reshape(-1,1)), axis=1)
pts_df = pd.DataFrame(pts)
pts_df.to_csv("random_numbers_3.txt", sep =" ", index=False, header=False)


pts_df = pd.DataFrame(pts)
