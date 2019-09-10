# -*- coding: utf-8 -*-
"""
Created on Sat May 18 14:33:41 2019

@author: AMIT
"""
import numpy as np
import re
from ChessBoard import ChessBoard

class Player:
    
    logging = True
    @classmethod
    def enable_logs(cls):
        cls.logging = True
    @classmethod
    def disable_logs(cls):
        cls.logging = False
        
    
    def __init__(self,color='WHITE'):
        # color value should be 'WHITE' or 'BLACK'
        self.color = color if color == 'WHITE' or color == 'BLACK' else 'WHITE'
        # setting own and enemy pieces
        self.own, self.enm = (np.arange(1,7),np.arange(7,13)) if self.color == 'WHITE' else (np.arange(7,13),np.arange(1,7))
        # bait value
        self.own_bait, self.enm_bait = (-1,-2) if self.color == 'WHITE' else (-2,-1)
        
    def assign_board(self,board):
        self.board = board
        # Setting LeftRook and RightRook State, Castling State
        # doing left,right instead of kingRook,QueenRook is easy
        self.has_lrook_moved = self.has_rrook_moved = False
        self.can_castling = True
    
    # return Bool depends on the piece at specified position
#    def is_movable(self,r,c):
#        if not ChessBoard.check_coord(r,c):
#            return False
#        
#        # can't move
#        flag = False
#        
#        if self.board[r,c] in self.own:
#            
#            piece_val = ChessBoard.piece_val(self.board[r,c])
#            # is piece is not a Pawn
#            if piece_val != 6:
#                if piece_val == 5:
#                    attk_zone = self.get_weakness()
#                    
#                for i,j in ChessBoard.moves[piece_val]:
#                    if ChessBoard.check_coord(r+i,c+j):
#                        # if blank or oppenent's
#                        if self.board[r+i,c+j] == 0 or self.board[r+i,c+j] in self.enm:
#                            # piece is king and 
#                            if piece_val == 5 and attk_zone[r+i,c+j] !=0 :
#                                continue
#                            flag = True
#                            break
#            else:
#                # considering pawn will not present at promotion row
#                # if fornt is blank or corner pieces are opponent's
#                r_ = ChessBoard.PROPG[self.color]
#                if self.board[r+r_,c] == 0:
#                    flag = True
#                if ChessBoard.check_coord(r+r_,c+1) and (self.board[r+r_,c+1] in self.enm or self.board[r+r_,c+1] == self.enm_bait):
#                    flag = True
#                if ChessBoard.check_coord(r+r_,c-1) and (self.board[r+r_,c-1] in self.enm or self.board[r+r_,c-1] == self.enm_bait):
#                    flag = True
#                
#        return flag
        
    # movable can be np.2D array or can be list of coordinate tuples, returns path for each cell if return_path is True
    def get_movable_pos(self, as_tuple_list=False, return_path=False):
        if as_tuple_list:
            movable = []
        else:
            movable = np.full(self.board.shape,False)
        paths = []
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
#                movable[i,j] = self.is_movable(i,j)
                path = self.get_path_of(i,j)
                if as_tuple_list:
                    if len(path)>0:
                        movable.append((i,j))
                else:
                    movable[i,j] = True if len(path)>0 else False
                if return_path:
                    paths.append(path)
        if return_path:
            return movable, paths
        else:
            return movable
    
    # return tuples of coordinates where piece can attack
    def get_attack_of(self,r,c):
        if not ChessBoard.check_coord(r,c) or self.board[r,c] not in self.own:
            return []
        # list of coords
        coords = []
        
        # translating to 1-6
        piece_val = ChessBoard.piece_val(self.board[r,c])
        
        # if not pawn
        if piece_val != 6:
            for direction in ChessBoard.moves[piece_val]:
                tempr, tempc = r, c
                for i in range(ChessBoard.moves_rng[piece_val]):
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
            r_ = ChessBoard.PROPG[self.color]
            if ChessBoard.check_coord(r + r_,c-1): # and self.board[r + r_,c-1] not in self.own:
                coords.append((r + r_,c-1))
            if ChessBoard.check_coord(r + r_,c+1): # and self.board[r + r_,c+1] not in self.own:
                coords.append((r + r_,c+1))
        
        return coords
    
    def get_strength(self):
        strength = np.zeros(self.board.shape, dtype='int')

        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i,j] in self.own:
                    coords = self.get_attack_of(i,j)
                    for r, c in coords:
                        strength[r,c] += 1
        return strength
    
    def get_weakness(self):
        return self.board.get_weakness(self)
    
    # add corrd to path after checking if king is not in trouble
    def add_coord_to_path(self,path, r1,c1, r2,c2):
        # cheking if the piece captures the bait
        if(ChessBoard.piece_val(self.board[r1,c1])==6 and self.board[r2,c2]==self.enm_bait):
            en_pass_take = True
            # temporary removing enemy pawn that used en_passant and get captured
            self.board.put_at(r1,c2,0)
        else:
            en_pass_take = False
            
        temp_piece = self.board[r2,c2]
        self.board.transact(r1,c1, r2,c2)
        
        attk_zone = self.get_weakness()
        k_val = np.argwhere(ChessBoard.PIECES == ('WK' if self.color == 'WHITE' else 'BK'))[0,0]
