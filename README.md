# Ballistic Trajectory Simulation

## Overview
The ballistic trajectory simulation is a program designed to simulate the trajectory of a bullet, taking into account various environmental and bullet characteristics. The user can specify the attributes of the bullet and the environment through a GUI, and the program will simulate the trajectory, considering aspects such as the Coriolis effect, gravity, and wind.

## Input
Through the GUI, you can input the following bullet characteristics:
- Mass (kg)
- Velocity (m/s)
- Energy (J)
- Twist Rate (in)
- Initial X Position (m)
- Initial Y Position (m)
- Initial Z Position (m)

As well as the environmental characteristics:
- Gravity (m/s²)
- Wind Speed (m/s)
- Latitude (degrees)
- Wind Direction (degrees)

After inputting the values, click "Run Simulation" to start the simulation.

## Understanding the Formulas
The simulation uses several formulas to update the bullet's characteristics as it travels. Here, we detail the main formulas used:

### Updating Bullet Spin:
The bullet's spin is updated based on its current velocity and the twist rate.
self.spin = velocity_ft_s * 720 / self.twist_rate

### Coriolis Effect
The Coriolis effect is calculated using the following formula:
a_coriolis = np.array([-2*v[1]*w*math.sin(alpha), 2*v[0]*w*math.sin(alpha), 0])

Where:
w is the Earth's angular velocity in rad/s (0.0000727 rad/s).
alpha is the latitude in radians.
v is the current bullet's velocity vector.

### Wind Effect
The wind effect on the bullet is given by:
wind_effect = np.array([-self.environment.wind * math.cos(math.radians(float(self.environment.direction))),-self.environment.wind * math.sin(math.radians(float(self.environment.direction))),0])

### Updating Bullet Position and Velocity
The bullet's position and velocity are updated at each time step considering gravity, wind effect, and the Coriolis effect:
self.bullet.position += self.bullet.velocity * dt
self.bullet.velocity += (self.calculate_coriolis_effect() - np.array([0, 0, self.environment.gravity]) + wind_effect) * dt

Here dt is the time step for the simulation (0.01 s).


## Output
The simulation results will be displayed graphically as a 3D plot showing the bullet's trajectory. The initial and final positions will be shown in a message box and the trajectory data will be saved as an Excel file.

![](https://github.com/jcast6/Bullet-Trajectory-Simulation/blob/main/bullet_trajectory_1.gif)




