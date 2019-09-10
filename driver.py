# -*- coding: utf-8 -*-
"""
Created on Sat May 18 19:58:31 2019

@author: AMIT
"""
import numpy as np
from ChessBoard import ChessBoard
from Player import Player

p1 = Player()
p2 = Player('BLACK')

cb = ChessBoard()
cb.assign_players(p1,p2)

#for pos in ['b1','b8','c1','c8','d1','d8','f1','f8','g1','g8']:
#    cb.put(pos,0)
#cb.board

dataset = open('dataset/all_with_filtered_anotations_since1998_first10000.txt','r').read().split('\n')[5:100]

for data in dataset:
    p1 = Player()
    p2 = Player('BLACK')
    
    cb = ChessBoard()
    cb.assign_players(p1,p2)
    
    print(data)
    moves = data.split('###')[1].strip().split(' ')
    print(moves)
    i = 0
    ss = [cb.get_snapshot()]
    wp = []
    wm = []
    bp = []
    bm = []
    while i<len(moves):
        move = moves[i].split('.')[1]
        print("w:",move)
        wp.append(p1.get_snapshot_vector().reshape((12,8,8)))
        r1,c1, r2,c2 = p1.make_move(move)
        wm.append(p1.get_move_vector(r1,c1, r2,c2).reshape((2,8,8)))
        ss.append(cb.get_snapshot())
        i += 1
        if i>=len(moves):
            break
        move = moves[i].split('.')[1]
        print("b:",move)
        bp.append(p2.get_snapshot_vector().reshape((12,8,8)))
        r1,c1, r2,c2 = p2.make_move(move)
        bm.append(p2.get_move_vector(r1,c1, r2,c2).reshape((2,8,8)))
        ss.append(cb.get_snapshot())
        i += 1
    #    input("press enter to continue ...")
    print("match done !!")
    
print("done !!")


cb.put('e1',5)
cb.put('e8',11)

cb.put('e2',4)

cb.put('a2',6)
cb.put('b4',12)

p2.get_movable_pos()

p1.get_strength()

cb.get_weakness(p1.color)


cp1 = Player()
cp2 = Player('BLACK')

ccb = ChessBoard()
ccb.assign_players(cp1,cp2)

for cmove in moves:
    if cmove:
        cp1.make_move(cmove.strip().split()[0])
        input("press enter to cont:")
        cp2.make_move(cmove.strip().split()[1])
        input("press enter to cont:")
