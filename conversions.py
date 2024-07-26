import numpy as np
import scipy.constants as cnst
from scipy.constants import physical_constants

#==============================================================================================

def meanFreePath(T, p, d=12E-10):
    return (1.380649E-23 * T) / (np.sqrt(2) * np.pi * d**2 * p)

def HaToeV(Ha: float):
    return Ha * 27.211386245981

def eVToHa(eV: float):
    return eV / 27.211386245981

def lambToeV(lamb: float):
    return cnst.c * physical_constants['Planck constant in eV/Hz'][0] / lamb

def eVToLamb(e: float):
    return cnst.c * physical_constants['Planck constant in eV/Hz'][0] / e

def hertzToSDens(deltaf: float):
    """returns surface density in ug/cm^2 and thickness in um"""
    return deltaf * 17.7e-9 * 10**6, deltaf * 17.7e-9 / 1.079 / 100 * 10**6

def sDensToThicc(dens: float):
    """Give surface density in ug/cm^2, returns thickness in nm"""
    return dens * 1e-6 / (1.079 * 100) * 1e9

#================================================================================================0

def main():
    #4.6.2024 thicc
    print("4.6.2024 weird coating thickness", hertzToSDens((9.55e3 - 3.4175e3)))

    print(eVToLamb(2.95))
    print(eVToLamb(HaToeV(0.0869)))
    print(eVToLamb(3.06616662))

    print("HOMO:", HaToeV(-0.198281364308048))
    print(HaToeV(-0.0313867871193444))

    print(eVToLamb(2.979), eVToLamb(5.445))

    print(eVToLamb(2.5495612))

    print(sDensToThicc(4.96))

if __name__ == "__main__":
    main()