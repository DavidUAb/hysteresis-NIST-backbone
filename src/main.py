import numpy as np
import matplotlib.pyplot as plt
import hysteresis as hys
from sklearn.metrics import mean_absolute_error
from get_params import get_segments, get_parms, get_x_and_y

def main():
    backbone_file = "SPC1.csv"
    hysteresis_data = np.loadtxt(backbone_file, delimiter=',', skiprows=2)

    # Sort the data into a xy curve
    x = hysteresis_data[:,1]*(1/280)
    y = hysteresis_data[:,0]*100
    xy = np.column_stack([x,y]) 

    # Make a hysteresis object
    myHys = hys.Hysteresis(xy)

    # Plot the object to see if cycles are tested properly
    fig, ax = plt.subplots()
    myHys.plot(True)
    plt.savefig("hysteresis.png")

    # count the number of repeats in each 'step' of the load protocol
    LPsteps = [5,5,5,3,3,3,3]

    # Make the backbone curve
    backbone = hys.getBackboneCurve(myHys, LPsteps, returnPeaks=True)    

    #Plot
    fig, ax = plt.subplots()
    backbone_data = backbone.plot(linestyle = '-.', label = 'Backbone')
    plt.minorticks_on()
    ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
    ax.grid(which='minor', linewidth=0.5, alpha = 0.4)
    ax.legend(loc='lower right')
    ax.set_xlabel('Actuator Displacement (mm)')
    ax.set_ylabel('Actuator Force (kN)')
    plt.savefig("backbone.png")

    backbone_x = backbone_data.get_xdata()
    backbone_y = backbone_data.get_ydata()
    

    steel1_backbone_x, steel1_backbone_y = plot_opensees_backbone("Steel01")

    steel1_mae = calc_mae(steel1_backbone_x, steel1_backbone_y, backbone_x, backbone_y)

    print("MAE for Steel01: ", steel1_mae)


def plot_opensees_backbone(steel_name):
    xy = np.loadtxt(steel_name+"hysteresis.csv", delimiter=',', skiprows=2)


    """
    There are [x] repeats at each load protocol step, and y steps in total.
    """
    lpSteps = [3]*20

    # Make the Hysteresis object
    myHys = hys.Hysteresis(xy)

    # Get the backbone
    backbone = hys.getBackboneCurve(myHys, lpSteps)

    fig, ax = plt.subplots()
    backbone_data = backbone.plot(label='Analysis Backbone Data', color='red')

    ax.set_xlabel('Deformation (mm/mm)')
    ax.set_ylabel('Stress (kPa)')
    plt.minorticks_on()
    ax.grid(which='major', color='grey', linewidth=0.5, alpha=0.8)
    ax.grid(which='minor', linewidth=0.5, alpha=0.4)
    ax.legend()
    ax.legend(loc='lower right')

    plt.savefig(steel_name+"standard_backbone.png")

    backbone_x = backbone_data.get_xdata()
    backbone_y = backbone_data.get_ydata()

    return backbone_x,backbone_y

def calc_mae(predicted_backbone_x, predicted_backbone_y, backbone_x, backbone_y):

    # Find the closest x_dense points to each x_sparse point and their corresponding y values
    y_dense_matched = np.array(
        [predicted_backbone_y[np.argmin(np.abs(predicted_backbone_x - x_val))] for x_val in backbone_x])

    # Calculate the Mean Absolute Error (MAE)
    mae = np.mean(np.abs(y_dense_matched - backbone_y))

    return mae


if __name__ == "__main__":
    main()