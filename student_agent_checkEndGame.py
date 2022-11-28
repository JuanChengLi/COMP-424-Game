# Student agent: Add your own agent here
import math

from agents.agent import Agent
from store import register_agent
import sys
# prof allows on Ed
from copy import deepcopy


def next_board(chess_board, next_pos, direction):
    new_board = deepcopy(chess_board)
    r, c = next_pos
    new_board[r, c, direction] = True
    return new_board


def distance(my_pos, adv_pos):
    return math.sqrt((my_pos[0] - adv_pos[0]) ** 2 + (my_pos[1] - adv_pos[1]) ** 2)


def check_endgame(chess_board, my_pos, adv_pos):
    """
    Check if the game ends and compute the current score of the agents.

    Returns
    -------
    is_endgame : int
        -1 if game not finished
        0 if adversary agent wins
        1 if my agent wins
        2 if game is a tie
    player_scores : int
        p0_score is adversary agent score
        p1_score is my agent score
    """
    # Union-Find
    father = dict()
    board_size = chess_board.shape[0]
    # Moves (Up, Right, Down, Left)
    moves = ((-1, 0), (0, 1), (1, 0), (0, -1))

    for r in range(board_size):
        for c in range(board_size):
            father[(r, c)] = (r, c)

    def find(pos):
        if father[pos] != pos:
            father[pos] = find(father[pos])
        return father[pos]

    def union(pos1, pos2):
        father[pos1] = pos2

    for r in range(board_size):
        for c in range(board_size):
            for direction, move in enumerate(moves[1:3]):
                # Only check down and right
                if chess_board[r, c, direction + 1]:
                    continue
                pos_a = find((r, c))
                pos_b = find((r + move[0], c + move[1]))
                if pos_a != pos_b:
                    union(pos_a, pos_b)

    for r in range(board_size):
        for c in range(board_size):
            find((r, c))
    # P1 is my_pos
    # P0 is adv_pos
    p0_r = find(tuple(adv_pos))
    p1_r = find(tuple(my_pos))
    p0_score = list(father.values()).count(p0_r)
    p1_score = list(father.values()).count(p1_r)
    if p0_r == p1_r:
        # game not finished
        return -1
    player_win = None
    win_blocks = -1
    if p0_score > p1_score:
        player_win = 0
        win_blocks = p0_score
    elif p0_score < p1_score:
        player_win = 1
        win_blocks = p1_score
    else:
        player_win = 2  # Tie
    return player_win


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
        all_moves = self.findAllMoves(chess_board, my_pos, adv_pos, max_step)
        my_pos = (all_moves[-1][0], all_moves[-1][1])
        dir = all_moves[-1][2]
        for move in all_moves:
            r, c, direction = move
            new_board = next_board(chess_board, (r, c), direction)
            game_state = check_endgame(new_board, (r, c), adv_pos)
            if game_state == 1:
                my_pos = (r, c)
                dir = direction
        # dummy return
        return my_pos, dir

    def findAllMoves(self, chess_board, my_pos, adv_pos, max_step):
        """
            find all possible moves of the agent using BFS
            Returns
            -------
            r, c, direction
        """
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
            for direction, move in enumerate(moves):
                # next position
                next_pos = (cur_pos[0] + move[0], cur_pos[1] + move[1])
                x, y = next_pos
                if 0 < x < chess_board.shape[0] and 0 < y < chess_board.shape[1]:
                    # checks if there is wall
                    if chess_board[x, y, direction]:
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
