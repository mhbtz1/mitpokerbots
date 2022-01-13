#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import copy 
import numpy as np 
import random

rank_map = {
    "2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6, "9": 7,
    "T": 8, "J": 9, "Q": 10, "K": 11, "A": 12,
}
suit_map = {
    "C": 0, "D": 1, "H": 2, "S": 3,
    "c": 0, "d": 1, "h": 2, "s": 3
}

flop_dict = {}
map_names = {}

def initialise_flop_dict():
    global flop_dict
    low_trips_flops = [("2s", "2c", "2d"), ("4s", "4d", "4h"), ("6c", "6d", "6h")]
    high_trips_flops = [("9s", "9c", "9d"), ("Js", "Jc", "Jd"), ("Ks", "Kc", "Kd")]
    flop_dict['low_trips_flops'] = ('001', low_trips_flops)
    flop_dict['high_trips_flops'] = ('002', high_trips_flops)
    low_connected_monotone = [("9s", "7s", "5s"), ("6s", "4s", "3s"), ("8s", "4s", "3s")]
    low_disconnected_monotone = [("9s", "6s", "2s"), ("Ts", "7s", "3s"), ("Ts", "6s", "3s")]
    high_monotone = [("Ks", "9s", "6s"), ("Qs", "8s", "3s"), ("As", "7s", "5s")]
    high_flopped_straight_monotone = [("As", "Ks", "Ts"), ("Ks", "Js", "9s"), ("Qs", "Js", "8s")]
    flop_dict['low_connected_monotone'] = ('003', low_connected_monotone)
    flop_dict['low_disconnected_monotone'] = ('004', low_disconnected_monotone)
    flop_dict['high_monotone'] = ('005', high_monotone)
    flop_dict['high_flopped_straight_monotone'] = ('006', high_flopped_straight_monotone)
    low_paired_low_side_rainbow = [("3s", "3d", "2h"), ("5s", "5d", "7h"), ("7s", "7d", "3h")]
    low_paired_low_side_fd = [("3s", "3d", "2s"), ("5s", "5d", "7s"), ("7s", "7d", "3s")]
    low_paired_ak_side_rainbow = [("6s", "6d", "Ah"), ("4s", "4d", "Kh"), ("3s", "3d", "Ac")]
    low_paired_ak_side_fd = [("6s", "6d", "As"), ("4s", "4d", "Ks"), ("3s", "3d", "As")]
    low_paired_high_side_rainbow = [("2s", "2d", "Th"), ("4s", "4d", "Qh"), ("6s", "6d", "Jh")]
    low_paired_high_side_fd = [("2s", "2d", "Ts"), ("4s", "4d", "Qs"), ("6s", "6d", "Js")]
    flop_dict['low_paired_low_side_rainbow'] = ('007', low_paired_low_side_rainbow)
    flop_dict['low_paired_low_side_fd'] = ('008', low_paired_low_side_fd)
    flop_dict['low_paired_ak_side_rainbow'] = ('009', low_paired_ak_side_rainbow)
    flop_dict['low_paired_ak_side_fd'] = ('010', low_paired_ak_side_fd)
    flop_dict['low_paired_high_side_rainbow'] = ('011', low_paired_low_side_rainbow)
    flop_dict['low_paired_high_side_fd'] = ('012', low_paired_high_side_fd)
    high_paired_low_side_rainbow = [("As", "Ad", "3h"), ("Ks", "Kd", "6h"), ("Qs", "Qd", "2h")]
    high_paired_low_side_fd = [("As", "Ad", "3s"), ("Ks", "Kd", "6s"), ("Qs", "Qd", "2s")]
    high_paired_high_side_rainbow = [("As", "Ad", "Kh"), ("Ks", "Kd", "Th"), ("Ts", "Td", "Ah")]
    high_paired_high_side_fd = [("As", "Ad", "Ks"), ("Ks", "Kd", "Ts"), ("Ts", "Td", "As")]
    flop_dict['high_paired_low_side_rainbow'] = ('013',high_paired_low_side_rainbow)
    flop_dict['high_paired_low_side_fd'] = ('014', high_paired_low_side_fd)
    flop_dict['high_paired_high_side_rainbow'] = ('015', high_paired_high_side_rainbow)
    flop_dict['high_paired_high_side_fd'] = ('016', high_paired_high_side_fd)
    triple_broadway_rainbow = [("As", "Qc", "Td"), ("Ks", "Jc", "Td"), ("As", "Qc", "Jd")]
    triple_broadway_fd = [("As", "Qc", "Ts"), ("Ks", "Jc", "Ts"), ("As", "Qc", "Js")]
    flop_dict['triple_broadway_rainbow'] = ('017', triple_broadway_rainbow)
    flop_dict['triple_broadway_fd'] = ('018', triple_broadway_fd)
    a_low_low_rainbow = [("As", "5c", "4d"), ("As", "4c", "3d"), ("As", "4c", "2d")]
    a_low_low_fd = [("As", "6c", "4s"), ("As", "4c", "3s"), ("As", "4c", "2s")]
    dry_a_high_rainbow = [("As", "9c", "4d"), ("As", "8c", "2d"), ("As", "7c", "3d")]
    dry_a_high_fd = [("As", "9c", "4s"), ("As", "8c", "2s"), ("As", "7c", "3s")]
    a_high_straightdraw_rainbow = [("As", "8c", "7d"), ("As", "9c", "7d"), ("As", "7s", "6d")]
    a_high_straightdraw_fd = [("As", "8c", "7s"), ("As", "9c", "7s"), ("As", "7s", "6s")]
    a_high_double_broadway_rainbow = [("As", "Kc", "2d"), ("As", "Qc", "6d"), ("As", "Tc", "5d")]
    a_high_double_broadway_fd = [("As", "Kc", "2s"), ("As", "Qc", "6s"), ("As", "Tc", "5s")]
    flop_dict['a_low_low_rainbow'] = ('019', a_low_low_rainbow)
    flop_dict['a_low_low_fd'] = ('020', a_low_low_fd)
    flop_dict['dry_a_high_rainbow'] = ('021', dry_a_high_rainbow)
    flop_dict['dry_a_high_fd'] = ('022', dry_a_high_fd)
    flop_dict['a_high_straightdraw_rainbow'] = ('023', a_high_straightdraw_rainbow)
    flop_dict['a_high_straightdraw_fd'] = ('024', a_high_straightdraw_fd)
    flop_dict['a_high_double_broadway_rainbow'] = ('025', a_high_double_broadway_rainbow)
    flop_dict['a_high_double_broadway_fd'] = ('026', a_high_double_broadway_fd)
    dry_k_high_rainbow = [("Ks", "7c", "2d"), ("Ks", "9c", "3d"), ("Ks", "8s", "4d")]
    dry_k_high_fd = [("Ks", "7c", "2s"), ("Ks", "9c", "3s"), ("Ks", "8s", "4s")]
    k_high_double_broadway_rainbow = [("Ks", "Qc", "8d"), ("Ks", "Tc", "5d"), ("Ks", "Jc", "5d")]
    k_high_double_broadway_fd = [("Ks", "Qc", "8s"), ("Ks", "Tc", "5s"), ("Ks", "Jc", "5s")]
    k_high_connected_rainbow = [("Ks", "9c", "7d"), ("Ks", "7c", "6d"), ("Ks", "5c", "4d")]
    k_high_connected_fd = [("Ks", "9c", "8s"), ("Ks", "8c", "7s"), ("Ks", "5c", "4s")]
    flop_dict['dry_k_high_rainbow'] = ('027', dry_k_high_fd)
    flop_dict['dry_k_high_fd'] = ('028', dry_k_high_fd)
    flop_dict['k_high_double_broadway_rainbow'] = ('029', k_high_double_broadway_rainbow)
    flop_dict['k_high_double_broadway_fd'] = ('030', k_high_double_broadway_fd)
    flop_dict['k_high_connected_rainbow'] = ('031', k_high_connected_rainbow)
    flop_dict['k_high_connected_fd'] = ('032', k_high_connected_fd)
    dry_q_high_rainbow = [("Qs", "7c", "3d"), ("Qs", "8c", "3d"), ("Qs", "5c", "2d")]
    dry_q_high_fd = [("Qs", "7c", "3s"), ("Qs", "8c", "3s"), ("Qs", "5c", "2s")]
    q_high_double_broadway_rainbow = [("Qs", "Jc", "3d"), ("Qs", "Jc", "9d"), ("Qs", "Tc", "7d")]
    q_high_double_broadway_fd = [("Qs", "Jc", "3s"), ("Qs", "Jc", "5s"), ("Qs", "Tc", "7s")]
    q_high_connected_rainbow = [("Qs", "9c", "5d"), ("Qs", "8c", "6d"), ("Qs", "7c", "6d")]
    q_high_connected_fd = [("Qs", "9c", "5s"), ("Qs", "8c", "6s"), ("Qs", "7c", "6s")]
    flop_dict['dry_q_high_rainbow'] = ('033', dry_q_high_rainbow)
    flop_dict['dry_q_high_fd'] = ('034', dry_q_high_fd)
    flop_dict['q_high_double_broadway_rainbow'] = ('035', q_high_double_broadway_rainbow)
    flop_dict['q_high_double_broadway_fd'] = ('036', q_high_double_broadway_fd)
    flop_dict['q_high_connected_rainbow'] = ('037', q_high_connected_rainbow)
    flop_dict['q_high_connected_fd'] = ('038', q_high_connected_fd)
    dry_j_high_rainbow = [("Js", "6c", "2d"), ("Js", "5c", "2d"), ("Js", "8c", "2d")]
    dry_j_high_fd = [("Js", "6c", "3s"), ("Js", "5c", "2s"), ("Js", "8c", "2s")]
    j_high_straight_rainbow = [("Js", "Tc", "9d"), ("Js", "9c", "7d"), ("Js", "9c", "8d")]
    j_high_straight_fd = [("Js", "Tc", "9s"), ("Js", "9c", "7s"), ("Js", "9c", "8s")]
    j_high_connected_rainbow = [("Js", "7c", "6d"), ("Js", "9c", "6d"), ("Js", "8c", "4d")]
    j_high_connected_fd = [("Js", "7c", "6s"), ("Js", "9c", "6s"), ("Js", "8c", "6d")]
    flop_dict['dry_j_high_rainbow'] = ('039', dry_j_high_rainbow)
    flop_dict['dry_j_high_fd'] = ('040', dry_j_high_fd)
    flop_dict['j_high_straight_rainbow'] = ('041', j_high_straight_rainbow)
    flop_dict['j_high_straight_fd'] = ('042', j_high_straight_fd)
    flop_dict['j_high_connected_rainbow'] = ('043', j_high_connected_rainbow)
    flop_dict['j_high_connected_fd'] = ('044', j_high_connected_fd)
    dry_t_high_rainbow = [("Ts", "8c", "3d"), ("Ts", "7c", "2d"), ("Ts", "6c", "4d")]
    dry_t_high_fd = [("Ts", "8c", "3s"), ("Ts", "7c", "2d"), ("Ts", "6c", "4s")]
    t_high_straight_rainbow = [("Ts", "7c", "6d"), ("Ts", "9c", "8d"), ("Ts", "8c", "7d")]
    t_high_straight_fd = [("Ts", "7c", "6s"), ("Ts", "9c", "8s"), ("Ts", "8c", "7s")]
    t_high_connected_rainbow = [("Ts", "8c", "5d"), ("Ts", "6c", "5d"), ("Ts", "9c", "5d")]
    t_high_connected_fd = [("Ts", "8c", "5s"), ("Ts", "6c", "5s"), ("Ts", "9c", "5s")]
    flop_dict['dry_t_high_rainbow'] = ('045', dry_t_high_rainbow)
    flop_dict['dry_t_high_fd'] = ('046', dry_t_high_fd)
    flop_dict['t_high_straight_rainbow'] = ('047', t_high_straight_rainbow)
    flop_dict['t_high_straight_fd'] = ('048', t_high_straight_fd)
    flop_dict['t_high_connected_rainbow'] = ('049', t_high_connected_rainbow)
    flop_dict['t_high_connected_fd'] = ('050', t_high_connected_fd)
    low_disconnected_rainbow = [("9s", "5c", "2d"), ("8s", "4c", "2d"), ("9s", "6c", "2d")]
    low_disconnected_fd = [("9s", "5c", "2s"), ("8s", "4c", "2s"), ("9s", "6c", "2s")]
    low_semiconnected_rainbow = [("9s", "8c", "4d"), ("9s", "6c", "4d"), ("8s", "5c", "3d")]
    low_semiconnected_fd = [("9s", "8c", "4s"), ("8s", "6c", "3s"), ("7s", "5c", "2s")]
    low_connected_rainbow = [("9s", "7c", "5d"), ("7s", "6c", "3d"), ("5s", "4c", "2d")]
    low_connected_fd = [("9s", "7c", "5d"), ("7s", "6c", "3d"), ("5s", "4c", "2d")]
    smooth_3straight_rainbow = [("9s", "8c", "7d"), ("7s", "6c", "5d"), ("5s", "4c", "3d")]
    smooth_3straight_fd = [("9s", "8c", "7d"), ("7s", "6c", "5d"), ("5s", "4c", "3d")]
    flop_dict['low_disconnected_rainbow'] = ('051', low_disconnected_rainbow)
    flop_dict['low_disconnected_fd'] = ('052', low_disconnected_fd)
    flop_dict['low_semiconnected_rainbow'] = ('053', low_semiconnected_rainbow)
    flop_dict['low_semiconnected_fd'] = ('054', low_semiconnected_fd)
    flop_dict['low_connected_rainbow'] = ('055', low_connected_rainbow)
    flop_dict['low_connected_fd'] = ('056', low_connected_fd)
    flop_dict['smooth_3straight_rainbow'] = ('057', smooth_3straight_rainbow)
    flop_dict['smooth_3straight_fd'] = ('058', smooth_3straight_fd)

    global map_names
    map_names['low_trips_flops'] = '001'
    map_names['high_trips_flops'] = '002'
    map_names['low_connected_monotone'] = '003'
    map_names['low_disconnected_monotone'] = '004'
    map_names['high_monotone'] = '005'
    map_names['high_flopped_straight_monotone'] = '006'
    map_names['low_paired_low_side_rainbow'] = ('007')
    map_names['low_paired_low_side_fd'] = ('008')
    map_names['low_paired_ak_side_rainbow'] = ('009')
    map_names['low_paired_ak_side_fd'] = ('010')
    map_names['low_paired_high_side_rainbow'] = ('011')
    map_names['low_paired_high_side_fd'] = ('012')
    map_names['high_paired_low_side_rainbow'] = ('013')
    map_names['high_paired_low_side_fd'] = ('014')
    map_names['high_paired_high_side_rainbow'] = ('015')
    map_names['high_paired_high_side_fd'] = ('016')
    map_names['triple_broadway_rainbow'] = ('017')
    map_names['triple_broadway_fd'] = ('018')
    map_names['a_low_low_rainbow'] = ('019')
    map_names['a_low_low_fd'] = ('020')
    map_names['dry_a_high_rainbow'] = ('021')
    map_names['dry_a_high_fd'] = ('022')
    map_names['a_high_straightdraw_rainbow'] = ('023')
    map_names['a_high_straightdraw_fd'] = ('024')
    map_names['a_high_double_broadway_rainbow'] = ('025')
    map_names['a_high_double_broadway_fd'] = ('026')
    map_names['dry_k_high_rainbow'] = ('027')
    map_names['dry_k_high_fd'] = ('028')
    map_names['k_high_double_broadway_rainbow'] = ('029')
    map_names['k_high_double_broadway_fd'] = ('030')
    map_names['k_high_connected_rainbow'] = ('031')
    map_names['k_high_connected_fd'] = ('032')
    map_names['dry_q_high_rainbow'] = ('033')
    map_names['dry_q_high_fd'] = ('034')
    map_names['q_high_double_broadway_rainbow'] = ('035')
    map_names['q_high_double_broadway_fd'] = ('036')
    map_names['q_high_connected_rainbow'] = ('037')
    map_names['q_high_connected_fd'] = ('038')
    map_names['dry_j_high_rainbow'] = ('039')
    map_names['dry_j_high_fd'] = ('040')
    map_names['j_high_straight_rainbow'] = ('041')
    map_names['j_high_straight_fd'] = ('042')
    map_names['j_high_connected_rainbow'] = ('043')
    map_names['j_high_connected_fd'] = ('044')
    map_names['dry_t_high_rainbow'] = ('045')
    map_names['dry_t_high_fd'] = ('046')
    map_names['t_high_straight_rainbow'] = ('047')
    map_names['t_high_straight_fd'] = ('048')
    map_names['t_high_connected_rainbow'] = ('049')
    map_names['t_high_connected_fd'] = ('050')
    map_names['low_disconnected_rainbow'] = ('051')
    map_names['low_disconnected_fd'] = ('052')
    map_names['low_semiconnected_rainbow'] = ('053')
    map_names['low_semiconnected_fd'] = ('054')
    map_names['low_connected_rainbow'] = ('055')
    map_names['low_connected_fd'] = ('056')
    map_names['smooth_3straight_rainbow'] = ('057')
    map_names['smooth_3straight_fd'] = ('058')





