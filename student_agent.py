# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys


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

    def step(self, chess_board, my_pos, adv_pos, max_step):
        # Moves (Up, Right, Down, Left)
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))

        # Opposite Directions
        opposites = {0: 2, 1: 3, 2: 0, 3: 1}



        # dummy return
        return my_pos, dir

    def findAllMoves(self,chess_board, my_pos, adv_pos, max_step):
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        # BFS
        cur_step = 0
        # queue to store position and step
        state_queue = [(my_pos, 0)]
        # visited keeps track of visited cases
        visited = {tuple(my_pos)}

        # checks valid moves within initial position
        all_moves = []
        r, c = my_pos
        for direction in range(4):
            if chess_board[r, c, direction]:
                continue
            else:
                all_moves.append((r, c, direction))
        # iterate till max step is reached
        while cur_step != max_step:
            cur_pos, cur_step = state_queue.pop(0)
            r, c = cur_pos
            # safe break
            if cur_step == max_step:
                break
            # checks all moves u,r,d,l
            # checks all dir for wall
            for move in moves:
                # next position
                next_pos = cur_pos + move
                x, y = next_pos
                for direction in range(4):
                    # checks if there is wall
                    if chess_board[r, c, direction]:
                        continue

                    # skip next position if not valid move or already visited
                    if next_pos == adv_pos or tuple(next_pos) in visited:
                        continue
                    else:
                        all_moves.append((x, y, direction))
                # update queue and visited positions
                visited.add(tuple(next_pos))
                state_queue.append((next_pos, cur_step + 1))
        return all_moves
