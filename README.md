# Ballistic Trajectory Simulation

Ballistic Trajectory Simulation is a Python application developed to simulate the trajectory of a bullet considering various environmental and bullet characteristics. The program also features a GUI to ease the process of inputting necessary data.

## Features

1. **Graphical User Interface (GUI)** - A user-friendly GUI to input bullet and environment characteristics without needing to interact with the command line.
2. **Bullet Trajectory Simulation** - Accurate simulation of bullet trajectory considering various factors like gravity, wind speed, and Coriolis effect.
3. **Simulation Visualization** - Visual representation of the bullet trajectory in a 3D graph.
4. **Data Export** - The trajectory data is saved to an Excel sheet for further analysis and reference.
5. **Simulation Results Popup** - A popup displaying the initial and final positions of the bullet after the simulation.

## Formulas Used

1. **Bullet Characteristics Formulas:**
   - Kinetic Energy: \( E = \frac{1}{2} m v^2 \)
   
2. **Coriolis Effect Formula:**
   - \( a_{coriolis} = \begin{bmatrix} -2v_y \omega \sin(\alpha) \\ 2v_x \omega \sin(\alpha) \\ 0 \end{bmatrix} \)
   
   where:
   - \( a_{coriolis} \): Coriolis acceleration vector
   - \( v_x \): velocity along the x-axis
   - \( v_y \): velocity along the y-axis
   - \( \omega \): Earth's angular velocity (0.0000727 rad/s)
   - \( \alpha \): Latitude in radians

## GUI Overview

The GUI consists of two frames:

1. **Frame 1** (Bullet Characteristics):
   - Mass (kg)
   - Velocity (m/s)
   - Energy (J)
   - Twist Rate (in)
   - Initial X Position (m)
   - Initial Y Position (m)
   - Initial Z Position (m)

2. **Frame 2** (Environment Characteristics):
   - Gravity (m/s²)
   - Wind Speed (m/s)
   - Latitude (degrees)
   - Wind Direction

After inputting the necessary details, click on "Run Simulation" to start the simulation.

## Output Data Sheets

The simulation results are stored in Excel files with filenames following the pattern `simulation_results_<count>.xlsx`, where `<count>` is the number of simulations run since the start of the program.


   
