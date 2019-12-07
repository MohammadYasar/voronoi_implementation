import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
import numpy as np
from math import sqrt
from functools import reduce
import operator, math
import geopandas

BIG_FLOAT = 1e3

class plotVoronoi:
    def __init__(self, pts = None, polygons = None, triangles = None, vertices=None, lines=None, edges = None):
        self.vertices=vertices
        self.lines=lines
        self.edges=edges
        self.pts = pts
        self.polygons = polygons # a dict of site:[edges] pairs
        self.triangles = triangles # a dict of site:[edges] pairs

#edge 3-tuple: (line index, vertex 1 index, vertex 2 index)   if either vertex index is -1, the edge extends to infiinity

    def plotPoints(self):
        x = [pt.x for pt in self.pts]
        y = [pt.y for pt in self.pts]

        plt.scatter(x, y, color = 'r')
        plt.xlim(min(x)-20, max(x)+15)
        plt.ylim(min(y)-20, max(y)+15)

    def plotPolygon(self):
        vals = np.linspace(0,1,256)
        colors = ["red",  "green", "blue","cyan"]
        c= 0
        for polygon in self.polygons:
            np.random.shuffle(vals)
            cmap = plt.cm.colors.ListedColormap(plt.cm.jet(vals))
            #print  (cmap)
            edges = (self.polygons[polygon])
            x,y = self.plotEdges(edges, color_ = cmap)
            pts = np.concatenate((np.asarray(x).reshape(-1,1), np.asarray(y).reshape(-1,1)), axis=1)

            #print (x,y)
            coords = pts

            center = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), coords), [len(coords)] * 2))
            pts =(sorted(coords, key=lambda coord: (-135 - math.degrees(math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360))
            x_new , y_new = [], []

            for pt in pts:
                x_new.append(pt[0])
                y_new.append(pt[1])

            #plt.fill(x_new,y_new)#, colors[c])
            c+=1
        plt.show()
        #plt.savefig("geocities.png")

    def plotEdges(self, edges, color_):
        x_coor, y_coor, neg_edge, pos_edge =[], [], 0, 0

        for edge in edges:
            curr_line = self.lines[edge[0]]

            if curr_line[1] ==0:
                v1 = (self.vertices[edge[1]])
                v2 = (self.vertices[edge[2]])
                plt.vlines(curr_line[2], v1[1], v2[1])
                x_coor.append(v1)
                x_coor.append(v2)
                y_coor.append(curr_line[2])
                y_coor.append(curr_line[2])

            elif edge[1]==-1:

                v1 = -BIG_FLOAT
                v2 = self.vertices[edge[2]]
                x = np.linspace(v1, v2[0], 100)
                line = (curr_line[2] - curr_line[0]*x)/curr_line[1]
                p = plt.plot(x, line)

                x_coor.append(v1)
                y_coor.append((curr_line[2] - curr_line[0]*v1)/curr_line[1])

                if self.checkduplicates(x_coor, v2[0]):
                    x_coor.append(v2[0])
                    y_coor.append(v2[1])

            elif edge[2]==-1:

                v2 = BIG_FLOAT
                v1 = self.vertices[edge[1]]
                x = np.linspace(0 if v1[0]<0 else v1[0], v2, 100)
                x = np.linspace(v1[0], v2, 100)
                line = (curr_line[2] - curr_line[0]*x)/curr_line[1]
                p = plt.plot(x, line)

                if self.checkduplicates(x_coor, v1[0]):
                    x_coor.append(v1[0])
                    y_coor.append(v1[1])

                x_coor.append(v2)
                y_coor.append((curr_line[2] - curr_line[0]*v2)/curr_line[1])

            else:
                v1 = self.vertices[edge[1]]
                v2 = self.vertices[edge[2]]
                x = np.linspace(v1[0], v2[0], 100)
                line = (curr_line[2] - curr_line[0]*x)/curr_line[1]
                plt.plot(x, line)

                x_coor.append(v1[0])
                x_coor.append(v2[0])
                y_coor.append(v1[1])
                y_coor.append(v2[1])

        return (x_coor), (y_coor)



    def checkduplicates(self, vertices, vertex):
        for v in vertices:
            if abs(vertex-v)<=0.0001:
                return False
        return True

    def plotVertices(self):

        for edge in self.edges:
            curr_line = self.lines[edge[0]]
            if edge[1]==-1:
                v1 = -10
                v2 = self.vertices[edge[2]]
                x = np.linspace(v1, v2[0], 100)
                line = (curr_line[2] - curr_line[0]*x)/curr_line[1]
            elif edge[2]==-1:
                v2 = 100
                v1 = self.vertices[edge[2]]
                x = np.linspace(v1[0], v2, 100)
                line = (curr_line[2] - curr_line[0]*x)/curr_line[1]

            else:
                v1 = self.vertices[edge[1]]
                v2 = self.vertices[edge[2]]
                x = np.linspace(v1[0], v2[0], 100)

                line = (curr_line[2] - curr_line[0]*x)/curr_line[1]

                plt.plot(line)
        plt.show()

    def geoplot(self):
        world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
        cities = geopandas.read_file(geopandas.datasets.get_path('naturalearth_cities'))
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        world.plot(ax=ax, color='white', edgecolor='black')
        cities.plot(ax=ax, marker='o', color='red', markersize=5);
        plt.xlim(-200,200)
        plt.ylim(-200,200)

    def plotTriangles(self):
        x = [pt.x for pt in self.pts]
        y = [pt.y for pt in self.pts]

        for triangle in self.triangles:
            for i in range(len(triangle)):
                index_1 = (triangle[i])
                index_2 = (triangle[(i+1)%len(triangle)])

                plt.plot([x[index_1], x[index_2]], [y[index_1], y[index_2]])
        plt.savefig("figures/Delaunay_cities.png")
