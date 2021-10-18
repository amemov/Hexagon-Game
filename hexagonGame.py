# Written by Anton Shepelev U28654378 and Andrey Kukushkin U20927418
# for Intro to AI CAP 4621
########################################################
#                   Hexagon Game                       #
########################################################
#     Select player role for AI ( 1 or 2 )             #
#     Input: edge (from, to)                           #
#     Using Alpha-Beta pruning, AI selects the best    #
#      option to win the game                          #
########################################################
#     About game: to win, need to form a triangle,     #
#       a set of 3 edges connected between each other  #
#       Intersections between edges permitted          #
########################################################
class Hexagon_Game:
    # Constructor. Initializes 6x6 adj matrix and set turn to Player 1
    def __init__(self): # 0    1    2    3    4    5
                        # 1    2    3    4    5    6
        self.hexagon = [['X', '.', '.', '.', '.', '.'], #1
                        ['.', 'X', '.', '.', '.', '.'], #2
                        ['.', '.', 'X', '.', '.', '.'], #3
                        ['.', '.', '.', 'X', '.', '.'], #4
                        ['.', '.', '.', '.', 'X', '.'], #5
                        ['.', '.', '.', '.', '.', 'X'],]#6
        self.player_turn = 's'

    # Check if end is reached OR ( all positions in adj matrix filled and no winner )
    def is_end(self):
        temp = 1; s_count = []; d_count = []
        for i in range(0,3):
            s_count.clear(); d_count.clear();
            for j in range(0,6):
                if(self.hexagon[i][j] == '.'):
                    temp = 0
                if(self.hexagon[i][j] == 's'):
                    s_count.append(j)
                if(self.hexagon[i][j] == 'd'):
                    d_count.append(j)
            # Check if counters have at least 2 points. If so, check if triangle base.
            # Otherwise, reset counters
            if (len(s_count) > 1):
                s_won = self.is_triangle(s_count, 's', i)
                if (s_won == True):
                    return 's'
            if (len(d_count) > 1):
                d_won = self.is_triangle(d_count, 'd', i)
                if (d_won == True):
                    return 'd'

        # If matrix is full and no winner
        if(temp == 1):
            return 'X'
        # Game is not over
        else:
            return 'Q'

    # Check for possible triangle edge from is_end
    def is_triangle(self, pos_counter, letter, point):
        # Pick one value and check if it forms an edge with some value in list
        while (len(pos_counter) > 1):
            t = pos_counter.pop(0)
            for i in range(0,len(pos_counter)):
                if(self.hexagon[point][t] == self.hexagon[point][pos_counter[i]]):
                    if (self.hexagon[t][pos_counter[i]] == letter):
                        return True
        return False

    # Input Validaton for moves
    def is_valid(self,x,y):
        if(x>6) or (y>6) or (x<=0) or (y<=0) or (x==y):
            return False
        elif self.hexagon[x-1][y-1] != '.':
            return False
        else:
            return True

    # Reports from where to where goes agent
    def report_hex(self,x,y):
        print("  Chose this edge: ", x,"  ", y)

    # Alpha-Beta Pruning Functions
    def min_alpha(self, alpha, beta, user, AI):
    # Check game status and who might have won
        check = self.is_end()
        # End
        if check == 'X':
            return(0, 0, 0)
        # S won
        if check == 's':
            return (1, 0, 0)
        # D won
        if check == 'd':
            return (-1, 0, 0)

    # Possible values for minimum are:
        # -1  - lost
        #  1  - won
        # -2 indicates worst case scenario:
        minimum = 2
        qx = None
        qy = None
        # Evaluate min alpha beta
        for i in range(0, 3):
            for j in range(0, 6):
                if(self.hexagon[i][j] == '.'):
                    self.hexagon[i][j] = user
                    self.hexagon[j][i] = user
                    (m, max_i, max_j) = self.max_alpha(alpha, beta, user, AI)
                    if m < minimum:
                        minimum = m
                        qx = i
                        qy = j
                    self.hexagon[i][j] = '.'
                    self.hexagon[j][i] = '.'
                    if minimum <= alpha:
                        return (minimum, qx, qy)

                    if minimum < beta:
                        beta = minimum

        return (minimum, qx, qy)


    def max_alpha(self, alpha, beta, user, AI):
    # Check game status and who might have won
        check = self.is_end()
        # End
        if check == 'X':
            return (0, 0, 0)
        # S won
        if check == 's':
            return (1, 0, 0)
        # D won
        if check == 'd':
            return (-1, 0, 0)
    # Possible values for maximum are:
        # -1  - lost
        #  1  - won
        # -2 indicates worst case scenario:
        maximum = -2
        qx = None
        qy = None
        # Evaluate min alpha beta
        for i in range(0, 3):
            for j in range(0, 6):
                if (self.hexagon[i][j] == '.'):
                    self.hexagon[i][j] = AI
                    self.hexagon[j][i] = AI
                    (m, min_i, main_j) = self.min_alpha(alpha, beta, user, AI)
                    if m > maximum:
                        maximum = m
                        qx = i
                        qy = j
                    self.hexagon[i][j] = '.'
                    self.hexagon[j][i] = '.'
                    if maximum >= beta:
                        return (maximum, qx, qy)

                    if maximum > alpha:
                        alpha = maximum

        return (maximum, qx, qy)

