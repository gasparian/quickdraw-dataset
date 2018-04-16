import numpy as np
from PIL import Image, ImageDraw
import cv2
import matplotlib.pyplot as plt

def dist(a, b):
    return np.power((np.power((a[0] - b[0]), 2) + np.power((a[1] - b[1]), 2)), 1./2)

def min_max(coords):
    x, y = [], []
    for i in range(len(coords)):
        x.append(int(min(coords[i][0]))); x.append(int(max(coords[i][0])))
        y.append(int(min(coords[i][1]))); y.append(int(max(coords[i][1])))
    return min(x), max(x), min(y), max(y)

def quickdraw_coords2img(image, dotSize=3, autoscale=(64,64), offset=5):
    image = np.array([[list(j) for j in i] for i in image])
    if autoscale:
        min_dists, dists = {}, [[] for i in range(len(image))]
        for i in range(len(image)):
            for j in range(len(image[i][0])):
                dists[i].append(dist([0, 0], [image[i][0][j], image[i][1][j]]))
            min_dists[min(dists[i])] = i

        min_dist = min(list(min_dists.keys()))
        min_index = min_dists[min_dist]
        start_point = [image[min_index][0][dists[min_index].index(min_dist)], image[min_index][1][dists[min_index].index(min_dist)]]
        for i in range(len(image)):
            for j in range(len(image[i][0])):
                image[i][0][j] = image[i][0][j] - start_point[0]
                image[i][1][j] = image[i][1][j] - start_point[1]

        min_x, max_x, min_y, max_y = min_max(image) 
        scaleX = ((max_x - min_x) / (autoscale[0]-(offset*2-1)))
        scaleY = ((max_y - min_y) / (autoscale[1]-(offset*2-1)))
        for i in range(len(image)):
            for j in range(len(image[i][0])):
                image[i][0][j] = image[i][0][j] / scaleX
                image[i][1][j] = image[i][1][j] / scaleY

    min_x, max_x, min_y, max_y = min_max(image)
    img = Image.new("RGB", (max_x-min_x+offset*2, max_y-min_y+offset*2), "white")
    draw = ImageDraw.Draw(img)

    for j in range(len(image)):
        for i in range(len(image[j][0]))[1:]:
            x, y = image[j][0][i-1], image[j][1][i-1]
            x_n, y_n = image[j][0][i], image[j][1][i]
            x -= min_x-offset; y -= min_y-offset
            x_n -= min_x-offset; y_n -= min_y-offset
            draw.line([(x,y), (x_n,y_n)], fill="black", width=dotSize)

    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.bitwise_not(img)

    if autoscale:
        return {'img':img, 'scaleX':scaleX, 'scaleY':scaleY, 'start_point': start_point}
    return {'img':img}