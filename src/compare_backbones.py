# -*- coding: utf-8 -*-
"""
Created on 5 April 2024
@author: David Chan
"""
import numpy as np
import matplotlib.pyplot as plt
import hysteresis as hys
from sklearn.metrics import mean_absolute_error
from get_params import get_segments, get_parms, get_x_and_y
from get_hysteresis_data import get_hysteresis


def main():
    backbone_file = "SPC1.csv"
    hysteresis_data = np.loadtxt(backbone_file, delimiter=',', skiprows=2)

    # Sort the data into a xy curve
    x = hysteresis_data[:, 1]*(1/280)
    y = hysteresis_data[:, 0]*100
    xy = np.column_stack([x, y])

    # Make a hysteresis object
    myHys = hys.Hysteresis(xy)

    # Plot the object to see if cycles are tested properly
    fig, ax = plt.subplots()
    myHys.plot(True)
    plt.savefig("hysteresis.png")
    plt.close()

    # count the number of repeats in each 'step' of the load protocol
    LPsteps = [5, 5, 5, 3, 3, 3, 3]

    # Make the backbone curve
    backbone = hys.getBackboneCurve(myHys, LPsteps, returnPeaks=True)

    backbone_data = backbone.plot(linestyle='-.', label='Backbone')

    experimental_backbone_x = backbone_data.get_xdata()
    experimental_backbone_y = backbone_data.get_ydata()

    mins = grid_search(experimental_backbone_x, experimental_backbone_y)

    plt.plot(experimental_backbone_x, experimental_backbone_y)
    plt.plot(mins[2], mins[3])

    plt.savefig(
        "FINAL Steel {} standard_backbone vs experimental backbone.png".format(mins[4]))
    plt.close()

    print("Error: ", mins[0], " M1: ", mins[1], " at i: ", mins[4])

    mins[5].plot(True)
    # myHys.plot(True)
    plt.savefig("Experimental vs Generated Hysteresis.png")


def get_hysteresis_backbone(M1):
    x, y = get_hysteresis(M1)
    xy = np.column_stack((x, y))
    """
    There are [x] repeats at each load protocol step, and y steps in total.
    """
    lpSteps = [3]*20

    # Make the Hysteresis object
    myHys = hys.Hysteresis(xy)

    # Get the backbone
    backbone = hys.getBackboneCurve(myHys, lpSteps)

    backbone_data = backbone.plot(label='Analysis Backbone Data', color='red')

    backbone_x = backbone_data.get_xdata()
    backbone_y = backbone_data.get_ydata()

    return backbone_x, backbone_y, myHys


def plot_backbone(backbone):
    # Plot
    fig, ax = plt.subplots()
    backbone_data = backbone.plot(label='Analysis Backbone Data', color='red')

    ax.set_xlabel('Deformation (mm/mm)')
    ax.set_ylabel('Stress (kPa)')
    plt.minorticks_on()
    ax.grid(which='major', color='grey', linewidth=0.5, alpha=0.8)
    ax.grid(which='minor', linewidth=0.5, alpha=0.4)
    ax.legend()
    ax.legend(loc='lower right')

    return ax, backbone_data


def grid_search(backbone_x, backbone_y):

    M1s = np.linspace(1, 5000, num=500)
    mins = [float('inf'), 0, 0, 0, 0, 0]
    i = 0

    for M1 in M1s:
        x_values, y_values, hysteresis_xy = get_hysteresis_backbone(M1)

        mae = calc_mae(x_values, y_values,
                       backbone_x, backbone_y)
        if mae < mins[0]:
            mins[0] = mae
            mins[1] = M1
            mins[2] = x_values
            mins[3] = y_values
            mins[4] = i
            mins[5] = hysteresis_xy

        if i % 100 == 0:
            print("Error: ", mins[0], "M1: ", mins[1])
            plt.plot(x_values, y_values)
            plt.plot(backbone_x, backbone_y)

            plt.savefig(
                "figs/Steel {}. standard_backbone vs experimental backbone.png".format(i))
            plt.close()
        i += 1

    return mins


def calc_mae(predicted_backbone_x, predicted_backbone_y, backbone_x, backbone_y):

    # Find the closest x_dense points to each x_sparse point and their corresponding y values
    y_dense_matched = np.array(
        [predicted_backbone_y[np.argmin(np.abs(predicted_backbone_x - x_val))] for x_val in backbone_x])

    # Calculate the Mean Absolute Error (MAE)
    mae = np.mean(np.abs(y_dense_matched - backbone_y))

    return mae


if __name__ == "__main__":
    main()
