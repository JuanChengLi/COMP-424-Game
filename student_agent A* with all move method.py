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
        best_distance = math.dist(my_pos, adv_pos)
        best_move = my_pos

        for move, dir in all_moves:
            x,y = move
            r,c = adv_pos
            distance = math.dist(move, adv_pos)
            if distance < best_distance:
                best_move = move
                best_distance = distance


        # barrier selection

        e_down = adv_pos[0] == best_move[0] + 1 and adv_pos[1] == best_move[1]
        e_up = adv_pos[0] == best_move[0] - 1 and adv_pos[1] == best_move[1]
        e_right = adv_pos[0] == best_move[0] and adv_pos[1] == best_move[1] + 1
        e_left = adv_pos[0] == best_move[0] and adv_pos[1] == best_move[1] - 1

        if e_down and not chess_board [best_move[0],best_move[1], self.dir_map["d"]]:
            dir = self.dir_map["d"]
        
        elif e_up and not chess_board [best_move[0],best_move[1], self.dir_map["u"]]:
            dir = self.dir_map["u"]

        elif e_right and not chess_board [best_move[0],best_move[1], self.dir_map["r"]]:
            dir = self.dir_map["r"]
        
        elif e_left and not chess_board [best_move[0],best_move[1], self.dir_map["l"]]:
            dir = self.dir_map["l"]
        
        else:
            dir = random.randint(0, 3)
            r, c = best_move
            while chess_board[r, c, dir]:
                dir = random.randint(0, 3)

        return best_move, dir

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

    def check_valid_input(self, x, y, dir, x_max, y_max):
        return 0 <= x < x_max and 0 <= y < y_max and dir in self.dir_map

    def check_endgame(self):
        """
        Check if the game ends and compute the current score of the agents.

        Returns
        -------
        is_endgame : bool
            Whether the game ends.
        player_1_score : int
            The score of player 1.
        player_2_score : int
            The score of player 2.
        """
        # Union-Find
        # create the dictionary and initialise all coord to point to their coord
        father = dict()
        for r in range(self.board_size):
            for c in range(self.board_size):
                father[(r, c)] = (r, c)

        # find the position which serves as 1st node, while contracting the graph
        def find(pos):
            if father[pos] != pos:
                father[pos] = find(father[pos])
            return father[pos]

        # point one node to its union
        def union(pos1, pos2):
            father[pos1] = pos2

        for r in range(self.board_size):
            for c in range(self.board_size):
                for dir, move in enumerate(
                    self.moves[1:3]
                ):  # Only check down and right
                    if self.chess_board[r, c, dir + 1]:
                        continue
                    pos_a = find((r, c))
                    pos_b = find((r + move[0], c + move[1]))
                    if pos_a != pos_b:
                        union(pos_a, pos_b)

        for r in range(self.board_size):
            for c in range(self.board_size):
                find((r, c))
        p0_r = find(tuple(self.p0_pos))
        p1_r = find(tuple(self.p1_pos))
        p0_score = list(father.values()).count(p0_r)
        p1_score = list(father.values()).count(p1_r)
        if p0_r == p1_r:
            return False, p0_score, p1_score
        player_win = None
        win_blocks = -1
        if p0_score > p1_score:
            player_win = 0
            win_blocks = p0_score
        elif p0_score < p1_score:
            player_win = 1
            win_blocks = p1_score
        else:
            player_win = -1  # Tie
        return True, p0_score, p1_score
