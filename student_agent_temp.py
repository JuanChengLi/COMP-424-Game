# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
# added import
from copy import deepcopy
import random
import math
from collections import deque
import timeit

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

    if p0_r == p1_r:
        # game not finished
        return -1

    p0_score = list(father.values()).count(p0_r)
    p1_score = list(father.values()).count(p1_r)

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

        self.moves = ((-1, 0), (0, 1), (1, 0), (0, -1))

        self.root = None

        self.autoplay = True

    def step(self, chess_board, my_pos, adv_pos, max_step):
        
        #if this is the first move, at the initial state of the board.
        if self.root == None:
            self.root = MonteCarloTreeSearchNode(chess_board, my_pos, adv_pos, max_step)
            self.root.mCTreeSearch()
        return 




class MonteCarloTreeSearchNode():

    """
    Class defining the properties of a MonteCarlo Tree node
    board: state of the chessboard
    parent: parent node of the node, none for root
    children: list of all possible moves
    number_of_visits: number of time a node has been visited
    score: score of the current node
    unvisited_children: list any children nodes that have not been visited yet
    """

    def __init__(self, chessboard, my_pos, adv_pos, dir, max_step, parent = None):
        self.board = chessboard
        self.my_pos = my_pos
        self.adv_pos = adv_pos
        self.dir = dir
        self.max_step = max_step
        self.parent = parent
        self.visited_children = []
        self.children_moves = []
        self.number_of_visits = 0
        self.win = 0
        self.unvisited_children = []

    #overall tree search, return a move and a direction
    def mCTreeSearch (self):

        start = timeit.default_timer()
        stop = timeit.default_timer()

        time_left = 2 - (stop - start)

        #if its the root, get 30 second
        if self.parent == None:
            time_left = 30 - (stop - start)
        
        # simulate while there is time left
        while time_left > 0:

            self.Simulate_Tree()

            stop = timeit.default_timer()
            time_left = 2 - (stop - start)
            if self.parent == None:
                time_left = 30 - (stop - start)
        
        child = self.tree_policy()
        return child.my_pos, child.dirs


    def set_children (self, all_children):
        self.unvisited_children = all_children

    def expand (self):

        all_my_moves = self.findAllMoves(self.chessboard, self.my_pos, self.adv_pos, self.max_step)

        for mymove, mydir in all_my_moves:
            
            newboard = deepcopy(self.chessboard)
            newboard[mymove[0]][mymove[1]][mydir] = True
            childnode = MonteCarloTreeSearchNode(newboard, mymove, self.adv_pos, mydir, self.max_step, parent = self)
            self.unvisited_children.append(childnode)
            self.children_moves.append(mymove)

    #take decision on tree policy or default policy
    def Simulate_Tree(self):

        score = None
        # if not all childrens have been explored, explored 
        if len(self.unvisited_children) > 0:
            score = self.default_policy()
        
        else :
            best_node = self.tree_policy()
            best_node.Simulate_Tree()
        
        if score != None:
            self.raveBackUp(score)


    def tree_policy(self):
        
        # exploration constant
        c = 2

        # best_child = self.visited_children[0]
        # exploitation = self.visited_children[0].win/self.visited_children[0].number_of_visits
        # exploration = c*math.sqrt(math.log(self.number_of_visits)/self.children[0].number_of_visits)

        # get the child that maximise the exploration exploitation score
        best_score = 0
        for child in self.visited_children:

            exploitation = child.win/child.number_of_visits
            exploration = c * math.sqrt(math.log(self.number_of_visits)/child.number_of_visits)
            score = exploitation + exploration
            
            if best_score < score:
                best_score = score
                best_child = child
        
        return best_child


    # choose a random child of the parent to simulate
    def default_policy(self):

        simulated_node = None
        # if there is only one unvisited child left
        if self.unvisited_children.count == 1:
            simulated_node = self.unvisited_children.pop()
            
        
        # pick a random child to visite 
        else:
            index = random.randint(0,len(self.unvisited_children) - 1)
            simulated_node = self.unvisited_children.pop(index)
        
        simulated_node.expand()
        self.visited_children.append(simulated_node)
        score = simulated_node.simulation()
        return score

    # TBD have to be rewritten
    def raveBackUp (self, score):
        
        if self.parent != None:
            parent = self.parent

            if score == 1:
                # TBD redo with dictionary.
                for i, move in enumerate(parent.children_moves):
                    # rave scoring, score all similar nodes
                    if move == self.my_pos:
                        
                        child = parent.unvisited_children.pop(i)
                        child.win = child.win + 1
                        child.number_of_visits = child.number_of_visits + 1
                        parent.visited_children.append(child)

                parent.raveBackUp(score)
        
            else:
                self.number_of_visits = self.number_of_visits + 1
                parent.raveBackUp(score)
            
        else:
            self.number_of_visits = self.number_of_visits + 1

            if score == 1:
                self.win = self.win + 1


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
    
    def simulation (self):
        # initiate/reset variables
        my_pos2 = self.my_pos
        adv_pos2 = self.adv_pos
        chess_board2 = deepcopy(self.board)
        turn = 0
        my_all_moves = []
        adv_all_moves = []
        my_rand_move = ((0, 0), 0)
        adv_rand_move = ((0, 0), 0)
        # update board with my new move
        chess_board2[my_pos2[0], my_pos2[1], self.dir] = True
        # check game status
        game_status = check_endgame(chess_board2, my_pos2, adv_pos2)
        counter = 0
        if game_status > -1:
            return game_status
        """
        simulate the game till game ends
        is_endgame : int
        -1 if game not finished
        0 if adversary agent wins
        1 if my agent wins
        2 if game is a tie
        """
        while game_status < 0:
            counter = counter + 1
            if counter > 1000:
                return 2
            # adv turn
            if turn == 0:
                adv_all_moves = self.findAllMoves(chess_board2, adv_pos2, my_pos2, self.max_step)
                # if no moves, stop simulating
                if len(adv_all_moves) == 0:
                    break
                # choose random move
                adv_rand_move = random.choice(adv_all_moves)
                # update adv move and board
                adv_pos2 = adv_rand_move[0]
                chess_board2[adv_pos2[0], adv_pos2[1], adv_rand_move[1]] = True
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
                my_all_moves = self.findAllMoves(chess_board2, my_pos2, adv_pos2, self.max_step)
                if len(my_all_moves) == 0:
                    break
                my_rand_move = random.choice(my_all_moves)
                my_pos2 = my_rand_move[0]
                chess_board2[my_pos2[0], my_pos2[1], my_rand_move[1]] = True
                game_status = check_endgame(chess_board2, my_pos2, adv_pos2)
                if game_status == 1:
                    wins += 1
                elif game_status == 2:
                    ties += 1
                turn = 4
            # turn = 0 is adv turn
            # turn = 1 is my turn
            turn = turn - 4
        return game_status