def main():
    # Prompt User Player choice ( 1 or 2 )
    print("########################################################\n"
          "#                   Hexagon Game                       #\n"
          "########################################################\n")
    mode = input("Select player for AI (1 or 2): ")
    mode = int(mode)
    while (mode > 2 or mode < 1):
        mode = input("ERROR. Select player for AI (1 or 2): ")
        mode = int(mode)

    game = Hexagon_Game()
    status = 'Q'; move_n = 0;
    if mode == 1:
        while status == 'Q':
            status = game.is_end()
            if (status == 's'):
                print("AI Won. Game Over")
                break
            if (status == 'd'):
                print("Player Won. Game Over")
                break
            if (status == 'X'):
                print("There are no possible moves in hexagon. Tie")
                break
            if game.player_turn == 'd':
                while True:
                    # Prompt edge from user
                    print("\nPlayer move\n")
                    start = int(input("  Line From: "))
                    end = int(input("  To: "))

                    # Check if input in range [1;6]
                    while (start > 6 or start < 1) or (end > 6 or end < 1):
                        print("Value(-s) out of range. Try again")
                        start = int(input("Line From: "))
                        end = int(input("To: "))

                    # Check if user's input is valid for matrix
                    if game.is_valid(start, end):
                        game.hexagon[start-1][end-1] = 'd'
                        game.hexagon[end-1][start-1] = 'd'
                        game.player_turn = 's'
                        break
                    else:
                        print("ERROR. Invalid Line.")
            else:
                print("\nAI move\n")

                # For time optimization, first move of the game predetermined
                # ( pruning itself always chooses this coordinates every time )
                #if(move_n!=0):
                (m, qx, qy) = game.max_alpha(-2, 2, 'd', 's') # s - AI ; d - User
                #else:
                #    move_n = 1; qx = 0; qy = 1

                # if alpha-beta pruning detected end of game
                if(qx == qy):
                    break

                game.hexagon[qx][qy] = 's'
                game.hexagon[qy][qx] = 's'

                # Print AI choice
                game.report_hex(qx + 1, qy + 1)
                game.player_turn = 'd'

                # Print current state of hexagon
                print(game.hexagon)
    else:
        while status == 'Q':
            status = game.is_end()
            if (status == 's'):
                print("Player Won. Game Over")
                break
            if (status == 'd'):
                print("AI Won. Game Over")
                break
            if (status == 'X'):
                print("There are no possible moves in hexagon. Tie")
                break
            if game.player_turn == 's':
                while True:
                    # Prompt edge from user
                    print("\nPlayer move\n")
                    start = int(input("  Line From: "))
                    end = int(input("  To: "))

                    # Check if input in range [1;6]
                    while(start>6 or start<1) or (end>6 or end<1):
                        print("Value(-s) out of range. Try again")
                        start = int(input("Line From: "))
                        end = int(input("To: "))

                    # Check if user's input is valid for matrix
                    if game.is_valid(start, end):
                        game.hexagon[start-1][end-1] = 's'
                        game.hexagon[end-1][start-1] = 's'
                        game.player_turn = 'd'
                        break
                    else:
                        print("ERROR. Invalid Line.")

                    # Check if move resulted in win
                    status = game.is_end()
                    if (status == 's'):
                        print("Player Won. Game Over")
                        break
            else:
                print("\nAI move\n")
                (m, px, py) = game.max_alpha(-2, 2, 's', 'd') # s - user ; d - AI

                # if alpha-beta pruning detected end of game
                if (px == py):
                    break
                game.hexagon[px][py] = 'd'
                game.hexagon[py][px] = 'd'

                # Print AI choice
                game.report_hex(px + 1, py + 1)
                game.player_turn = 's'

                # Print current state of hexagon
                print(game.hexagon)
                
main()