#        print(k_val)
        k_pos = np.argwhere(self.board.board == k_val)[0]
#        print(k_pos)
        # if move is not getting king under attack then add path
        if attk_zone[k_pos[0],k_pos[1]] == 0:
#            print("True")
            path.append((r2,c2))
        
        self.board.transact(r2,c2, r1,c1)
        self.board.put_at(r2,c2, temp_piece)
        if en_pass_take:
            # putting the enemy pawn back
            self.board.put_at(r1,c2,12 if self.color == 'WHITE' else 6)
    
    """TODO: test everything and castling"""
    # returns tuples of coordinates where piece can move
    def get_path_of(self,r,c):
        if self.board[r,c] not in self.own:
            return []
        # list of coords
        path = []
        piece_val = ChessBoard.piece_val(self.board[r,c])
        
        # if not pawn
        if piece_val != 6:
            # to get attk zone that will help in considering king's path
            if piece_val == 5:
                attk_zone = self.get_weakness()
            for direction in ChessBoard.moves[piece_val]:
                tempr, tempc = r, c
                for i in range(ChessBoard.moves_rng[piece_val]):
                    tempr, tempc = tempr + direction[0], tempc + direction[1]
                    
                    # if out of the board
                    if not ChessBoard.check_coord(tempr,tempc):
                        break
                    # if empty/bait then add coord
                    if self.board[tempr,tempc] <= 0:
#                        if piece_val!=5 or (piece_val == 5 and attk_zone[tempr,tempc] == 0):
#                            path.append((tempr,tempc))
                        # taking care if king is not in trouble
                        self.add_coord_to_path(path, r,c, tempr,tempc)
                        
                        # if piece is king, cheking for castling
                        if piece_val == 5 and self.can_castling:
                            if not self.has_lrook_moved and ( (self.color,tempr,tempc) == ('WHITE',7,3) or (self.color,tempr,tempc) == ('BLACK',0,3) ):
                                # check left block and futher left side block for empty
                                if self.board[tempr,tempc-1] == 0 and self.board[tempr,tempc-2] == 0:
                                    # king is not getting attacked in way
                                    if (attk_zone[tempr,tempc+1],attk_zone[tempr,tempc],attk_zone[tempr,tempc-1]) == (0,0,0):
                                        path.append((tempr,tempc-1))
                            if not self.has_rrook_moved and ( (self.color,tempr,tempc) == ('WHITE',7,5) or (self.color,tempr,tempc) == ('BLACK',0,5) ):
                                # check right block for empty
                                if self.board[tempr,tempc+1] == 0:
                                    # king is not getting attacked in way
                                    if (attk_zone[tempr,tempc+1],attk_zone[tempr,tempc],attk_zone[tempr,tempc-1]) == (0,0,0):
                                        path.append((tempr,tempc+1))
                    # if own piece then break
                    elif self.board[tempr,tempc] in self.own:
                        break
                    # else opponents piece, add current and break
                    else:
                        # if piece is king then he can't attck the opponent who is backed-up by opponent
#                        if piece_val!=5 or (piece_val == 5 and attk_zone[tempr,tempc] == 0):
#                            path.append((tempr,tempc))
                        # taking care if king is not in trouble
                        self.add_coord_to_path(path, r,c, tempr,tempc)
                        break
        # if piece is pawn
        else:
            r_ = ChessBoard.PROPG[self.color]
            if self.board[r+r_,c] == 0:
#                path.append((r+r_,c))
                self.add_coord_to_path(path, r,c, r+r_,c)
                # if Pawn at starting pos. and check if 2-step is available
                if ((self.color == 'WHITE' and r==6) or (self.color != 'WHITE' and r==1 )) and self.board[r+2*r_,c] == 0:
#                    path.append((r+2*r_,c))
                    self.add_coord_to_path(path, r,c, r+2*r_,c)
            if ChessBoard.check_coord(r+r_,c-1) and (self.board[r+r_,c-1] in self.enm or self.board[r+r_,c-1] == self.enm_bait):
#                path.append((r+r_,c-1))
                self.add_coord_to_path(path, r,c, r+r_,c-1)
            if ChessBoard.check_coord(r+r_,c+1) and (self.board[r+r_,c+1] in self.enm or self.board[r+r_,c+1] == self.enm_bait):
