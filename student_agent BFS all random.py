# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
# added import
from copy import deepcopy
import random
import math
from collections import deque


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

        self.moves = ((-1, 0), (0, 1), (1, 0), (0, -1))

        self.autoplay = True

    def step(self, chess_board, my_pos, adv_pos, max_step):

        #move selection
        all_moves = self.findAllMoves(chess_board, my_pos, adv_pos, max_step)
        if len(all_moves) > 1:
            index = random.randint(0,len(all_moves) - 1)
            move, dir = all_moves[index]
        else:
            move, dir = all_moves[0]

        return move, dir

    def findAllMoves(self, chess_board, my_pos, adv_pos, max_step):
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        # BFS
        cur_step = 0
        # queue to store position and step
        state_queue = deque()
        state_queue.append((my_pos, 0))
        # visited keeps track of visited cases
        visited = {tuple(my_pos)}
        # all_moves is a list of all moves
        all_moves = []

        for dir in range(4):
            if not chess_board[my_pos[0]][my_pos[1]][dir]:
                all_moves.append((my_pos, dir)) 

        # iterate till max step is reached
        while state_queue:

            cur_pos, cur_step = state_queue.popleft()
            r, c = cur_pos

            if cur_step >= max_step:
                break

            # checks all moves u,r,d,l
            # checks all dir for wall
            for direction, move in enumerate(moves):
                
                # checks if there is wall
                blocked = chess_board[cur_pos[0], cur_pos[1], direction]
                if blocked:
                    continue

                # next position
                next_pos = (cur_pos[0] + move[0], cur_pos[1] + move[1])
                x, y = next_pos

                # skip next position if not valid move or already visited
                if next_pos == adv_pos or tuple(next_pos) in visited:
                    continue

                # check if position is valid
                in_bound = 0 <= x < chess_board.shape[0] and 0 <= y < chess_board.shape[1]

                if in_bound:

                    for dir in range(4):
                        if not chess_board[x][y][dir]:
                            all_moves.append(((x, y), dir))       

                # update queue and visited positions
                visited.add(tuple(next_pos))
                state_queue.append((next_pos, cur_step + 1))

        return all_moves