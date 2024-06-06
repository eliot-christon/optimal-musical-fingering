__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    
    with open("src/genetic_optim/saved/fitnesses.npy", "rb") as f:
        fitnesses = np.load(f)

    # plt.figure()
    # plt.imshow(fitnesses, aspect='auto')
    # plt.colorbar()
    # plt.xlabel("Individual")
    # plt.ylabel("Generation")

    # plt.show()

    fig, ax = plt.subplots(1, 2, figsize=(14, 5))

    # fix colormap
    cmap = plt.get_cmap('coolwarm_r')

    ax[0].set_xlabel("Generation")
    ax[0].set_ylabel("Individual")
    ax[0].set_title("Fitnesses of all individuals over generations")
    cbar = plt.colorbar(ax[0].imshow(fitnesses.T, aspect='auto', cmap=cmap), ax=ax[0])
    # invert y axis
    ax[0].invert_yaxis()

    ax[1].plot(np.mean(fitnesses, axis=1))
    ax[1].set_xlabel("Generation")
    ax[1].set_ylabel("Mean fitness")
    ax[1].set_title("Mean fitness over generations")

    plt.show()