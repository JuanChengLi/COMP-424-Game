# Student agent: Add your own agent here
import math
import random

from agents.agent import Agent
from store import register_agent
import sys
# prof allows on Ed
from copy import deepcopy
from collections import deque

def simulation (n, chess_board, my_pos, my_dir, adv_pos, max_step):
    wins = 0
    ties = 0
    # n number of simulations
    for i in range(n):
        # initiate/reset variables
        my_pos2 = my_pos
        adv_pos2 = adv_pos
        chess_board2 = deepcopy(chess_board)
        turn = 0
        my_all_moves = []
        adv_all_moves = []
        my_rand_move = ((0, 0), 0)
        adv_rand_move = ((0, 0), 0)
        # update board with my new move
        chess_board2[my_pos2[0], my_pos2[1], my_dir] = True
        # check game status
        game_status = check_endgame(chess_board2, my_pos2, adv_pos2)
        if game_status > -1:
            return wins, ties, n
        """
        simulate the game till game ends
        is_endgame : int
        -1 if game not finished
        0 if adversary agent wins
        1 if my agent wins
        2 if game is a tie
        """
        while game_status < 0:
            # adv turn
            if turn == 0:
                adv_all_moves = findAllMoves(chess_board2, adv_pos2, my_pos2, max_step)
                # if no moves, stop simulating
                if len(adv_all_moves) == 0:
                    break
                # choose random move
                adv_rand_move = random.choice(adv_all_moves)
                # update adv move and board
                adv_pos2 = adv_rand_move[0]
                chess_board2[adv_pos2[0], adv_pos2[0], adv_rand_move[1]] = True
                # check game status and update
                game_status = check_endgame(chess_board2, my_pos2, adv_pos2)
                if game_status == 1:
                    wins += 1
                elif game_status == 2:
                    ties += 1
                # set temp turn to not enter next if statement
                turn = 5
            # my turn
            if turn == 1:
                my_all_moves = findAllMoves(chess_board2, my_pos2, adv_pos2, max_step)
                if len(my_all_moves) == 0:
                    break
                my_rand_move = random.choice(my_all_moves)
                my_pos2 = my_rand_move[0]
                chess_board2[my_pos2[0], my_pos2[0], my_rand_move[1]] == True
                game_status = check_endgame(chess_board2, my_pos2, adv_pos2)
                if game_status == 1:
                    wins += 1
                elif game_status == 2:
                    ties += 1
                turn = 4
            # turn = 0 is adv turn
            # turn = 1 is my turn
            turn = turn - 4
    return wins, ties, n



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



def findAllMoves(chess_board, my_pos, adv_pos, max_step):
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
                all_moves.append(((x, y), direction))

            # update queue and visited positions
            visited.add(tuple(next_pos))
            state_queue.append((next_pos, cur_step + 1))

    return all_moves


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
        self.autoplay = True

    def step(self, chess_board, my_pos, adv_pos, max_step):
        # Moves (Up, Right, Down, Left)
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        all_moves = self.findAllMoves(chess_board, my_pos, adv_pos, max_step)
        simulated_games = []
        for move in all_moves:
            pos, direction = move
            new_board = next_board(chess_board, pos, direction)
            game_state = check_endgame(new_board, pos, adv_pos)
            if game_state == 1:
                return pos, direction
            win, tie, n = simulation(5, chess_board, pos, direction, adv_pos, max_step)
            simulated_games.append(win)
        best_move = simulated_games.index(max(simulated_games))
        # dummy return
        return all_moves[best_move][0], all_moves[best_move][1]

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
                    all_moves.append(((x, y), direction))

                # update queue and visited positions
                visited.add(tuple(next_pos))
                state_queue.append((next_pos, cur_step + 1))

        return all_moves