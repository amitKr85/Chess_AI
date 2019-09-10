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
    
    
    def __init__(self,color = 'WHITE',set_pos = True):
        self.board = np.zeros((8,8),dtype='int')
        if not (color == 'WHITE' or color == 'BLACK'):
            color = 'WHITE'
        self.color = color
        
        if set_pos:
            self.set_starting_position()
        
    def check_pos(pos,strict=True):
        reg = re.compile('^[A-Ha-h][1-8]$') if strict else re.compile('^[A-Ha-h]?[1-8]?$')
        if reg.match(pos) is not None:
            return True
        else:
            return False
    
    def check_coord(r,c):
        if r<8 and r>=0 and c<8 and c>=0:
            return True
        else:
            return False
    
    # row must be legal [A-Ha-h], returns index value of row
    def parse_row(self,row):
        row = row.upper()
        return 7 - (ord(row) - 49) if self.color == 'WHITE' else ord(row) - 49
    
    # col must be legal [1-8], return index value of column
    def parse_col(self,col):
        col = col.upper()
        return ord(col) - 65 if self.color == 'WHITE' else 7 - (ord(col) - 65)
    
    def parse_pos(self,pos,strict=True):
        if not ChessBoard.check_pos(pos,strict):
            return -1,-1 # for invalid position 
        if strict:
            row = self.parse_row(pos[1])
            col = self.parse_col(pos[0])
        else:
            m = re.compile(r'^([A-Ha-h])?([1-8])?$').match(pos)
            col = -1 if m.group(1) is None else self.parse_col(m.group(1))
            row = -1 if m.group(2) is None else self.parse_row(m.group(2))
#        pos = pos.upper()
#        # pos : 'A1' piece : 1
#        if self.color == 'WHITE':
#            col = ord(pos[0]) - 65
#            row = 7 - (ord(pos[1]) - 49)
#        else:
#            col = 7 - (ord(pos[0]) - 65)
#            row = ord(pos[1]) - 49
        return row,col
    
    # to put a piece in given location
    def put(self,pos,piece):
        row,col = self.parse_pos(pos)
        self.put_at(row,col,piece)
    
    # to get a piece from given location
    def get(self,pos):
        row,col = self.parse_pos(pos)
        return self.get_at(row,col)
    
    # to clear a piece or clear_all if none param. is given
    def clear(self,pos=None):
        if pos is None:
            self.board = np.zeros((8,8),dtype='int')
            return
        row,col = self.parse_pos(pos)
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
    
    # to print board
    def get_snapshot(self):
        return ChessBoard.PIECES[self.board]
        # to append m in front of movable pieces
#        ss = np.empty(self.board.shape,dtype='<U3')
#        for i in range(self.board.shape[0]):
#            for j in range(self.board.shape[0]):
#                tag = ChessBoard.PIECES[self.board[i,j]]
#                if self.is_movable(i,j):
#                    tag = tag+'m'
#                ss[i,j] = tag
#        return ss
        
        
    def set_starting_position(self):
        pieces = np.array([1,2,3,4,5,3,2,1])
        
        if self.color == 'WHITE':
            self.board[0] = pieces + 6
            self.board[1] = np.full(8,12)
            self.board[-1] = pieces
            self.board[-2] = np.full(8,6)
        else:
            self.board[0] = pieces[::-1]
            self.board[1] = np.full(8,6)
            self.board[-1] = pieces[::-1] + 6
            self.board[-2] = np.full(8,12)
            
        # Setting LeftRook and RightRook State, Castling State
        # doing left,right instead of kingRook,QueenRook is easy
        self.has_lrook_moved = self.has_rrook_moved = False
        self.can_castling = True
            
        print(self.board)
    
    def is_movable(self,r,c):
        if not ChessBoard.check_coord(r,c):
            return False
