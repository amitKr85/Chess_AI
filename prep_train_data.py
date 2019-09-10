# -*- coding: utf-8 -*-
"""
Created on Mon May 20 14:44:27 2019

@author: AMIT
"""
import re 
import numpy as np
import time
from ChessBoard import ChessBoard
from Player import Player


# list of dataset, format: 1st 12*64 cols for snapshot, other 128 cols for movement

# r'([^ ]+)( {[^{}]+})?( \d+\.\.\.)? ([^ ]+)( {[^{}]+})?(( 1\-0)|( 0\-1)|( 1/2\-1/2))?' regex to read matches

datalist = []
begin_t = time.time()
prev_t = time.time()
times = []
games_start = 0
limit = games_limit = 100
logging = True

def print_(*args,**kwargs):
    if logging:
        print(*args,**kwargs)


with open('dataset/lichess_db_standard_rated_2013-01.pgn','r') as file:
#with open('dataset/test.pgn','r') as file:
    while True:
        if games_limit == 0:
            break
        games_limit -= 1
        
        about = dict()
        end_f = True
        print("game",limit-games_limit,end="")
        while True:
            line = file.readline().strip('\n')
            m = re.compile(r'^\[(\w+) \"(.+)\"\]$').match(line)
            if not m:
                break
            print_("parsing meta-data for game",limit-games_limit)
            if games_start <= 0:
                key = m.group(1)
                val = m.group(2)
                about[key] = val
                print_(f'{key}:{val}')
            end_f = False
        
        if end_f:
            print_("end of file")
            break
        
        if games_start <= 0:
            if about["Result"] == "1-0":
                white_wins = True
            elif about["Result"] == "0-1":
                white_wins = False
            elif about["Result"] == "1/2-1/2":
                try:
                    if int(about["WhiteElo"]) >= int(about["BlackElo"]):
                        white_wins = True
                    else:
                        white_wins = False
                except:
                    # if invaid data '?' occured in either of Elo
                    if about["WhiteElo"].isdigit():
                        white_wins = True
                    else:
                        white_wins = False
            
            p1 = Player()
            p2 = Player('BLACK')
            cb = ChessBoard()
            cb.assign_players(p1,p2)
            
            if logging:
                Player.enable_logs()
                ChessBoard.enable_logs()
            else:
                Player.disable_logs()
                ChessBoard.disable_logs()
#        player = p1 if white_wins else p2
        
        while True:
            line = file.readline().strip('\n')
            if games_start > 0:
                file.readline()
                games_start -= 1
                print("-skipped")
                break
            if not line:
                break
            print("-parsing")
            print_("parsing moves for game",limit-games_limit)
            moves = re.split(r'\b\d+\. ',line)
            print_(moves)
            end_f = False
            if moves:
                for move in moves:
                    if move:
                        if move == moves[-1]:
                            last = True
                        else:
                            last = False
#                        w_b_move = move.strip().split()
                        move_match = re.compile(r'([^ ]+)( {[^{}]+})?( \d+\.\.\.)? ([^ ]+)( {[^{}]+})?(( 1\-0)|( 0\-1)|( 1/2\-1/2))?').match(move.strip())
                        w_b_move = [move_match.group(1), move_match.group(4), move_match.group(6)]
                        row = []
                        # white move
                        print_("white move:",w_b_move[0])
                        if white_wins:
                            row.append(p1.get_snapshot_vector())
                            r1,c1, r2,c2, prom = p1.make_move(w_b_move[0])
                            row.append(p1.get_move_vector(r1,c1, r2,c2, prom))
                        else:
                            p1.make_move(w_b_move[0])
                        
                        if last and w_b_move[1] in ["0-1","1-0","1/2-1/2"]:
                            print_(w_b_move[1])
                            break
                        
                        # black move
                        print_("black move:",w_b_move[1])
                        if not white_wins:
                            row.append(p2.get_snapshot_vector())
                            r1,c1, r2,c2, prom = p2.make_move(w_b_move[1])
                            row.append(p2.get_move_vector(r1,c1, r2,c2, prom))
                        else:
                            p2.make_move(w_b_move[1])
                        
                        datalist.append(np.concatenate(row))
                        
                        if last:
                            print_(w_b_move[2])
                        else:
                            print_()
        
        times.append(time.time()-prev_t)
        prev_t = time.time()
        print_("the game took",times[-1],"secs")

end_t = time.time()
print("total time taken",end_t-begin_t,"sec")
print("avg time taken",sum(times)/len(times))
datalist_np = np.stack(datalist)
