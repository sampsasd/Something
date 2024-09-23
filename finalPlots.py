import numpy as np
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename, askopenfilenames

#FINAL PLOTS FOR GRADU


def readCurrentSweepData():
    """Returns dict with angle key and [currentList, powerList, stdList]"""
    pass

def readParamsData():
    """Returns dict with angle key and wls fit params"""
    pass

def readBlueData():
    """Returns [angleList, powerList, stdList]"""
    pass



def plotCurrentsweepData(angle, currentList, powerList, filter = None, stdList = None):
    """Plots UV current sweep data with or without filter"""
    pass

def thirtySixtyCombineUV(paramsDict30, paramsDict60):
    """Completes conversion distribution using
    measurements with 30 and 60 degree incident angle.\n
    Returns full angle distribution."""
    pass

def plotAngleDistUV(paramsDict, incAng = None):
    pass

def plotAngleDistBLUE(angleList, powerList, stdList = None):
    pass

def riemannSum(distData):
    """Returns Riemann sum of distribution"""
    pass


def main():
    pass

if __name__ == '__main__':
    main()