#        if self.board[r,c] == 0:
#            return False
        # can't move
        flag = False
        
        if self.color=='WHITE' and self.board[r,c]<7 and self.board[r,c] != 0:
            # is piece is not a Pawn
            if self.board[r,c] != 6:
                for i,j in ChessBoard.moves[self.board[r,c]]:
                    if ChessBoard.check_coord(r+i,c+j):
                        # if blank or oppenent's
                        if self.board[r+i,c+j] == 0 or self.board[r+i,c+j]>6:
                            flag = True
                            break
            else:
                # considering pawn will not present at first row, r-1 will always < 8
                # if fornt is blank or corner pieces are opponent's
                if self.board[r-1,c] == 0 or (ChessBoard.check_coord(r-1,c+1) and self.board[r-1,c+1]>6) or (ChessBoard.check_coord(r-1,c-1) and self.board[r-1,c-1]>6):
                    flag = True
        elif self.color!='WHITE' and self.board[r,c]>6:
            # is piece is not a Pawn
            if self.board[r,c] != 12:
                for i,j in ChessBoard.moves[self.board[r,c]-6]:
                    if ChessBoard.check_coord(r+i,c+j):
                        # if blank or oppenent's
                        if self.board[r+i,c+j] < 7:
                            flag = True
                            break
            else:
                # considering pawn will not present at first row, r-1 will always < 8
                # if fornt is blank or corner pieces are opponent's
                if self.board[r-1,c] == 0 or (ChessBoard.check_coord(r-1,c+1) and self.board[r-1,c+1]<7 and self.board[r-1,c+1]!=0) or (ChessBoard.check_coord(r-1,c-1) and self.board[r-1,c-1]<7 and self.board[r-1,c-1]!=0):
                    flag = True
        return flag
        
    def get_movable_pos(self):
        movable = np.full(self.board.shape,False)
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                movable[i,j] = self.is_movable(i,j)
        return movable
    
    # return tuples of coordinates where piece can attack
    def get_attack_of(self,r,c):
        if not ChessBoard.check_coord(r,c) or self.board[r,c] == 0:
            return []
        # list of coords
        coords = []
        
        if self.board[r,c] > 6:
            piece = self.board[r,c]-6
            enm = list(range(1,7))
            own = list(range(7,13))
        else:
            piece = self.board[r,c]
            own = list(range(1,7)) # our pieces
            enm = list(range(7,13)) # enemy pieces
        
        # if not pawn
        if piece != 6:
            for direction in ChessBoard.moves[piece]:
                tempr, tempc = r, c
                for i in range(ChessBoard.moves_rng[piece]):
                    tempr, tempc = tempr + direction[0], tempc + direction[1]
                    
                    # if out of the board
                    if not ChessBoard.check_coord(tempr,tempc):
                        break
                    # if empty then add coord
                    if self.board[tempr,tempc] == 0:
                        coords.append((tempr,tempc))
                    # if own piece or opponent's piece then add current and break
                    else:
                        coords.append((tempr,tempc))
                        break
        # if piece is pawn
        else:
            # to get pawn direction
            if (self.color=='WHITE' and self.board[r,c]==6) or (self.color!='WHITE' and self.board[r,c]==12):
                r_ = -1
            else:
                r_ = 1
            if ChessBoard.check_coord(r + r_,c-1) and self.board[r + r_,c-1] not in own:
                coords.append((r + r_,c-1))
            if ChessBoard.check_coord(r + r_,c+1) and self.board[r + r_,c+1] not in own:
                coords.append((r + r_,c+1))
        
        return coords
    
    def get_strength(self):
        strength = np.zeros(self.board.shape)
        if self.color == 'WHITE':
            own = list(range(1,7)) # our pieces
            enm = list(range(7,13)) # enemy pieces
        else:
            enm = list(range(1,7))
            own = list(range(7,13))

        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i,j] in own:
                    coords = self.get_attack_of(i,j)
                    for r, c in coords:
                        strength[r,c] += 1
        return strength
    
    def get_weakness(self):
        weak = np.zeros(self.board.shape)
        if self.color == 'WHITE':
            own = list(range(1,7)) # our pieces
            enm = list(range(7,13)) # enemy pieces
        else:
            enm = list(range(1,7))
            own = list(range(7,13))

        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i,j] in enm:
                    coords = self.get_attack_of(i,j)
                    for r, c in coords:
                        weak[r,c] += 1
        return weak
                
    
    """TODO: test everything and castling"""
    # returns tuples of coordinates where piece can move
    def get_path_of(self,r,c):
        if not self.is_movable(r,c):
            return []
        # list of coords
        path = []
        if self.color == 'WHITE':
            own = list(range(1,7)) # our pieces
            enm = list(range(7,13)) # enemy pieces
            piece = self.board[r,c]
        else:
            enm = list(range(1,7))
            own = list(range(7,13))
            piece = self.board[r,c]-6
        
        # if not pawn
        if piece != 6:
            # to get attk zone that will help in considering king's path
            if piece == 5:
                attk_zone = self.get_weakness()
            for direction in ChessBoard.moves[piece]:
                tempr, tempc = r, c
                for i in range(ChessBoard.moves_rng[piece]):
                    tempr, tempc = tempr + direction[0], tempc + direction[1]
                    
                    # if out of the board
                    if not ChessBoard.check_coord(tempr,tempc):
                        break
                    # if empty then add coord
                    if self.board[tempr,tempc] == 0:
                        if piece!=5 or (piece == 5 and attk_zone[tempr,tempc] == 0):
                            path.append((tempr,tempc))
                        # if piece is king, cheking for castling
                        if piece == 5 and self.can_castling:
                            if not self.has_lrook_moved and ( (self.color,tempr,tempc) == ('WHITE',7,3) or (self.color,tempr,tempc) == ('BLACK',7,2) ):
                                # check left block and if color is white, check further left side block
                                if self.board[tempr,tempc-1] == 0 and ((self.color,self.board[tempr,tempc-2])==('WHITE',0) or self.color!='WHITE'):
                                    # king is not getting attacked in way
                                    if (attk_zone[7,tempc+1],attk_zone[7,tempc],attk_zone[7,tempc-1]) == (0,0,0):
                                        path.append((tempr,tempc-1))
                            if not self.has_rrook_moved and ( (self.color,tempr,tempc) == ('WHITE',7,5) or (self.color,tempr,tempc) == ('BLACK',7,4) ):
                                # check right block and if color is black, check further right side block
                                if self.board[tempr,tempc+1] == 0 and ((self.color,self.board[tempr,tempc+2])==('BLACK',0) or self.color=='WHITE'):
                                    # king is not getting attacked in way
                                    if (attk_zone[7,tempc+1],attk_zone[7,tempc],attk_zone[7,tempc-1]) == (0,0,0):
                                        path.append((tempr,tempc+1))
                    # if own piece then break
                    elif self.board[tempr,tempc] in own:
                        break
                    # else opponents piece, add current and break
                    else:
                        # if piece is king then he can't attck the opponent who is backed-up by someone
                        if piece!=5 or (piece == 5 and attk_zone[tempr,tempc] == 0):
                            path.append((tempr,tempc))
                        break
        # if piece is pawn
        else:
            if self.board[r-1,c] == 0:
                path.append((r-1,c))
                # if Pawn at starting pos. and check if 2-step is available
                if r==6 and self.board[r-2,c] == 0:
                    path.append((r-2,c))
            if ChessBoard.check_coord(r-1,c-1) and self.board[r-1,c-1] in enm:
                path.append((r-1,c-1))
            if ChessBoard.check_coord(r-1,c+1) and self.board[r-1,c+1] in enm:
                path.append((r-1,c+1))
        
        return path        
    
    # will return piece_val, current_row,col, to_row,col
    def parse_move(self,move,color):
        # verify/analyze patten at https://www.regex101.com
        pattern = r'([RNBQK]?)([a-h]?)([1-8]?)x?([a-h][1-8])=?([RNBQ]?)([\+\?\-!#=]{,2})'
        regex = re.compile(pattern)
        match = regex.match(move)
        if match is None:
            raise Exception("invalid move (syntax doesn't matched)")
