import numpy as np

class DynamicUnicycle:
    def __init__(self, id=0, x=0, y=0, theta=0):
        self.id = id
        self.x = x
        self.y = y
        self.theta = theta
    
    def step(self, v, w, dt):
        self.x += v * np.cos(self.theta) * dt
        self.y += v * np.sin(self.theta) * dt
        self.theta += w * dt
    
    def step_rk4(self, v, w, dt):
        k1_x = v * np.cos(self.theta) * dt
        k1_y = v * np.sin(self.theta) * dt
        k1_theta = w * dt
        
        k2_x = v * np.cos(self.theta + 0.5 * k1_theta) * dt
        k2_y = v * np.sin(self.theta + 0.5 * k1_theta) * dt
        k2_theta = w * dt
        
        k3_x = v * np.cos(self.theta + 0.5 * k2_theta) * dt
        k3_y = v * np.sin(self.theta + 0.5 * k2_theta) * dt
        k3_theta = w * dt
        
        k4_x = v * np.cos(self.theta + k3_theta) * dt
        k4_y = v * np.sin(self.theta + k3_theta) * dt
        k4_theta = w * dt
        
        self.x += (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6
        self.y += (k1_y + 2 * k2_y + 2 * k3_y + k4_y) / 6
        self.theta += (k1_theta + 2 * k2_theta + 2 * k3_theta + k4_theta) / 6