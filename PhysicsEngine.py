class Movement: 
    def __init__(self):
            pass

    def ending_velocity(self, initial_velocity, acceleration, time = 6):
        final_velocity = initial_velocity + acceleration * time
        return final_velocity
