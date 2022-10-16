# THIS IS MY REALIZATION OF RRT ALGORITHM

import random
import math as m
from tkinter import *
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class Node:
    def __init__(self, id, coordinates, children):
        self.coordinates = coordinates
        self.children = children
        self.id = id

    def add_child(self, child):
        self.children.append(child)

    def child_with_id(self, id):
        for child in self.children:
            if child.id == id:
                return child
            if (res := child.child_with_id(id)) is not None:
                return res
        return None


def dist(node1, point):
    return m.sqrt((node1.coordinates[0] - point[0]) ** 2 + (node1.coordinates[1] - point[1]) ** 2)


def treeFindNearest(tree, point, min, nearestId, forbidden):
    if tree is None:
        return nearestId
    if not tree.children:
        return nearestId
    else:
        for child in tree.children:
            distance = dist(child, point)
            print('id = ', child.id, 'd = ', distance)
            if (distance < min) and (child.id not in forbidden):
                min = distance
                nearestId = child.id
                print("nearest id = ", nearestId)
    return treeFindNearest(tree.child_with_id(nearestId), point, min, nearestId, forbidden)


def visualize(tree):
    if tree is None:
        return 1
    canvas.create_oval(tree.coordinates[0]-2, tree.coordinates[1]-2, tree.coordinates[0]+2, tree.coordinates[1]+2, fill='black')
    if not tree.children:
        return 1
    else:
        for child in tree.children:
            canvas.create_line(tree.coordinates[0], tree.coordinates[1], child.coordinates[0], child.coordinates[1])
            visualize(child)


def build_clear_rrt(start_node):
    for i in range(n):
        lim = int(50 + i*0.25)
        random_point = [random.randint(-lim, lim), random.randint(-lim, lim)]
        print('point = ', random_point)
        nearestId = treeFindNearest(start_node, random_point, dist(start_node, random_point), 0)
        print('id = ', nearestId)
        nearestNode = start_node.child_with_id(nearestId)
        print(nearestNode)
        if nearestNode is None:
            start_node.add_child(Node(i + 1, random_point, []))
            print('point', random_point, ' ADDED as node with id = ', i+1, ' directly')
        else:
            nearestNode.add_child(Node(i+1, random_point, []))
            print('ADDED node with id = ', i+1, ' and coordinates = ', random_point)
    print('end')

def build_obstacle_rrt(start_node, obstacle_map):
    for i in range(n):
        lim = int(50 + i*(0.25*1000/n))
        random_point = [300 + random.randint(-lim, lim), 300 + random.randint(-lim, lim)]
        print('point = ', random_point)
        if obstacle_map[random_point[0], random_point[1]] == 1:
            print('point is in obstacle :(')
        else:
            forbidden_ids = []
            parentNotFound = True
            while parentNotFound:
                nearestId = treeFindNearest(start_node, random_point, dist(start_node, random_point), 0, forbidden_ids)
                print('id = ', nearestId)
                nearestNode = start_node.child_with_id(nearestId)
                print(nearestNode)
                if nearestNode is None:
                    if not is_line_in_obst(random_point, start_node.coordinates, obstacle_map):
                        start_node.add_child(Node(i + 1, random_point, []))
                        print('point', random_point, ' ADDED as node with id = ', i + 1, ' directly')
                        parentNotFound = False
                    else:
                        print('point ', random_point, ' will NOT be added directly because of collision')
                        forbidden_ids.append(0)
                        #canvas.create_oval(random_point[0] - 2, random_point[1] - 2, random_point[0] + 2,
                        #                   random_point[1] + 2, fill='red')
                        parentNotFound = False
                else:
                    if not is_line_in_obst(random_point, nearestNode.coordinates, obstacle_map):
                        nearestNode.add_child(Node(i + 1, random_point, []))
                        print('ADDED node with id = ', i + 1, ' and coordinates = ', random_point)
                        parentNotFound = False
                    else:
                        print('point will not be added to node with id ', nearestNode.id)
                        forbidden_ids.append(nearestId)
    print('end')

def build_obstacle_map(n, size):
    map = np.zeros((size, size))
    for i in range(n):
        x = random.randint(0, size - 50)
        y = random.randint(0, size - 50)
        print('OBSTACLE ', i, '   ', x, y)
        map[x:x+50, y:y+50] = 1
    return map

def visualize_map(map, canvas):
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i, j] == 1:
                canvas.create_rectangle((i, j) * 2)


def is_line_in_obst(point1, point2, obst_map):
    x1, y1, x2, y2 = point1[0], point1[1], point2[0], point2[1]
    if x1 == x2:
        for i in range(y1, y2):
            if obst_map[x1, i] == 1:
                return True
    if y1 == y2:
        for i in range(x1, x2):
            if obst_map[i, y1] == 1:
                return True
    if x1 != x2 and y1 != y2:
        for i in range(obst_map.shape[0]):
            for j in range(obst_map.shape[1]):
                if (abs((i - x1)/(x2 - x1) - (j - y1)/(y2 - y1)) < 0.01) and (min(x1, x2) < i < max(x1, x2)) and (min(y1, y2) < j < max(y1, y2)):
                    #canvas.create_rectangle((i, j) * 2, outline='blue')
                    if obst_map[i, j] == 1:
                        return True
    return False

start = Node(0, [300, 300], [])
goal = [200, 100]
n = 500
size = 600
root = Tk()
canvas = Canvas(root, width=size, height=size)
canvas.pack()
obs_map = build_obstacle_map(4, 600)
visualize_map(obs_map, canvas)
build_obstacle_rrt(start, obs_map)
visualize(start)
root.mainloop()
