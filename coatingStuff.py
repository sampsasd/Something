import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#=============================FUNCTIONS==================================================================

def readDatData(fileName):
    """Returns (time, temperature, frequency, voltage)"""
    freq = []
    temp = []
    time = []
    volt = ['0']
    with open(fileName, 'r') as file:
        for row in file:
            rawRow = row.strip().split()
            freq.append(float(rawRow[3]))
            if not time:
                t_i = float(rawRow[2])
                time.append(0.)
            else:
                tMin = (float(rawRow[2]) - t_i) / 60
                time.append(tMin)
            temp.append(float(rawRow[5]))
            if len(rawRow) == 7:
                volt.append(rawRow[6])
        
    print("(time, temp, freq, volt)")
    return np.array(time), np.array(temp), np.array(freq), np.array(volt)

def deltaFreq(freq: np.ndarray):
    """Returns in kHz"""
    f_i = freq[0]
    f = [(point - f_i)*1E-3 for point in freq]
    return np.array(f)

def plotCoating(time: np.ndarray, temperature: np.ndarray, deltaf: np.ndarray, realtT: np.ndarray=None, tAndC: np.ndarray=None, V: np.ndarray=None, coup=0, volt=0, title: str=None, save: str=None):
    
    fig, ax = plt.subplots(1, 1)
    if title is not None:
        fig.suptitle(title)
    
    line1, = ax.plot(time, deltaf, color="mediumorchid", label="$\Delta f$")
    ax.set_xlabel("$t$ / min")
    ax.set_ylabel("$\Delta f$ / kHz")
    ax.yaxis.set_major_locator(ticker.MultipleLocator(base=0.1))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=30))
    ax.grid(linestyle="-")
    axa = ax.twinx()
    line2, = axa.plot(time, temperature, color="coral", label="$T$", lw=1, ls="-")
    axa.set_ylabel("$T$ / $^{\circ}$C")
    if realtT is not None:
        line3, = axa.plot(realtT[0], realtT[1], color="gold", label="$T_{\\mathrm{accurate}}$", ls="-")
        axa.legend(handles=[line1, line2, line3], loc="center left")
    else:
        axa.legend(handles=[line1, line2], loc="center left")
    plt.tight_layout()
    if save is not None:
        plt.savefig("./plots/" + save)
    plt.show()

#===========================================plots===========================================================

def main():

    #03.05.2024 First Knudsen test, ~1 mm pinhole, 177 mg TPB

    t = [30, 40, 50, 60, 70, 80, 92, 100, 110, 120, 130, 140]
    temp = [32, 64, 96, 117, 128, 138, 146, 149, 153, 154, 156, 157]
    tT = np.array([t, temp])

    test240503 = readDatData("240503-test.dat")

    freq = deltaFreq(test240503[2])

    #plotCoating(test240503[0], test240503[1], freq, tT, title="~1 mm pinhole test 03.05.2024", save="240503-test.png")

    #07.05.2024 Second Knudsen cell test 0.4 mm pinhole, 200 mg TPB

    t = [25, 40, 55, 70, 85, 100, 115, 130]
    temp = [34, 75, 112, 133, 146, 152, 157, 160]
    tT = np.array([t, temp])

    coat240507 = readDatData("240507.dat")

    freq = deltaFreq(coat240507[2])

    #plotCoating(coat240507[0], coat240507[1], freq, tT, title="0.4 mm pinhole 07.05.2024", save="240507")

    coat240618 = readDatData("240618.dat")
    freq240618 = deltaFreq(coat240618[2])

    plotCoating(coat240618[0], coat240618[1], freq240618)


#=========================================================================================================================

if __name__ == "__main__":
    main()