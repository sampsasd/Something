import numpy as np
import scipy.constants as cnst
from scipy.constants import physical_constants

#==============================================================================================

def meanFreePath(T, p, d=12E-10):
    return (1.380649E-23 * T) / (np.sqrt(2) * np.pi * d**2 * p)

def hartree(Ha: float):
    return Ha * 27.211386245981

def eVToHa(eV: float):
    return eV / 27.211386245981

def lambToE(lamb: float):
    return cnst.c * physical_constants['Planck constant in eV/Hz'][0] / lamb

def eToLmab(e: float):
    return cnst.c * physical_constants['Planck constant in eV/Hz'][0] / e

def hertzToThicc(deltaf: float):
    """returns surface density in ug/cm^2 and thickness in um"""
    return deltaf * 17.7e-9 * 10**6, deltaf * 17.7e-9 / 1.079 / 100 * 10**6

#================================================================================================0


#4.6.2024 thicc
print("4.6.2024 weird coating thickness", hertzToThicc((9.55e3 - 3.4175e3)))

print(eToLmab(2.95))
print(eToLmab(hartree(0.0869)))
print(eToLmab(3.06616662))

print("HOMO:", hartree(-0.198281364308048))
print(hartree(-0.0313867871193444))

print(eToLmab(2.979), eToLmab(5.445))

print(eToLmab(2.5495612))