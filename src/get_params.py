"""
Created on 5 April 2024
@author: David Chan
"""

import matplotlib.pyplot as plt
import numpy as np
import csv

# Constants for conversion
ksi_to_kPa = 6894.76  # 1 ksi = 6894.76 kPa
GPa_to_kPa = 1e6      # 1 GPa = 1,000,000 kPa
# Young's modulus for steel in kPa
E_steel_kPa = 200 * GPa_to_kPa

# Define steel properties (assumed for demonstration purposes)
Fye = 50  # Yield strength of steel in ksi (kilo-pounds per square inch)
d = 1.0  # Depth of seciton in meters
# Convert yield strength from ksi to kPa
Fye_kPa = Fye * ksi_to_kPa
theta_pc = -0.003 + 0.0007 * d


def main():

    strain_at_yield, Qy, x_Qmax, Qmax_prime, x_Qr, Qr_prime, x_int, theta_ult = get_parms()

    list_of_segments = get_segments(
        strain_at_yield, Qy, x_Qmax, Qmax_prime, x_Qr, Qr_prime, x_int, theta_ult)

    # Generate points for the cyclic backbone curve starting at the origin
    points = {
        'Origin': (0, 0),
        'Qy (kPa)': (strain_at_yield, Qy),
        "Qmax' (kPa)": (x_Qmax, Qmax_prime),
        'Qint (kPa)': (x_int, Qr_prime),
        "Qr' (kPa)": (x_Qr, Qr_prime),
        'LVCC1 (kPa)': (x_Qr, 200),
        # Assuming Q at LVCC is 0 for simplicity
        'LVCC (kPa)': ((x_Qr + theta_ult*x_Qr), 0)
    }

    x_values, y_values = get_x_and_y(list_of_segments)

    # Plot the cyclic backbone
    plt.figure(figsize=(10, 6))
    lines = plt.plot(x_values, y_values, 'r--',
                     label='Cyclic Backbone Function')
    # Annotate the points on the curve
    for label, (x, y) in points.items():
        plt.annotate(f'{label}', (x, y), textcoords="offset points",
                     xytext=(0, 10), ha='center')
        plt.annotate(f'{label}', (-x, -y), textcoords="offset points",
                     xytext=(0, 10), ha='center')

    # Plot formatting
    plt.title('Cyclic Backbone Curve')
    plt.xlabel('Deformation (mm/mm)')
    plt.ylabel('Stress (kPa)')
    plt.grid(True)
    plt.legend()
    plt.savefig("backbone.png")

    with open("backbone.csv", 'w', newline='') as f:
        # using csv.writer method from csv package
        write = csv.writer(f)
        write.writerow(['x', 'y'])
        write.writerows(zip(x_values, y_values))


def calc_strain_at_yield(Qy):
    # Calculate strain at yield (elastic deformation) using Young's modulus
    # stress = force/area; strain = stress/E; for area = 1mÂ², stress = force
    strain_at_yield = (10*Qy / E_steel_kPa)  # strain is dimensionless
    return strain_at_yield


def calc_Qy(area=0.0089):
    # Equations based on provided parameters for cyclic backbone
    Qy = area * Fye_kPa  # Input cross-sectional area
    return Qy


def calc_Qmax_prime(Qy):
    Qmax_prime = 1.10 * Qy
    return Qmax_prime


def calc_Qr_prime(Qy):
    Qr_prime = 0.2 * Qy
    return Qr_prime


def calc_x_Qr(x_Qmax, theta_ult):
    x_Qr = x_Qmax + theta_ult
    return x_Qr


def calc_x_Qmax(strain_at_yield, theta_cap):
    x_Qmax = strain_at_yield + theta_cap
    return x_Qmax


def calc_x_int(x_Qmax, theta_pc):
    x_int = x_Qmax + theta_pc*-10
    return x_int


def calc_segment(x1, y1, x2, y2):
    # Calculate slope
    if (x2 - x1) != 0:
        m = (y2 - y1) / (x2 - x1)
        # Calculate y-intercept
        b = y1 - m * x1

        # Generate X values between A and B
        x_values = np.linspace(x1, x2, num=100)  # 100 points between x1 and x2

        # Calculate corresponding Y values using the line equation
        y_values = m * x_values + b
    else:
        # Generate X values between A and B
        x_values = np.linspace(x1, x2, num=100)  # 100 points between x1 and x2
        # Calculate corresponding Y values using the line equation
        y_values = np.linspace(y1, y2, num=100)  # 100 points between y1 and y2

    return (x_values, y_values)


def get_parms(area=0.0089, theta_ult=0.05):
    Qy = calc_Qy(area)
    strain_at_yield = calc_strain_at_yield(Qy)

    # Parameters for the cyclic backbone
    theta_cap = 0.046 - 0.0013 * d  # Assuming 'd' is proportional to Fye for simplicity

    Qmax_prime = calc_Qmax_prime(Qy)

    Qr_prime = calc_Qr_prime(Qy)

    x_Qmax = calc_x_Qmax(strain_at_yield, theta_cap)
    x_Qr = calc_x_Qr(x_Qmax, theta_ult)

    x_int = calc_x_int(x_Qmax, theta_pc)

    return strain_at_yield, Qy, x_Qmax, Qmax_prime, x_Qr, Qr_prime, x_int, theta_ult


def get_segments(strain_at_yield, Qy, x_Qmax, Qmax_prime, x_Qr, Qr_prime, x_int, theta_ult):

    segment1 = calc_segment(0, 0, strain_at_yield, Qy)
    segment2 = calc_segment(strain_at_yield, Qy, x_Qmax, Qmax_prime)
    segment3 = calc_segment(x_Qmax, Qmax_prime, x_int, Qr_prime)
    segment4 = calc_segment(x_int, Qr_prime, x_Qr, Qr_prime)
    segment5 = calc_segment(x_Qr, Qr_prime, x_Qr, 0)
    segment6 = calc_segment(x_Qr, 0, (x_Qr + theta_ult*x_Qr), 0)

    return [segment1, segment2, segment3, segment4, segment5, segment6]


def get_x_and_y(list_of_segments):
    # Extract the x and y coordinates for plotting
    x_values = []
    y_values = []
    for segment in list_of_segments:
        x_values.extend(segment[0].tolist())
        y_values.extend(segment[1].tolist())
    return x_values, y_values


if __name__ == "__main__":
    main()
