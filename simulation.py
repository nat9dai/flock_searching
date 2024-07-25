from dynamic_unicycle import DynamicUnicycle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pynput import keyboard

def create_robot_triangle(x, y, yaw, color='blue'):
    side_length, front_length = 0.3, 0.45
    half_length = side_length / 2
    vertices = [
        (x - half_length, y - half_length),
        (x - half_length, y + half_length),
        (x + front_length, y)
    ]
    rot_matrix = np.array([[np.cos(yaw), -np.sin(yaw)],
                           [np.sin(yaw), np.cos(yaw)]])
    rotated_vertices = np.dot(vertices - np.array([x, y]), rot_matrix.T) + np.array([x, y])
    return Polygon(rotated_vertices, closed=True, edgecolor='k', facecolor=color)

xlim_min, xlim_max = -5, 5
ylim_min, ylim_max = -5, 5
fig, ax = plt.subplots()

def update_plot(robot_list):
    ax.clear()
    ax.set(xlim=(xlim_min, xlim_max), ylim=(ylim_min, ylim_max),
                title='Robot Positions and Orientations', xlabel='X Position (m)', ylabel='Y Position (m)')

    for robot in robot_list:
        color = 'red' if robot.id == 0 else 'blue'
        ax.add_patch(create_robot_triangle(robot.x, robot.y, robot.theta, color))

def on_press(key):
    try:
        if key == keyboard.Key.up:
            leader.v += 0.1  # Increase forward speed
        elif key == keyboard.Key.down:
            leader.v -= 0.1  # Decrease forward speed
        elif key == keyboard.Key.left:
            leader.omega += 0.1  # Turn left
        elif key == keyboard.Key.right:
            leader.omega -= 0.1  # Turn right
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def run(robot_list, dt):
    plt.ion()  # Enable interactive mode for real-time plotting
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while True:
        update_plot(robot_list)
        for robot in robot_list:
            if robot.id == 0:
                robot.step(leader.v, leader.omega, dt)
            else:
                robot.step(0, 0, dt)
        plt.pause(dt)

dt = 0.01
robot_list = []
N = 3
for i in range(N):
    robot_list.append(DynamicUnicycle(i, i/2, i/2, 0))

leader = robot_list[0]
leader.v = 0
leader.omega = 0

run(robot_list, dt)