class FlopCard:
    def __init__(self, card, suit):
        self.card = card
        self.suit = suit

def boardtype(flop):
    #looks at the flop and evaluates the texture. Return type: (flop grouping name, examples)
    global flop_dict
    cards = [-1, -1, -1]
    cards[0] = FlopCard(flop[0][0],flop[0][1])
    cards[1] = FlopCard(flop[1][0], flop[1][1])
    cards[2] = FlopCard(flop[2][0], flop[2][1])

    high_card = flop[0][0]
    middle_card = flop[1][0]
    low_card = flop[2][0]
    
    #trips flops 
    low_trips_flops = [("2s", "2c", "2d"), ("4s", "4d", "4h"), ("6c", "6d", "6h")]
    high_trips_flops = [("9s", "9c", "9d"), ("Js", "Jc", "Jd"), ("Ks", "Kc", "Kd")]

    if high_card == middle_card == low_card: 
        if flop.high_card <= 7:
            return ("low_trips", low_trips_flops)
        else: 
            return ("high_trips", high_trips_flops) 
    
    #monotone flops 
    low_connected_monotone = [("9s", "7s", "5s"), ("6s", "4s", "3s"), ("8s", "4s", "3s")]
    low_disconnected_monotone = [("9s", "6s", "2s"), ("Ts", "7s", "3s"), ("Ts", "6s", "3s")]
    high_monotone = [("Ks", "9s", "6s"), ("Qs", "8s", "3s"), ("As", "7s", "5s")]
    high_flopped_straight_monotone = [("As", "Ks", "Ts"), ("Ks", "Js", "9s"), ("Qs", "Js", "8s")]


    if cards[0].suit == cards[1].suit == cards[2].suit:
        gaps = (high_card - middle_card - 1) + (middle_card - low_card - 1)
        if high_card <= 10: 
            if gaps <= 4: 
                return ("low_connected_monotone", low_connected_monotone)
            else: 
                return ("low_disconnected_monotone", low_disconnected_monotone) 
        else: 
            if gaps <= 2: 
                return ("high_flopped_straight_monotone", high_flopped_straight_monotone)
            else: 
                return ("high_monotone", high_monotone)
    
    #low paired flops 
    low_paired_low_side_rainbow = [("3s", "3d", "2h"), ("5s", "5d", "7h"), ("7s", "7d", "3h")]
    low_paired_low_side_fd = [("3s", "3d", "2s"), ("5s", "5d", "7s"), ("7s", "7d", "3s")]
    low_paired_ak_side_rainbow = [("6s", "6d", "Ah"), ("4s", "4d", "Kh"), ("3s", "3d", "Ac")]
    low_paired_ak_side_fd = [("6s", "6d", "As"), ("4s", "4d", "Ks"), ("3s", "3d", "As")]
    low_paired_high_side_rainbow = [("2s", "2d", "Th"), ("4s", "4d", "Qh"), ("6s", "6d", "Jh")]
    low_paired_high_side_fd = [("2s", "2d", "Ts"), ("4s", "4d", "Qs"), ("6s", "6d", "Js")]



    
    #high paired flops 
    high_paired_low_side_rainbow = [("As", "Ad", "3h"), ("Ks", "Kd", "6h"), ("Qs", "Qd", "2h")]
    high_paired_low_side_fd = [("As", "Ad", "3s"), ("Ks", "Kd", "6s"), ("Qs", "Qd", "2s")]
    high_paired_high_side_rainbow = [("As", "Ad", "Kh"), ("Ks", "Kd", "Th"), ("Ts", "Td", "Ah")]
    high_paired_high_side_fd = [("As", "Ad", "Ks"), ("Ks", "Kd", "Ts"), ("Ts", "Td", "As")]

    if high_card == middle_card or middle_card == low_card: 
            #define cards as the paired card and the "side" card 
        if high_card == middle_card: 
            paired_card = high_card 
            side_card = low_card
        elif middle_card == low_card: 
            paired_card = middle_card
            side_card = high_card 
    
            #low paired boards 
        if paired_card <= 8: 
            if side_card <= 8: 
                if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit: 
                    return ("low_paired_low_side_fd", low_paired_low_side_fd)
                return ("low_paired_low_side_rainbow", low_paired_low_side_rainbow)
            elif side_card == 13 or side_card == 12: 
                if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                    return ("low_paired_ak_side_fd", low_paired_ak_side_fd)
                return ("low_paired_low_side_rainbow", low_paired_low_side_rainbow)
            else: 
                if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                    return ("low_paired_high_side_fd", low_paired_high_side_fd)
                return ("low_paired_high_side_rainbow", low_paired_high_side_rainbow)
        elif paired_card > 8: 
            if side_card <= 8: 
                if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                    return ("high_paired_low_side_fd", high_paired_low_side_fd)
                return ("high_paired_low_side_rainbow", high_paired_low_side_rainbow)
            else: 
                if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                    return ("high_paired_high_side_fd", high_paired_high_side_fd)
                return ("high_paired_high_side_rainbow", high_paired_high_side_rainbow)
    
    #triple broadway boards 
    triple_broadway_rainbow = [("As", "Qc", "Td"), ("Ks", "Jc", "Td"), ("As", "Qc", "Jd")]
    triple_broadway_fd = [("As", "Qc", "Ts"), ("Ks", "Jc", "Ts"), ("As", "Qc", "Js")]

    if low_card >= 10: 
        if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
            return ("triple_broadway_fd", triple_broadway_fd)
        return ("triple_broadway_rainbow", triple_broadway_rainbow)
    
    #A-high boards 
    a_low_low_rainbow = [("As", "5c", "4d"), ("As", "4c", "3d"), ("As", "4c", "2d")]
    a_low_low_fd = [("As", "6c", "4s"), ("As", "4c", "3s"), ("As", "4c", "2s")]
    dry_a_high_rainbow = [("As", "9c", "4d"), ("As", "8c", "2d"), ("As", "7c", "3d")]
    dry_a_high_fd = [("As", "9c", "4s"), ("As", "8c", "2s"), ("As", "7c", "3s")]
    a_high_straightdraw_rainbow = [("As", "8c", "7d"), ("As", "9c", "7d"), ("As", "7s", "6d")]
    a_high_straightdraw_fd = [("As", "8c", "7s"), ("As", "9c", "7s"), ("As", "7s", "6s")]
    a_high_double_broadway_rainbow = [("As", "Kc", "2d"), ("As", "Qc", "6d"), ("As", "Tc", "5d")]
    a_high_double_broadway_fd = [("As", "Kc", "2s"), ("As", "Qc", "6s"), ("As", "Tc", "5s")]

    
    if high_card == 14:
        if middle_card <= 5: 
            if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                return ("a_low_low_fd", a_low_low_fd)
            return ("a_low_low_rainbow", a_low_low_rainbow)
        elif middle_card > 5 and middle_card < 10: 
            if (middle_card-low_card) <= 2: 
                if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                    return ("a_high_straightdraw_fd", a_high_straightdraw_fd)
                return ("a_high_straightdraw_rainbow", a_high_straightdraw_rainbow)
            else: 
                if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                    return ("dry_a_high_fd", dry_a_high_fd)
                return ("dry_a_high_rainbow", dry_a_high_rainbow)
        else: 
            if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                return ("a_high_double_broadway_fd", a_high_double_broadway_fd)
            return ("a_high_double_broadway_rainbow", a_high_double_broadway_rainbow)
        
    
    #K high boards 
    dry_k_high_rainbow = [("Ks", "7c", "2d"), ("Ks", "9c", "3d"), ("Ks", "8s", "4d")]
    dry_k_high_fd = [("Ks", "7c", "2s"), ("Ks", "9c", "3s"), ("Ks", "8s", "4s")]
    k_high_double_broadway_rainbow = [("Ks", "Qc", "8d"), ("Ks", "Tc", "5d"), ("Ks", "Jc", "5d")]
    k_high_double_broadway_fd = [("Ks", "Qc", "8s"), ("Ks", "Tc", "5s"), ("Ks", "Jc", "5s")]
    k_high_connected_rainbow = [("Ks", "9c", "7d"), ("Ks", "7c", "6d"), ("Ks", "5c", "4d")]
    k_high_connected_fd = [("Ks", "9c", "8s"), ("Ks", "8c", "7s"), ("Ks", "5c", "4s")]


    
    if high_card == 13: 
        if middle_card >= 10: 
            if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                return ("k_high_double_broadway_fd", k_high_double_broadway_fd)
            return ("k_high_double_broadway_rainbow", k_high_double_broadway_rainbow)
        else: 
            if (middle_card == 9 and low_card >= 7) or middle_card - low_card == 1:
                if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                    return ("k_high_connected_fd", k_high_connected_fd)
                return ("k_high_connected_rainbow", k_high_connected_rainbow)
            else: 
                if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                    return ("dry_k_high_fd", dry_k_high_fd)
                return ("dry_k_high_rainbow", dry_k_high_rainbow)
            
    
    #Q high boards 
    dry_q_high_rainbow = [("Qs", "7c", "3d"), ("Qs", "8c", "3d"), ("Qs", "5c", "2d")]
    dry_q_high_fd = [("Qs", "7c", "3s"), ("Qs", "8c", "3s"), ("Qs", "5c", "2s")]
    q_high_double_broadway_rainbow = [("Qs", "Jc", "3d"), ("Qs", "Jc", "9d"), ("Qs", "Tc", "7d")]
    q_high_double_broadway_fd = [("Qs", "Jc", "3s"), ("Qs", "Jc", "5s"), ("Qs", "Tc", "7s")]
    q_high_connected_rainbow = [("Qs", "9c", "5d"), ("Qs", "8c", "6d"), ("Qs", "7c", "6d")]
    q_high_connected_fd = [("Qs", "9c", "5s"), ("Qs", "8c", "6s"), ("Qs", "7c", "6s")]

    
    if high_card == 12: 
        if middle_card >= 10:
            if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                return ("q_high_double_broadway_fd", q_high_double_broadway_fd)
            return ("q_high_double_broadway_rainbow", q_high_double_broadway_rainbow)
        else: 
            gap_1 = high_card - middle_card - 1
            gap_2 = middle_card - low_card - 1
            if gap_2 == 0 and low_card >= 5: 
                if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                    return ("q_high_connected_fd", q_high_connected_fd)
                return ("q_high_connected_rainbow", q_high_connected_rainbow)
            elif gap_1 <= 2 and gap_2 <= 3 or gap_1 <= 3 and gap_2 <= 1: 
                if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                    return ("q_high_connected_fd", q_high_connected_fd)
                return ("q_high_connected_rainbow", q_high_connected_rainbow)
            else: 
                if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                    return ("dry_q_high_fd", dry_q_high_fd)
                return ("dry_q_high_rainbow", dry_q_high_rainbow)
    
    
    #J high boards
    dry_j_high_rainbow = [("Js", "6c", "2d"), ("Js", "5c", "2d"), ("Js", "8c", "2d")]
    dry_j_high_fd = [("Js", "6c", "3s"), ("Js", "5c", "2s"), ("Js", "8c", "2s")]
    j_high_straight_rainbow = [("Js", "Tc", "9d"), ("Js", "9c", "7d"), ("Js", "9c", "8d")]
    j_high_straight_fd = [("Js", "Tc", "9s"), ("Js", "9c", "7s"), ("Js", "9c", "8s")]
    j_high_connected_rainbow = [("Js", "7c", "6d"), ("Js", "9c", "6d"), ("Js", "8c", "4d")]
    j_high_connected_fd = [("Js", "7c", "6s"), ("Js", "9c", "6s"), ("Js", "8c", "6d")]

    
    if high_card == 11: 
        gap_1 = high_card - middle_card - 1 
        gap_2 = middle_card - low_card - 1 
        if gap_1 + gap_2 <= 3: 
            if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                return ("j_high_straight_fd", j_high_straight_fd)
            return ("j_high_straight_rainbow", j_high_straight_rainbow)
        elif gap_2 == 0 and low_card >= 5: 
            if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                return ("j_high_connected_fd", j_high_connected_fd) 
            return ("j_high_connected_rainbow", j_high_connected_rainbow)
        elif gap_1 <= 1 and gap_2 <= 2 or gap_1 <= 2 and gap_2 <= 1 : 
            if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                return ("j_high_connected_fd", j_high_connected_fd) 
            return ("j_high_connected_rainbow", j_high_connected_rainbow)
        else: 
             if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                 return ("dry_j_high_fd", dry_j_high_fd)
             return ("dry_j_high_rainbow", dry_j_high_rainbow)
    
    #T high boards 
    dry_t_high_rainbow = [("Ts", "8c", "3d"), ("Ts", "7c", "2d"), ("Ts", "6c", "4d")]
    dry_t_high_fd = [("Ts", "8c", "3s"), ("Ts", "7c", "2d"), ("Ts", "6c", "4s")]
    t_high_straight_rainbow = [("Ts", "7c", "6d"), ("Ts", "9c", "8d"), ("Ts", "8c", "7d")]
    t_high_straight_fd = [("Ts", "7c", "6s"), ("Ts", "9c", "8s"), ("Ts", "8c", "7s")]
    t_high_connected_rainbow = [("Ts", "8c", "5d"), ("Ts", "6c", "5d"), ("Ts", "9c", "5d")]
    t_high_connected_fd = [("Ts", "8c", "5s"), ("Ts", "6c", "5s"), ("Ts", "9c", "5s")]

    if high_card == 10: 
        gap_1 = high_card - middle_card - 1 
        gap_2 = middle_card - low_card - 1 
        if gap_1 + gap_2 <= 3: 
            if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                return ("t_high_straight_fd", t_high_straight_fd)
            return ("t_high_straight_rainbow", t_high_straight_rainbow)
        elif gap_2 == 0 and low_card >= 4: 
            if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                return ("t_high_connected_fd", t_high_connected_fd) 
            return ("t_high_connected_rainbow", t_high_connected_rainbow)
        elif gap_1 <= 1 and gap_2 <= 2: 
            if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                return ("t_high_connected_fd", t_high_connected_fd) 
            return ("t_high_connected_rainbow", t_high_connected_rainbow)
        else: 
            if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                 return ("dry_t_high_fd", dry_t_high_fd)
            return ("dry_t_high_rainbow", dry_t_high_rainbow)
        
        
    #9 high and lower 
    low_disconnected_rainbow = [("9s", "5c", "2d"), ("8s", "4c", "2d"), ("9s", "6c", "2d")]
    low_disconnected_fd = [("9s", "5c", "2s"), ("8s", "4c", "2s"), ("9s", "6c", "2s")]
    low_semiconnected_rainbow = [("9s", "8c", "4d"), ("9s", "6c", "4d"), ("8s", "5c", "3d")]
    low_semiconnected_fd = [("9s", "8c", "4s"), ("8s", "6c", "3s"), ("7s", "5c", "2s")]
    low_connected_rainbow = [("9s", "7c", "5d"), ("7s", "6c", "3d"), ("5s", "4c", "2d")]
    low_connected_fd = [("9s", "7c", "5d"), ("7s", "6c", "3d"), ("5s", "4c", "2d")] 
    smooth_3straight_rainbow = [("9s", "8c", "7d"), ("7s", "6c", "5d"), ("5s", "4c", "3d")]
    smooth_3straight_fd = [("9s", "8c", "7d"), ("7s", "6c", "5d"), ("5s", "4c", "3d")]

    
    if high_card <= 9: 
        gap_1 = high_card - middle_card - 1 
        gap_2 = middle_card - low_card - 1 
        if gap_1 == gap_2 == 0: 
            if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                return ("smooth_3straight_fd", smooth_3straight_fd) 
            return ("smooth_3straight_rainbow", smooth_3straight_rainbow)
        elif gap_1 + gap_2 <= 3: 
            if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                return ("low_connected_fd", low_connected_fd) 
            return ("low_connected_rainbow", low_connected_rainbow)
        elif gap_1 >= 1 and high_card >= 8 and low_card == 2: 
            if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                return ("low_disconnected_fd", low_disconnected_fd) 
            return ("low_disconnected_rainbow", low_disconnected_rainbow)
        else: 
            if cards[0].suit == cards[1].suit or cards[1].suit == cards[2].suit or cards[0].suit == cards[2].suit:
                return ("low_semiconnected_fd", low_semiconnected_fd) 
            return ("low_semiconnected_rainbow", low_semiconnected_rainbow)

            
        
    