import numpy as np
import matplotlib.pyplot as plt
import TempProfile, profile

temperature_profile = np.array(profile.T)

# Define parameters
alpha = 0.01  # Thermal diffusivity
L = len(temperature_profile)  # Length of the 1D domain
T = temperature_profile  # Initial temperature profile

# Set up the time and space discretization
dt = 0.01  # Time step
dx = 1.0  # Spatial step
num_time_steps = 100  # Number of time steps

# Create an array for spatial positions
x = np.arange(L)

# Create an array to store the temperature profile at each time step
temperature_profiles = [T]  # Initial profile

for _ in range(num_time_steps):
    new_T = T.copy()
    new_T[1:-1] = T[1:-1] + alpha * (T[2:] - 2 * T[1:-1] + T[:-2]) / (dx ** 2) * dt
    T = new_T
    temperature_profiles.append(T)

# Plot the temperature profiles at different time steps
for i, profile in enumerate(temperature_profiles):
    plt.plot(x, profile, label=f"Time Step {i}")
plt.xlabel("Position")
plt.ylabel("Temperature")
plt.legend()
plt.show()