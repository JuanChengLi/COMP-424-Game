# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
from copy import deepcopy
import random
import math


@register_agent("student_agent")
class StudentAgent(Agent):
    """
    A dummy class for your implementation. Feel free to use this class to
    add any helper functionalities needed for your agent.
    """

    def __init__(self):
        super(StudentAgent, self).__init__()
        self.name = "StudentAgent"
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }

        self.move_map = {
            "up": (-1,0),
            "right": (0,1),
            "down": (1,0),
            "left": (0,-1),
        }

        self.autoplay = True

    def step(self, chess_board, my_pos, adv_pos, max_step):


        s_x, s_y = my_pos
        e_x, e_y = adv_pos

        moving_agent = deepcopy(my_pos)
        step_left = max_step

        d_x = e_x - s_x
        d_y = e_y - s_y


        if (abs(d_x) >= step_left):
            move_x = int(math.copysign(step_left,d_x))
            step_left = step_left - abs(move_x)
        
        elif (abs(d_x) < step_left):
            move_x = d_x
            step_left = step_left - abs(move_x)
        
        if (abs(d_y) >= step_left):
            move_y = int(math.copysign(step_left,d_y))
            step_left = step_left - abs(move_y)

        elif (abs(d_y) < step_left):
            move_y = d_y
            step_left = step_left - abs(d_y)
        
        my_pos = s_x + move_x, s_y + move_y

        if (e_x == my_pos[0] + 1 and e_y == my_pos[1]):
            barrier = self.dir_map["d"]
        
        elif (e_x == my_pos[0] - 1 and e_y == my_pos[1]):
            barrier = self.dir_map["u"]

        elif (e_x == my_pos[0] and e_y == my_pos[1] + 1):
            barrier = self.dir_map["r"]
        
        elif (e_x == my_pos[0] and e_y == my_pos[1] - 1):
            barrier = self.dir_map["l"]
        
        else:
            barrier = random.randint(0, 4)
        
        

        """
        Implement the step function of your agent here.
        You can use the following variables to access the chess board:
        - chess_board: a numpy array of shape (x_max, y_max, 4)
        - my_pos: a tuple of (x, y)
        - adv_pos: a tuple of (x, y)
        - max_step: an integer

        You should return a tuple of ((x, y), dir),
        where (x, y) is the next position of your agent and dir is the direction of the wall
        you want to put on.

        Please check the sample implementation in agents/random_agent.py or agents/human_agent.py for more details.
        """
        # dummy return
        return my_pos, barrier
