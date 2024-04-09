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


def main():
    file = "hysteresis.csv"
    backbone_file = "backbone.csv"

    xy = np.loadtxt(file, delimiter=',', skiprows=2)
    predicted_backbone = np.loadtxt(backbone_file, delimiter=',', skiprows=1)

    """
  There are [x] repeats at each load protocol step, and y steps in total.
  """
    lpSteps = [1]*2

    # Make the Hysteresis object
    myHys = hys.Hysteresis(xy)

    # Get the backbone
    backbone = hys.getBackboneCurve(myHys, lpSteps)

    _, backbone_data = plot_backbone(backbone)
    plt.savefig("standard_backbone.png")

    backbone_x = backbone_data.get_xdata()
    backbone_y = backbone_data.get_ydata()

    predicted_backbone_x = np.array(predicted_backbone)[:, 0]
    predicted_backbone_y = np.array(predicted_backbone)[:, 1]

    mae = calc_mae(predicted_backbone_x, predicted_backbone_y,
                   backbone_x, backbone_y)
    print(f'Mean Absolute Error (MAE): {mae}')

    ax, backbone_data = plot_backbone(backbone)
    ax.plot(predicted_backbone_x, predicted_backbone_y)

    plt.savefig("standard_backbone vs initial backbone.png")

    mins = grid_search(backbone, backbone_x, backbone_y)

    ax, _ = plot_backbone(backbone)
    ax.plot(mins[3], mins[4])

    plt.savefig(
        "FINAL standard_backbone vs {},{} backbone.png".format(mins[0], mins[1]))
    plt.close()

    print(mins[0], mins[1], mins[2])


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


def grid_search(backbone, backbone_x, backbone_y):

    areas = np.linspace(0.0001, 0.01, num=250)
    theta_ults = np.linspace(0.01, 1, num=250)
    mins = [float('inf'), 0, 0, 0, 0]
    i = 0

    for area in areas:
        for theta_ult in theta_ults:
            strain_at_yield, Qy, x_Qmax, Qmax_prime, x_Qr, Qr_prime, x_int, theta_ult = get_parms(
                area, theta_ult)

            list_of_segments = get_segments(
                strain_at_yield, Qy, x_Qmax, Qmax_prime, x_Qr, Qr_prime, x_int, theta_ult)

            x_values, y_values = get_x_and_y(list_of_segments)

            mae = calc_mae(x_values, y_values,
                           backbone_x, backbone_y)
            if (mae < mins[0]) & (x_values[-1] <= 0.12):
                mins[0] = mae
                mins[1] = area
                mins[2] = theta_ult
                mins[3] = x_values
                mins[4] = y_values
                if i % 50 == 0:
                    ax, _ = plot_backbone(backbone)
                    ax.plot(x_values, y_values)

                    plt.savefig(
                        "figs/{}. standard_backbone vs {},{} backbone.png".format(i, area, theta_ult))
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
