
import threading as td
import numpy as np
import networkx as nx
import time
import json
from Walker import generateCZML

from constellation import Constellation

class Coordinator():
    def __init__(self):
        self.constel = Constellation()
        with open('static/test.czml', 'r') as f:
            self.data = json.load(f)

    def build(self, planes, nodes, inclination, altitude):
        generateCZML(planes, nodes, inc = inclination, h=altitude)
        with open('static/test.czml', 'r') as f:
            self.data = json.load(f)

    def update(self, t):
        return self.data