#            return -1, -1,-1, -1,-1
        c = 'W' if color == 'WHITE' else 'B'
        # if pawn
        if match.group(1) == '':
            piece_val = np.argwhere(ChessBoard.PIECES == (c+'P'))[0,0]
        else:    
            piece_val = np.argwhere(ChessBoard.PIECES == (c+match.group(1)))[0,0]
        # current row,col
        r1,c1 = self.parse_pos(match.group(2)+match.group(3),strict=False)
        # moved to row,col
        r2,c2 = self.parse_pos(match.group(4))
        
        print(f'parsed_move:{piece_val}:{r1},{c1}:{r2},{c2}')
        return piece_val, r1,c1, r2,c2
    
    # move the piece and return moved_pos
    def move_piece(self, piece, r1,c1, r2,c2):
        # finding positions of the piece
        piece_pos = np.argwhere(self.board == piece)
        print(piece_pos, piece, r1,c1, r2,c2)
        # position of available pieces
        avail_pieces = []
        # finding which pieces can move to target coordinates
        for i in range(piece_pos.shape[0]):
            path = self.get_path_of(piece_pos[i,0],piece_pos[i,1])
            if (r2,c2) in path:
                avail_pieces.append((piece_pos[i,0],piece_pos[i,1]))
        if len(avail_pieces) == 0:
            raise Exception("invalid move (no one can reach the target pos)")
        elif len(avail_pieces) == 1:
            self.transact(avail_pieces[0][0],avail_pieces[0][1], r2,c2)
            return avail_pieces[0][0], avail_pieces[0][1]
        # if ambiguity between pieces (which piece to move)
        else:
            # removing pieces whose row doesn't match
            if r1 != -1:
                for tup in avail_pieces:
                    if tup[0] != r1:
                        avail_pieces.remove(tup)
            # removing pieces whose col. doesn't match
            if c1 != -1:
                for tup in avail_pieces:
                    if tup[1] != r1:
                        avail_pieces.remove(tup)
            # if still ambiguity throw error else transact
            # specified current pos doesnt match
            if len(avail_pieces) == 0:
                raise Exception("invalid move (no one at specified current pos that can reach target pos)")
            elif len(avail_pieces) == 1:
                self.transact(avail_pieces[0][0],avail_pieces[0][1], r2,c2)
                return avail_pieces[0][0], avail_pieces[0][1]
            else:
                raise Exception(f"ambiguity between pieces at pos: {avail_pieces}")
    
    """TODO: test"""
    # returns vector of movement for project
    # format: 1st 64 for current, next 64 for target
    def move_own(self,move):
        piece, r1,c1, r2,c2 = self.parse_move(move,self.color)
        # move piece and get moved_pos
        r1,c1 = self.move_piece(piece, r1,c1, r2,c2)
        # mirror pos if color is BLACK
        if self.color != 'WHITE':
            c,t = self.mirror_pos([(r1,c1),(r2,c2)])
            r1,c1 = c
            r2,c2 = t
        vec = np.zeros(128, dtype='int')
        vec[8*r1+c1] = 1
        vec[64 + 8*r2+c2] = 1
        return vec
    
    """TODO: test"""
    def move_opp(self,move):
        piece, r1,c1, r2,c2 = self.parse_move(move, 'BLACK' if self.color == 'WHITE' else 'WHITE')
        self.move_piece(piece, r1,c1, r2,c2)
        
    # returns vector of positions of pieces 
    # format: 1st 64 for rook, next 64 for bishop and so on
    # format: 1st 6*64 for own pieces next 6*64 for opponents pieces
    def get_snapshot_vector(self):
        pos = np.zeros(12*64, dtype='int')
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i,j] > 0:
                    if self.color == 'WHITE':
                        pos[ int(64 * (self.board[i,j]-1) + 8*i+j) ] = 1
                    else:
                        # if black then coord vertically symmetric from center
                        if self.board[i,j] > 6:
                            pos[ int(64 * (self.board[i,j]-7) + 8*i+(7-j))] = 1
                        else:
                            pos[ int(6*64 + 64 * (self.board[i,j]-1) + 8*i+(7-j))] = 1
        return pos
    
    # mirror list of position, center vertical line as pivot
    def mirror_pos(self,position_list):
        mirrored_list = []
        for pos in position_list:
            mirrored_list.append((pos[0],7-pos[1]))
        return mirrored_list
        

def verify(pos,color='WHITE'):
    b=ChessBoard(color=color,set_pos=False)
    for i in range(pos.shape[0]):
        if pos[i] == 1:
            if color == 'WHITE':
                p = i//64 + 1
                c = (i%64)%8
            else:
                if i<6*64:
                    p = i//64 + 7
                else:
                    p = i//64 - 5
                c = 7-(i%64)%8
                    
            r = (i%64)//8
            b.put_at(r,c,p)
    print(b.get_snapshot())