#                path.append((r+r_,c+1))
                self.add_coord_to_path(path, r,c, r+r_,c+1)
        
#        print(path)
        return path        
    
    # move the piece and return moved_pos
    def move_piece(self, piece, r1,c1, r2,c2):
        # finding positions of the piece
        piece_pos = np.argwhere(self.board.board == piece)
        if Player.logging:
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
            self.board.transact(avail_pieces[0][0],avail_pieces[0][1], r2,c2)
            return avail_pieces[0][0], avail_pieces[0][1]
        # if ambiguity between pieces (which piece to move)
        else:
            # removing pieces whose row doesn't match
            pieces_to_remove = set()
            if r1 != -1:
                for tup in avail_pieces:
                    if tup[0] != r1:
                        pieces_to_remove.add(tup)
            # removing pieces whose col. doesn't match
            if c1 != -1:
                for tup in avail_pieces:
                    if tup[1] != c1:
                        pieces_to_remove.add(tup)
            
            for t_piece in pieces_to_remove:
                avail_pieces.remove(t_piece)
            # if still ambiguity throw error else transact
            # specified current pos doesnt match
            if len(avail_pieces) == 0:
                raise Exception("invalid move (no one at specified current pos that can reach target pos)")
            elif len(avail_pieces) == 1:
                self.board.transact(avail_pieces[0][0],avail_pieces[0][1], r2,c2)
                return avail_pieces[0][0], avail_pieces[0][1]
            else:
                raise Exception(f"ambiguity between pieces at pos: {avail_pieces}")
    
    """TODO: test En passant move, test everything, test pawn_promotion and castling"""
    # make move and returns current and target coordinates
    def make_move(self,move):
        # parsing piece val, current row,col, target row,col
        piece, r1,c1, r2,c2 = ChessBoard.parse_move(move,self.color)
        # checking if pawn is taking bait and capturing pawn using en_passant
        bait_taken = False
        if ChessBoard.piece_val(piece) == 6 and self.board[r2,c2] == self.enm_bait:
            bait_taken = True
        # making transaction and getting prev r1,c1 if piece made successfully
        r1,c1 = self.move_piece(piece, r1,c1, r2,c2)
        
        # remove opponent en passant baits
        self.board.remove_bait(self)
        # remove captured pawn by en_passant if made
        if bait_taken:
            # clearing the captured Pawn by en_passant at prev. row and target column
            self.board.put_at(r1,c2,0)
        # if no exception occured, transaction done successfully then, care for castling, promotion, en passant
        # if Rook has moved
        if ChessBoard.piece_val(piece) == 1 and ((self.color=='WHITE' and r1==7) or (self.color!='WHITE' and r1==0)):
            if c1 == 0: # left-Rook has moved
                self.has_lrook_moved = True
            elif c1 == 7: # right-Rook has moved
                self.has_rrook_moved = True
        # for castling occured, if piece is king 
        if ChessBoard.piece_val(piece) == 5 and r1 == r2 and c1 == 4 and abs(c2-c1) == 2:
            # queen side
            if c2 == 2:
                self.board.transact(r1,0,r2,3) # transact left side Rook
            elif c2 == 6:
                self.board.transact(r1,7,r2,5) # transact right-side Rook
            self.can_castling = False
        # check for promotion, if Pawn at first or last row
        prom_piece = -1
        if ChessBoard.piece_val(piece) == 6 and (r2 == 0 or r2 == 7):
            match = re.compile(ChessBoard.move_pattern).match(move)
            p = match.group(5).upper()
            piece = np.argwhere(ChessBoard.PIECES == ('W'+p if self.color == 'WHITE' else 'B'+p))[0,0]
            self.board.put_at(r2,c2, piece)
            prom_piece = ChessBoard.piece_val(piece)
        # inserting en_passant bait (-1) for WHITE, (-2) for BLACK, if pawn jumps 2 cells
        if ChessBoard.piece_val(piece) == 6 and (r1 == 1 or r1 == 6) and c1==c2 and abs(r2-r1) == 2:
            r_ = ChessBoard.PROPG[self.color]
            self.board.add_bait(r1+r_,c1, self)
        
        # telling that this player has made his turn
        self.board.turn_made(self)
        
        if Player.logging:
            print(f"piece moved:{piece}, from:{r1},{c1}, to:{r2},{c2}, promoted to:{prom_piece}")
        
        return r1,c1, r2,c2, prom_piece
    
    def get_snapshot_vector(self):
        return self.board.get_snapshot_vector(self)
        
    def get_move_vector(self,r1,c1, r2,c2, prom):
        return self.board.get_move_vector(self,r1,c1, r2,c2, prom)
    
    
    