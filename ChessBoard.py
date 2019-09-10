# -*- coding: utf-8 -*-
"""
Created on Fri May 10 18:11:27 2019

@author: AMIT
"""

import numpy as np
import re

class ChessBoard:
    
    WHITE = 1
    BLACK = 2
    # direction of propogation white: up(-1) , black: down(1) 
    PROPG = {'WHITE':-1,'BLACK':1}
    PIECES = np.array(['','WR','WN','WB','WQ','WK','WP','BR','BN','BB','BQ','BK','BP'])
    # least moves/direction for: '',Rook,Knight,Bishop,Queen,King
    moves = {0:[],
             1:[(-1,0),(1,0),(0,-1),(0,1)],
             2:[(-2,-1),(-2,1),(2,-1),(2,1),(-1,-2),(1,-2),(-1,2),(1,2)],
             3:[(-1,-1),(-1,1),(1,-1),(1,1)],
             4:[(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)],
             5:[(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]}
    # max no of times piece can move in its direction
    # notice for King: add your method to add castling move for King
    # notice for Pawn: add your method for Pawn moves
    moves_rng = {0:0,
                 1:7,
                 2:1,
                 3:7,
                 4:7,
                 5:1}
    
    # verify/analyze patten at https://www.regex101.com
    # group1: piece_val
    # group2: current col
    # group3: current row
    # group4: target coordinate (row,col)
    # group5: promotion piece
    # group6: annotations
    move_pattern = r'([RNBQK]?)([a-h]?)([1-8]?)x?([a-h][1-8])=?([RNBQ]?)([\+\?\-!#=]{,2})'
    
    shape = (8,8)
    
    logging = True
    
    @classmethod
    def enable_logs(cls):
        cls.logging = True
    @classmethod
    def disable_logs(cls):
        cls.logging = False
    
    def __init__(self,initialize_board = True):
        self.board = np.zeros((8,8),dtype='int')
        if initialize_board:
            self.set_starting_position()
    
    def assign_players(self, player1, player2):
        if player1.color == player2.color:
            raise Exception("attemp to assign players of same colors")
        self.player_w, self.player_b = (player1,player2) if player1.color == 'WHITE' else (player2,player1)
        self.player_w.assign_board(self)
        self.player_b.assign_board(self)
        
    def set_starting_position(self):
        pieces = np.array([1,2,3,4,5,3,2,1])
        
        self.board[0] = pieces + 6
        self.board[1] = np.full(8,12)
        self.board[-1] = pieces
        self.board[-2] = np.full(8,6)
        
        # setting white's turn
        self.turn = 1
        if ChessBoard.logging:
            print(self.board)
    
    # initialize board with FEN notation
    def initialize_fen(self,fen):
        if not re.compile(r'([RNBQKPrnbqkp1-8]+\/){7}[RNBQKPrnbqkp1-8]+ [wb] (K?Q?k?q?|-) ([a-h][1-8]|-) \d+ \d+').match(fen):
            raise Exception('incorrect FEN notation')
            
        self.board = np.zeros((8,8),dtype='int')
        
        fields = fen.split(' ')
        # parse positions
        p = {'R':1, 'N':2, 'B':3, 'Q':4, 'K':5, 'P':6, 'r':7, 'n':8, 'b':9, 'q':10, 'k':11, 'p':12}
        for i,row in enumerate(fields[0].split('/')):
            j = 0
            for k in row:
                if k.isnumeric():
                    j += int(k)
                else:
                    self.put_at(i,j, p[k])
                    j += 1
        # parseing turn 1 for white, 2 for black
        self.turn = 1 if fields[1] == 'w' else 2
        # parsing castling
        if fields[2] == '-':
            self.player_w.can_castling = False
            self.player_b.can_castling = False
        else:
            if 'K' in fields[2] or 'Q' in fields[2]:
                self.player_w.can_castling = True
                if 'K' in fields[2]:
                    self.player_w.has_rrook_moved = False
                if 'Q' in fields[2]:
                    self.player_w.has_lrook_moved = False
            if 'k' in fields[2] or 'q' in fields[2]:
                self.player_b.can_castling = True
                if 'k' in fields[2]:
                    self.player_b.has_rrook_moved = False
                if 'q' in fields[2]:
                    self.player_b.has_lrook_moved = False
        # parsing en_passant move, setting bait -2 if next turn is WHITE else -1
        if fields[3] != '-':
            self.put(fields[3], -2 if self.turn == 1 else -1)
        # parse halfmoves and full moves
        """TODO: implement"""
    
    # setting who's turn is next
    def turn_made(self,player):
        # black's turn if called by WHITE else white's turn
        self.turn = 2 if player.color == 'WHITE' else 1
        
    def __getitem__(self,i):
        if ChessBoard.check_coord(i[0],i[1]):
            return self.board[i[0],i[1]]
        else:
            raise Exception(f"invalid index [{i[0]},{i[1]}]")
    
    def get_weakness(self,player):
        if player.color == "WHITE":
            return self.player_b.get_strength()
        else:
            return self.player_w.get_strength()
        
    def check_pos(pos,strict=True):
        reg = re.compile('^[A-Ha-h][1-8]$') if strict else re.compile('^[A-Ha-h]?[1-8]?$')
#        print("type:",type(pos))
        if reg.match(pos) is not None:
            return True
        else:
            return False
    
    def check_coord(r,c):
        if r<8 and r>=0 and c<8 and c>=0:
            return True
        else:
            return False
        
     # mirror list of position, center vertical line as pivot
    def mirror_vert_pos(position_list):
        mirrored_list = []
        for pos in position_list:
            mirrored_list.append((pos[0],7-pos[1]))
        return mirrored_list

    # mirror list of position, center horiz. line as pivot
    def mirror_horiz_pos(position_list):
        mirrored_list = []
        for pos in position_list:
            mirrored_list.append((7-pos[0],pos[1]))
        return mirrored_list
    
    def piece_val(piece):
        return (piece-1)%6 + 1
    
    # returns index value of row
    def parse_row(row):
        if re.compile(r'^[1-8]$').match(row) is not None:
            return 7 - (ord(row) - 49)
        else:
            raise Exception(f"invalid row {row}")
    
    # return index value of column
    def parse_col(col):
        if re.compile(r'^[A-Ha-h]$').match(col) is not None:
            col = col.upper()
            return ord(col) - 65
        else:
            raise Exception(f"invalid column {col}")
    
    def parse_pos(pos,strict=True):
        if not ChessBoard.check_pos(pos,strict):
            raise Exception(f"invalid position {pos}, strict={strict}") 
        if strict:
            row = ChessBoard.parse_row(pos[1])
            col = ChessBoard.parse_col(pos[0])
        else:
            m = re.compile(r'^([A-Ha-h])?([1-8])?$').match(pos)
            col = -1 if m.group(1) is None else ChessBoard.parse_col(m.group(1))
            row = -1 if m.group(2) is None else ChessBoard.parse_row(m.group(2))
        return row,col
    
    # return the readable move of given coord move
    def get_move(self,r1,c1, r2,c2):
        suff = chr(ord('a')+c1) + chr(ord('8')-r1) + chr(ord('a')+c2) + chr(ord('8')-r2)
        if ChessBoard.piece_val(self.board[r1,c1]) == 5 and abs(c1-c2)>1:
            if abs(c1-c2)==2:
                return 'O-O'
            else:
                return 'O-O-O'
        if ChessBoard.piece_val(self.board[r1,c1]) == 6:
            return suff
        else:
            return ChessBoard.PIECES[self.board[r1,c1]][1:] + suff
    
    # to put a piece in given location
    def put(self,pos,piece):
        row,col = ChessBoard.parse_pos(pos)
        self.put_at(row,col,piece)
    
    # to get a piece from given location
    def get(self,pos):
        row,col = ChessBoard.parse_pos(pos)
        return self.get_at(row,col)
    
    # to clear a piece or clear_all if none param. is given
    def clear(self,pos=None):
        if pos is None:
            self.board = np.zeros((8,8),dtype='int')
            self.player_w.assign_board(self)
            self.player_b.assign_board(self)
            return
        row,col = ChessBoard.parse_pos(pos)
        self.put_at(row,col,0)
    
    # to put at given coordinate
    def put_at(self,r,c,piece):
        if ChessBoard.check_coord(r,c):
            self.board[r,c] = piece
        else:
            raise Exception("invalid position")
    
    # to get piece from given coordinate
    def get_at(self,r,c):
        if ChessBoard.check_coord(r,c):
            return self.board[r,c]
        else:
            raise Exception("invalid position")
    
    # move piece from given row,col to target row,col
    def transact(self,r,c,tr,tc): 
        piece = self.get_at(r,c)
        self.put_at(tr,tc,piece)
        self.put_at(r,c, 0)
    
    #  adding bait if player's pawn jumps 2 cells, called by players
    def add_bait(self,r,c,player):
        self.put_at(r,c, player.own_bait)
        
    # remove bait called by players after each move to remove opponents bait
    def remove_bait(self,player):
        self.board[self.board == player.enm_bait] = 0
    
    # to print board
    def get_snapshot(self):
        # taking snapshot of pieces without taking any bait
        temp = np.array(self.board,copy=True)
        temp[self.board<0]=0
        return ChessBoard.PIECES[temp]
        # to append m in front of movable pieces
#        ss = np.empty(self.board.shape,dtype='<U3')
#        for i in range(self.board.shape[0]):
#            for j in range(self.board.shape[0]):
#                tag = ChessBoard.PIECES[self.board[i,j]]
#                if self.is_movable(i,j):
#                    tag = tag+'m'
#                ss[i,j] = tag
#        return ss
    
    
    # will return piece_value, current_row,col, to_row,col
    """TODO: test castling move"""
    def parse_move(move,color):
        
        regex = re.compile(ChessBoard.move_pattern)
        match = regex.match(move)
        # if castling move
        if not match and re.compile(r'(O(\-O)?\-O)([\+\?\-!#=]{,2})').match(move):
            r1,c1 = ChessBoard.parse_pos('e1') if color == 'WHITE' else ChessBoard.parse_pos('e8')
            match_c = re.compile(r'(O(\-O)?\-O)([\+\?\-!#=]{,2})').match(move)
            if match_c.group(1) == 'O-O-O':
                c2 = ChessBoard.parse_pos('c',strict=False)[1]
            else:
                c2 = ChessBoard.parse_pos('g',strict=False)[1]
            r2 = r1
            piece_value = np.argwhere(ChessBoard.PIECES == ('WK' if color == 'WHITE' else 'BK'))[0,0]
            if ChessBoard.logging:
                print(f'parsed_move castling:{piece_value}:{r1},{c1}:{r2},{c2}')
            return piece_value, r1,c1, r2,c2
        
        elif not match: 
            raise Exception("invalid move (syntax doesn't matched) "+str(move))
#            return -1, -1,-1, -1,-1
        c = 'W' if color == 'WHITE' else 'B'
        # if pawn
        if match.group(1) == '':
            piece_value = np.argwhere(ChessBoard.PIECES == (c+'P'))[0,0]
        else:    
            piece_value = np.argwhere(ChessBoard.PIECES == (c+match.group(1)))[0,0]
        # current row,col
        r1,c1 = ChessBoard.parse_pos(match.group(2)+match.group(3),strict=False)
        # moved to row,col
        r2,c2 = ChessBoard.parse_pos(match.group(4))
        
        # checking if promoted letter has been specified else raise Error # if print, use logging condition to print
#        print("grp5",type(match.group(5)),match.group(5))
        if ChessBoard.piece_val(piece_value) == 6 and (r2 == 0 or r2 == 7) and not match.group(5):
            raise Exception("promotion piece not specified for the promoted Pawn")
        
        if ChessBoard.logging:
            print(f'parsed_move:{piece_value}:{r1},{c1}:{r2},{c2}')
        return piece_value, r1,c1, r2,c2
    
    # returns vector of movement for project
    # format: 1st 64 for current, next 64 for target
    def get_move_vector(self, player, r1,c1, r2,c2, prom):
        # mirror pos if color is BLACK
        if player.color != 'WHITE':
            c,t = ChessBoard.mirror_horiz_pos([(r1,c1),(r2,c2)])
            r1,c1 = c
            r2,c2 = t
        vec = np.zeros(132, dtype='int8')
        vec[8*r1+c1] = 1
        vec[64 + 8*r2+c2] = 1
        if prom>0:
            vec[127+prom] = 1
        return vec
        
    # returns vector of positions of pieces 
    # format: 1st 64 for rook, next 64 for bishop and so on
    # format: 1st 6*64 for own pieces next 6*64 for opponents pieces
    def get_snapshot_vector(self,player):
        pos = np.zeros(12*64, dtype='int8')
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i,j] > 0:
                    if player.color == 'WHITE':
                        pos[ int(64 * (self.board[i,j]-1) + 8*i+j) ] = 1
                    else:
                        # if black then coord horizontally symmetric from center
                        if self.board[i,j] > 6:
                            pos[ int(64 * (self.board[i,j]-7) + 8*(7-i)+j)] = 1
                        else:
                            pos[ int(6*64 + 64 * (self.board[i,j]-1) + 8*(7-i)+j)] = 1
        return pos
        

#def verify(pos,color='WHITE'):
#    b=ChessBoard(color=color,set_pos=False)
#    for i in range(pos.shape[0]):
#        if pos[i] == 1:
#            if color == 'WHITE':
#                p = i//64 + 1
#                c = (i%64)%8
#            else:
#                if i<6*64:
#                    p = i//64 + 7
#                else:
#                    p = i//64 - 5
#                c = 7-(i%64)%8
#                    
#            r = (i%64)//8
#            b.put_at(r,c,p)
#    print(b.get_snapshot())