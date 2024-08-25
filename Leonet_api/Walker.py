import math
from astropy import units as u
from astropy import time
from astropy.time import Time
from astropy.coordinates import CartesianRepresentation
from poliastro.frames import Planes
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
import numpy as np
import math
from poliastro.czml.extract_czml import CZMLExtractor


R_E = 6378
H_L = 1248  # LEO层轨道高度
EPOCH = time.Time("2022-04-12 04:00:00", scale="utc")  # UTC by default
LNUMP = 6  # LEO number of planes
LNUMS = 8  # LEO number of satellites in a plane

SLOTS = 1

def sat(h, ecc, inc, raan, argp, nu, ep):
    # six elements
    a = (R_E + h) * u.km
    ecc = ecc * u.one
    inc = inc * u.deg
    raan = raan * u.deg  
    argp = argp * u.deg  
    nu = nu * u.deg  
    orbit = Orbit.from_classical(Earth, a, ecc, inc, raan, argp, nu, epoch=ep) 
    return orbit


def constellation(num_plane, num_sat, F, h, ecc, inc, raan_0, argp, nu_0, ep):
    allsat = [[0 for i in range(num_sat)] for i in range(num_plane)]
    for i in range(num_plane):
        for j in range(num_sat):
            raan = raan_0 + i * 360 / num_plane
            nu = nu_0 + j * 360 / num_sat + i * 360 * F / (num_sat * num_plane)
            nu = nu % 360
            if nu >= 180:
                nu -= 360
            allsat[i][j] = sat(h, ecc, inc, raan, argp, nu, ep)
    return allsat

def generateCZML(num_plane, num_sat, F=1, h=500, ecc=0, inc=50, raan_0=0, argp=0, nu_0=0, ep=EPOCH):
    leosats_0 = constellation(num_plane, num_sat, F, h, ecc, inc, raan_0, argp, nu_0, ep)  # LEO walker constellation at time 0
    # time = 10 * u.min
    # print(leosats_0[0][0].r)  # xyz
    # neworbit = leosats_0[0][0].propagate(time)  # sat0_0 10-min propagation
    # print(neworbit.r)  # xyz

    tsat = leosats_0[0][0]
    start_epoch = tsat.epoch
    end_epoch = tsat.epoch + tsat.period
    N = 40

    extractor = CZMLExtractor(start_epoch, end_epoch, N)
    i = 0
    for p in leosats_0:
        for s in p:
            extractor.add_orbit(
                s,
                id_name="MolniyaOrbit"+str(i),
                path_width=2,
                label_text="Molniya",
                label_fill_color=[(125+i*5)%255, (30+i*10)%255, 120, 255],
            )
            i = i + 1

    with open('static/test.czml', "w+") as f_out:
        f_out.write(str(extractor.get_document()))

generateCZML(12, 20, 1, 500, 0, 50, 0, 0, 0, EPOCH)