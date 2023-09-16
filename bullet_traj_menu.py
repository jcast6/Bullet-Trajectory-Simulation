import math
import numpy as np
import tkinter as tk
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import animation
from tkinter import messagebox

def create_gui():
    global mass_var, velocity_var, energy_var, twist_rate_var
    global x_pos_var, y_pos_var, z_pos_var
    global gravity_var, wind_var, latitude_var, direction_var

    root = tk.Tk()
    root.title("Ballistic Trajectory Simulation")

    frame1 = tk.Frame(root)
    frame1.pack(side=tk.LEFT, padx=20, pady=20)

    frame2 = tk.Frame(root)
    frame2.pack(side=tk.LEFT, padx=20, pady=20)

    mass_var = tk.StringVar()
    velocity_var = tk.StringVar()
    energy_var = tk.StringVar()
    twist_rate_var = tk.StringVar()
    x_pos_var = tk.StringVar()
    y_pos_var = tk.StringVar()
    z_pos_var = tk.StringVar()

    gravity_var = tk.StringVar()
    wind_var = tk.StringVar()
    latitude_var = tk.StringVar()
    direction_var = tk.StringVar()

    bullet_char_labels = ["Mass (kg)", "Velocity (m/s)", "Energy (J)", "Twist Rate (in)", "Initial X Position (m)", "Initial Y Position (m)", "Initial Z Position (m)"]
    env_char_labels = ["Gravity (m/s²)", "Wind Speed (m/s)", "Latitude (degrees)", "Wind Direction"]

    bullet_char_vars = [mass_var, velocity_var, energy_var, twist_rate_var, x_pos_var, y_pos_var, z_pos_var]
    env_char_vars = [gravity_var, wind_var, latitude_var, direction_var]

    for i, label in enumerate(bullet_char_labels):
        tk.Label(frame1, text=label).grid(row=i, column=0, padx=5, pady=5)
        tk.Entry(frame1, textvariable=bullet_char_vars[i]).grid(row=i, column=1, padx=5, pady=5)

    for i, label in enumerate(env_char_labels):
        tk.Label(frame2, text=label).grid(row=i, column=0, padx=5, pady=5)
        tk.Label(frame2, text="Wind Direction (degrees, clockwise from North)").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(frame2, textvariable=env_char_vars[i]).grid(row=i, column=1, padx=5, pady=5)

    tk.Button(root, text="Run Simulation", command=run_simulation).pack(pady=20)

    root.mainloop()

def get_float_input(prompt, min_value=None, max_value=None):
    while True:
        try:
            # Getting a float input with a prompt, and optional min and max values
            value = float(input(prompt))
            if min_value is not None and value < min_value:
                raise ValueError(f"The value cannot be less than {min_value}")
            if max_value is not None and value > max_value:
                raise ValueError(f"The value cannot be more than {max_value}")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}")

def get_string_input(prompt, valid_values=None):
    while True:
        # Getting a string input with a prompt and an optional list of valid values
        value = input(prompt)
        if valid_values is None or value in valid_values:
            return value
        else:
            print(f"Invalid input. Valid values are: {', '.join(valid_values)}")

def get_bullet_characteristics():
    try:
        mass = float(mass_var.get())
        velocity = float(velocity_var.get())
        energy = float(energy_var.get())
        twist_rate = float(twist_rate_var.get())
        initial_position = [float(x_pos_var.get()), float(y_pos_var.get()), float(z_pos_var.get())]
        return mass, velocity, energy, twist_rate, initial_position
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numerical values for bullet characteristics")
        return None

def get_environment_characteristics():
    try:
        gravity = float(gravity_var.get())
        wind = float(wind_var.get())
        latitude = float(latitude_var.get())
        direction = direction_var.get()
        return gravity, wind, latitude, direction
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numerical values for environment characteristics")
        return None

class Bullet:
    def __init__(self, mass, velocity, energy, twist_rate, initial_position):
        # Initializing bullet properties
        self.mass = mass
        # Initializing velocity vector with velocity along the x-axis
        self.velocity = np.array([velocity, 0.0, 0.0])  
        self.energy = energy
        # Setting twist rate (in inches)
        self.twist_rate = twist_rate  
        self.spin = 0  # Initializing bullet spin to zero
        # Setting the initial position vector
        self.position = np.array(initial_position)  
        
    
    def update_spin(self):
        # Convert velocity from m/s to ft/s
        velocity_ft_s = np.linalg.norm(self.velocity) * 3.281
        # Update bullet spin based on the current velocity and twist rate
        self.spin = velocity_ft_s * 720 / self.twist_rate

class Environment:
    def __init__(self, gravity, wind, latitude, direction):
        # Setting environment characteristics: gravity, wind, latitude, and direction
        self.gravity = gravity
        self.wind = wind
        self.latitude = latitude
        self.direction = direction

