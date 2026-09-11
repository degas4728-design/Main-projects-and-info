from domain.service.service import GameService
from datasource.repository.repository import Gamerepository

class Gamelogic(GameService):

    def __init__(self, repository):
        self.repository = repository
        self.last_valid_field = None

    def _is_full(self, field):
        status = True

        for i in field:
            for j in i:
                if j == 0:
                    status = False
                    break
            if status == False:
                break
        return status

    def _is_win(self, field, player):
        win = False
        count_char_v,count_char_g,count_char_pu,count_char_lu  = 0, 0, 0, 0
        global_break = 0
        for i in range(3):
            for j in range(3):
                if field[i][j] == player:
                    count_char_g = count_char_g + 1
                if field[j][i] == player:
                    count_char_v = count_char_v + 1
                if count_char_v == 3 or count_char_g == 3:
                    win = True
                    global_break = 1
                    break
            count_char_v, count_char_g = 0, 0
            if global_break == 1:break

        for i in range(3):
            if field[i][i] == player:
                count_char_pu = count_char_pu + 1
            if count_char_pu == 3:
                win = True
                break
        global_break = 0
        if field[0][2] == player and field[1][1] == player and field[2][0] == player:
            win = True
        return win
        
    def _minimax(self, field, dp ,comp):
        if self._is_win(field, 2) == True:
            return 1, dp
        if self._is_win(field, 1) == True:
            return -1, dp
        if self._is_full(field):
            return 0, dp
        
        
        if comp == True:
            b_score = -10 ** 9
            for i in range(len(field)):
                for j in range(len(field)):
                    if field[i][j] == 0:
                        field[i][j] = 2
                        ls = self._minimax(field, dp+1, False)
                        score = ls[0]
                        dp = ls[1]
                        field[i][j] = 0
                        if score > b_score:
                            b_score = score
        if comp == False:
            b_score = 10**9 
            for i in range(len(field)):
                for j in range(len(field)):
                    if field[i][j] == 0:
                        field[i][j] = 1
                        ls = self._minimax(field, dp+1, True)
                        score = ls[0]
                        dp = ls[1]
                        field[i][j] = 0
                        if score < b_score:
                            b_score = score


        return [b_score, dp]

    def comp_motion(self, field):
        move = None
        b_score = -10**9 
        score, dp = 0,0
        best_dp = 10**9 
        copy_field = [0,0,0]
        for i in range(len(field)):copy_field[i] = field[i].copy()

        for i in range(len(copy_field)):
            for j in range(len(copy_field)):
                if copy_field[i][j] == 0:
                    copy_field[i][j] = 2
                    ls = self._minimax(copy_field, 0,False)
                    score = ls[0]
                    dp = ls[1]
                    copy_field[i][j] = 0
                    if score > b_score and dp < best_dp: 
                        b_score = score
                        best_dp = dp
                        move = [i,j]

        field[move[0]][move[1]] = 2

    def is_end(self, field): 
        status = False
        if self._is_win(field,1) == True or self._is_win(field,2) == True:
            status = True
        if self._is_full(field) == True:
            status = True
        
        return status

    def valid_field(self, game , past_field):
        status = True
        for i in range(3):
            for j in range(3):
                if past_field[i][j] == 2:
                    if game.field.matrix[i][j] != 2:
                        status = False                
        return status
    

