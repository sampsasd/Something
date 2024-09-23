import numpy as np
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename, askopenfilenames

#FINAL PLOTS FOR GRADU
#direct uv current sweep with and without filter, uv current sweep, filtered sweep, 
#   angle distribution with and without filter, combined conversion dist
#blue angle distribution
#blue specular peak height as function of coating thickness (relative?)
#blue Riemann sum as function of coating thickness
#Riemann sum of combined conversion dist as a function of coating thickness


def readCurrentSweepData():
    """Returns dict with angle key and [currentList, powerList, stdList]"""
    pass

def readParamsData():
    """Returns dict with angle key and wls fit params"""
    pass

def readBlueData():
    """Returns [angleList, powerList, stdList]"""
    pass

def saveSum(sDensityList, sumList):
    """Saves Riemann sum as funnction of surface density to a csv"""
    pass

def readSum():
    """Returns thicknessList, sumList"""
    pass

#===============================================================================================0



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

def plotSumVsThick(thicknessList, sumList):
    """Plots Riemann sum as function of coating thickness"""
    pass



#============================================================================================================

def main():
    pass

if __name__ == '__main__':
    main()