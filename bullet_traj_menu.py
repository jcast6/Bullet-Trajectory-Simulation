import math
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

class Bullet:
    def __init__(self, mass, velocity, energy, twist_rate):
        self.mass = mass
        self.velocity = np.array([velocity, 0.0, 0.0])  # Initial velocity along the x-axis
        self.energy = energy
        self.twist_rate = twist_rate  # Twist rate in inches
        self.spin = 0  # Bullet's spin in RPM
        self.position = np.array([0.0, 0.0, 60.0])  # x, y, z (bullet fired from "" units above the ground)
        
    def update_spin(self):
        # Convert velocity to ft/s
        velocity_ft_s = np.linalg.norm(self.velocity) * 3.281
        # Update spin
        self.spin = velocity_ft_s * 720 / self.twist_rate

class Environment:
    def __init__(self, gravity, wind, latitude, direction):
        self.gravity = gravity
        self.wind = wind
        self.latitude = latitude
        self.direction = direction

class Simulation:
    def __init__(self, bullet, environment):
        self.bullet = bullet
        self.environment = environment
        self.trajectory = [[], [], []]  # Store the bullet's trajectory

    def calculate_coriolis_effect(self):
        w = 0.0000727  # Angular velocity of the Earth in rad/s
        alpha = math.radians(self.environment.latitude)  # Converting latitude to radians
        v = self.bullet.velocity  # Bullet's velocity
        a_coriolis = np.array([-2*v[1]*w*math.sin(alpha), 2*v[0]*w*math.sin(alpha), 0])
        return a_coriolis

    def update_bullet_position(self):
        # Update bullet's position and velocity
        dt = 0.01  # Time step
        self.bullet.position += self.bullet.velocity * dt
        self.bullet.velocity += (self.calculate_coriolis_effect() - np.array([0, 0, self.environment.gravity])) * dt
        self.bullet.update_spin()

        self.trajectory[0].append(self.bullet.position[0])
        self.trajectory[1].append(self.bullet.position[1])
        self.trajectory[2].append(self.bullet.position[2])

    def run(self):
        while self.bullet.position[2] > 0:  # While bullet is still in the air
            self.update_bullet_position()

    def animate(self, i):
        self.line.set_data(self.trajectory[0][:i+1], self.trajectory[2][:i+1])
        return self.line,

    def update(self, i):
        self.line.set_data(self.trajectory[0][:i+1], self.trajectory[2][:i+1])
        return self.line,

    def init(self):
        self.line.set_data([], [])
        return self.line,

    def plot_trajectory(self):
        self.run()  # Run the simulation first
        # Convert the trajectory into a numpy array
        self.trajectory = np.array(self.trajectory)

        fig, ax = plt.subplots()
        ax.set_xlim((min(self.trajectory[0]), max(self.trajectory[0])))
        ax.set_ylim((0, max(self.trajectory[2])))  # We want to plot height (z), not y
        self.line, = ax.plot([], [], 'b-')
        
        anim = animation.FuncAnimation(fig, self.update, frames=range(len(self.trajectory[0])), 
                                       interval=200, init_func=self.init, blit=True)
        
        anim.save('bullet_trajectory.gif', writer='pillow')
        plt.show()

# Instantiate the classes
bullet = Bullet(mass=0.008, velocity=940, energy=3617, twist_rate=12)  # Twist rate of 1:12"
environment = Environment(gravity=9.81, wind=2, latitude=45, direction='N')
simulation = Simulation(bullet, environment)

# Run the simulation and plot the trajectory
simulation.plot_trajectory()
