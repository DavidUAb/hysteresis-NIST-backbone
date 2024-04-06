import matplotlib.pyplot as plt
import numpy as np
import csv

# Constants for conversion
ksi_to_kPa = 6894.76  # 1 ksi = 6894.76 kPa
GPa_to_kPa = 1e6      # 1 GPa = 1,000,000 kPa

# Young's modulus for steel in kPa
E_steel_kPa = 200 * GPa_to_kPa

# Define steel properties (assumed for demonstration purposes)
Fye = 36  # Yield strength of steel in ksi (kilo-pounds per square inch)
d =  2.0 #Depth of seciton in meters
# Convert yield strength from ksi to kPa
Fye_kPa = Fye * ksi_to_kPa

# Equations based on provided parameters for cyclic backbone
Qy = 1.0 * Fye_kPa  # Assuming cross-sectional area of 1 m² for simplicity

# Calculate strain at yield (elastic deformation) using Young's modulus
# stress = force/area; strain = stress/E; for area = 1m², stress = force
strain_at_yield = Qy / E_steel_kPa  # strain is dimensionless

# Parameters for the cyclic backbone
theta_cap = 0.046 - 0.0013 * d  # Assuming 'd' is proportional to Fye for simplicity
Qmax_prime = 1.10 * Qy
theta_pc = -0.003 + 0.0007 * d
theta_ult = 0.05
Qr_prime = 0.2 * Qy
#x_Qmax = strain_at_yield + ((Qmax_prime-Qy)/theta_cap)
x_Qmax = strain_at_yield + theta_cap
#x_Qr = x_Qmax + (((Qr_prime-Qmax_prime)/theta_pc) + theta_ult)
x_Qr = x_Qmax  + theta_ult
# Generate points for the cyclic backbone curve starting at the origin
points = {
    'Origin': (0, 0),
    'Qy (kPa)': (strain_at_yield, Qy),
    "Qmax' (kPa)": (x_Qmax, Qmax_prime),
    "Qr' (kPa)": (x_Qr, Qr_prime),
    'LVCC (kPa)': ((x_Qr + theta_ult*x_Qr), 0)  # Assuming Q at LVCC is 0 for simplicity
}


# Extract the x and y coordinates for plotting
x_values = [point[0] for point in points.values()]
y_values = [point[1] for point in points.values()]
neg_x_values = [-point[0] for point in points.values()]
neg_y_values = [-point[1] for point in points.values()]


# Plot the cyclic backbone
plt.figure(figsize=(10, 6))
line1 = plt.plot(x_values, y_values, 'r--', label='Cyclic Backbone Function')
line2 = plt.plot(neg_x_values, neg_y_values, 'r--',)

print(line1)

# Annotate the points on the curve
for label, (x, y) in points.items():
    plt.annotate(f'{label}', (x, y), textcoords="offset points", xytext=(0,10), ha='center')
    plt.annotate(f'{label}', (-x, -y), textcoords="offset points", xytext=(0,10), ha='center')

# Plot formatting
plt.title('Cyclic Backbone Curve')
plt.xlabel('Deformation (strain)')
plt.ylabel('Stress (kPa)')
plt.grid(True)
plt.legend()
plt.savefig("backbone.png")
    
with open("backbnoe.csv",'w') as f:
    #using csv.writer method from csv package
    write = csv.writer(f)
    write.writerow(['x','y'])
    write.writerows(line1)