# Ballistic Trajectory Simulation

This application allows users to simulate the trajectory of a bullet taking into consideration various bullet and environmental characteristics. 
The simulation integrates real-world physics principles like the Coriolis effect and gravity to model the bullet's trajectory accurately.

### Functionalities

1. **GUI Interface**: GUI for inputting bullet and environmental characteristics.
2. **Simulation**: A simulation is ran based on the input characteristics and calculates the bullet's trajectory.
3. **Animation**: Visualizes the trajectory of the bullet in a 3D animated plot.
4. **Data Export**: Trajectory results data are imported into an Excel sheet.

### Math Formulas

The simulation uses various math formulas to calculate the bullet's trajectory.

1. **Velocity Update**
   
   The velocity is updated considering Coriolis effect, gravity, and wind effect:

```math
\vec{V}_{\text{new}} = \vec{V}_{\text{old}} + (\vec{A}_{\text{coriolis}} - \vec{A}_{\text{gravity}} + \vec{A}_{\text{wind}}) \Delta t\
```
   
2. **Coriolis Effect**
   
   The Coriolis acceleration (\(\vec{A}_{\text{coriolis}}\)) is given by the formula:

   \[
   \vec{A}_{\text{coriolis}} = \begin{bmatrix} -2V_y \omega \sin(\alpha) \\ 2V_x \omega \sin(\alpha) \\ 0 \end{bmatrix}
   \]
   
   where:
   - \( V_x, V_y \): components of the bullet's velocity vector
   - \( \omega \): Earth's angular velocity (\(7.27 \times 10^{-5}\) rad/s)
   - \( \alpha \): latitude in radians

3. **Gravity Effect**
   
   The gravity acceleration (\(\vec{A}_{\text{gravity}}\)) is simply:
   
   \[
   \vec{A}_{\text{gravity}} = \begin{bmatrix} 0 \\ 0 \\ -g \end{bmatrix}
   \]
   
   where \( g \) is the gravitational acceleration.

4. **Wind Effect**
   
   The wind acceleration (\(\vec{A}_{\text{wind}}\)) is calculated based on the wind speed and direction:
   
   \[
   \vec{A}_{\text{wind}} = \begin{bmatrix} -\text{wind speed} \cdot \cos(\text{wind direction}) \\ -\text{wind speed} \cdot \sin(\text{wind direction}) \\ 0 \end{bmatrix}
   \]

5. **Bullet Spin**
   
   The bullet's spin is updated according to the formula:

   \[
   \text{spin} = \left(\frac{\text{velocity (in ft/s)}}{\text{twist rate (in inches)}}\right) \cdot 720
   \]

### Menu and Creating Data Sheets

The application features a two-frame GUI interface where users can input various bullet characteristics (mass, velocity, energy, twist rate, and initial position) and environmental factors 
(gravity, wind speed, latitude, and wind direction). After running the simulation, the application will automatically create data sheets in the form of Excel files, storing the trajectory data (X, Y, and Z positions) for further analysis.