class Simulation:
    def __init__(self, bullet, environment):
        # Initializing simulation with bullet and environment instances
        self.bullet = bullet
        self.environment = environment
        # Initializing trajectory list to store bullet's trajectory during the simulation
        self.trajectory = [[], [], []]  

    def calculate_coriolis_effect(self):
        # Constants representing the Earth's angular velocity in rad/s
        w = 0.0000727  
        # Converting latitude from degrees to radians
        alpha = math.radians(self.environment.latitude)  
        v = self.bullet.velocity  # Getting the current bullet's velocity vector
        # Calculating Coriolis acceleration vector
        a_coriolis = np.array([-2*v[1]*w*math.sin(alpha), 2*v[0]*w*math.sin(alpha), 0])
        return a_coriolis

    def update_bullet_position(self):
         # Time step for simulation (in seconds)
        dt = 0.01  
        # Updating bullet's position based on its current velocity and the time step
        self.bullet.position += self.bullet.velocity * dt
        
        # Calculate wind effect
        wind_effect = np.array([-self.environment.wind * math.cos(math.radians(float(self.environment.direction))), 
                                -self.environment.wind * math.sin(math.radians(float(self.environment.direction))), 
                                0])
        
        # Updating bullet's velocity considering the Coriolis effect, gravity, and wind effect
        self.bullet.velocity += (self.calculate_coriolis_effect() - np.array([0, 0, self.environment.gravity]) + wind_effect) * dt
        # Updating bullet's spin
        self.bullet.update_spin()
        # Storing the updated bullet's position in the trajectory list
        self.trajectory[0].append(self.bullet.position[0])
        self.trajectory[1].append(self.bullet.position[1])
        self.trajectory[2].append(self.bullet.position[2])

    def run(self):
        # Running the simulation while the bullet is above ground level (Z > 0)
        while self.bullet.position[2] > 0:  
            self.update_bullet_position()

    def animate(self, i):
        # Setting data for animation frame
        self.line.set_data(self.trajectory[0][:i+1], self.trajectory[2][:i+1])
        return self.line,

    def update(self, i):
        # Updating plot data for 3D trajectory plot
        self.line.set_data(self.trajectory[0][:i+1], self.trajectory[1][:i+1])
        self.line.set_3d_properties(self.trajectory[2][:i+1])
        return self.line,

    def init(self):
        # Initializing line data for animation
        self.line.set_data([], [])
        self.line.set_3d_properties([])
        return self.line,

    def plot_trajectory(self):
        # Running the simulation to get the complete trajectory
        self.run()  
        # Converting trajectory lists to a numpy array for easier manipulation
        self.trajectory = np.array(self.trajectory) 

        # Initializing 3D plot for displaying the bullet trajectory
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim((min(self.trajectory[0]), max(self.trajectory[0])))
        ax.set_ylim((min(self.trajectory[1]), max(self.trajectory[1])))
        ax.set_zlim((min(self.trajectory[2]), max(self.trajectory[2])))  # Updated line
        self.line, = ax.plot([], [], [], 'b-')
        
        # Creating an animation of the bullet trajectory
        anim = animation.FuncAnimation(fig, self.update, frames=range(len(self.trajectory[0])), 
                                    interval=200, init_func=self.init, blit=False)
        
        # unique file name for simulation based on simulation count
        gif_name = f'bullet_trajectory_{simulation_count}.gif'
        
        # Saving the animation as a GIF
        anim.save(gif_name, writer='pillow')
        plt.show()

def run_simulation():
    bullet_char = get_bullet_characteristics()
    environment_char = get_environment_characteristics()

    if bullet_char and environment_char:
        bullet = Bullet(*bullet_char)
        environment = Environment(*environment_char)
        
        simulation = Simulation(bullet, environment)
        simulation.plot_trajectory()
        
        # Get the initial and final positions from the simulation's trajectory data
        initial_position = simulation.trajectory[:, 0]
        final_position = simulation.trajectory[:, -1]
        
        # Create a message to display
        message = f"Initial Position: X={initial_position[0]:.2f}, Y={initial_position[1]:.2f}, Z={initial_position[2]:.2f}\n"
        message += f"Final Position: X={final_position[0]:.2f}, Y={final_position[1]:.2f}, Z={final_position[2]:.2f}"
        
        # Save the trajectory data to an Excel file
        save_to_excel(simulation.trajectory)
        
        # Display a messagebox with the initial and final positions
        messagebox.showinfo("Simulation Results", message)

simulation_count = 0
def save_to_excel(trajectory):
    global simulation_count
    simulation_count += 1

    # Create a DataFrame from the trajectory data
    df = pd.DataFrame({
        'X Position': trajectory[0],
        'Y Position': trajectory[1],
        'Z Position': trajectory[2]
    })

    # Create a unique file name based on the simulation count
    file_name = f'simulation_results_{simulation_count}.xlsx'
    
    # Save the DataFrame to an Excel file
    df.to_excel(file_name, index=False)

def main():
    create_gui()

if __name__ == "__main__":
    main()
