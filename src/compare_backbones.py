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
from get_hysteresis_data import *


def main():
    backbone_file = "backbone.csv"

    predicted_backbone = np.loadtxt(backbone_file, delimiter=',', skiprows=1)

    plt.savefig("standard_backbone.png")

    experimental_backbone_x = np.array(predicted_backbone)[:, 0]
    experimental_backbone_y = np.array(predicted_backbone)[:, 1]

    mins = grid_search(experimental_backbone_x, experimental_backbone_y)

    ax, _ = plt.plot(experimental_backbone_x, experimental_backbone_y)
    ax.plot(mins[3], mins[4])

    plt.savefig(
        "FINAL standard_backbone vs {} backbone.png".format(mins[1]))
    plt.close()

    print(mins[0], mins[1], mins[2])


def get_hysteresis_backbone(M1):
    xy = get_hysteresis(M1)
    """
    There are [x] repeats at each load protocol step, and y steps in total.
    """
    lpSteps = [3]*20

    # Make the Hysteresis object
    myHys = hys.Hysteresis(xy)

    # Get the backbone
    backbone = hys.getBackboneCurve(myHys, lpSteps)

    _, backbone_data = plot_backbone(backbone)

    backbone_x = backbone_data.get_xdata()
    backbone_y = backbone_data.get_ydata()

    return backbone_x, backbone_y


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

    M1s = np.linspace(2500, 3500, num=1000)
    mins = [float('inf'), 0, 0, 0]
    i = 0

    for M1 in M1s:
        x_values, y_values = get_hysteresis_backbone(M1)

        mae = calc_mae(x_values, y_values,
                       backbone_x, backbone_y)
        if (mae < mins[0]) & (x_values[-1] <= 0.12):
            mins[0] = mae
            mins[1] = M1
            mins[2] = x_values
            mins[3] = y_values
            if i % 50 == 0:
                ax, _ = plot_backbone(backbone)
                ax.plot(x_values, y_values)
                ax.plot(backbone_x, backbone_y)

                plt.savefig(
                    "figs/{}. standard_backbone vs {} backbone.png".format(i, M1))
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
