import math
import eval7
from python_skeleton.skeleton.states import CallAction, FoldAction, RaiseAction, CheckAction
import SwapPoker
from python_skeleton.skeleton.CFRM import KuhnPoker
import numpy as np
import random
import InformationSet

class MCCFR():
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['h', 'd', 's', 'c']

    def get_information_set(self, card_plus_history):
        if (card_plus_history not in self.info_map):
            self.info_map[card_plus_history] = InformationSet(2)
        return self.info_map[card_plus_history]


    def __init__(self, game_state, round_state):
        self.info_map = {}
        self.game_state = game_state
        self.round_state = round_state
        self.board = []
        self.deck = []
        for s in MCCFR.cards:
            for c in MCCFR.suits:
                self.deck.append(s + c)
        random.shuffle(self.deck)

        self.p1_hole_cards = [self.deck[0], self.deck[1]]
        self.p2_hole_cards = [self.deck[2], self.deck[3]]
        self.deck = self.deck[4:]

    def mccfr(self, game_state : SwapPoker, history_state, reach_probabilities, cur_player ):
        '''
        make self play procedure without using actual GameState and RoundState namedtuples; will use while applying during real play
        '''
        if(game_state.is_terminal(history_state)):
            return game_state.utility()

        cur_hand = self.p1_hole_cards if cur_player == 0 else self.p2_hole_cards
        other_hand = self.p2_hole_cards if cur_player == 0 else self.p1_hole_cards
        get_all_actions = game_state.get_all_actions()
        for i in range(len(get_all_actions)):
            pass





def kuhn_cfrm(self, cards, history, reach_probabilities, cur_player):
    if (KuhnPoker.is_terminal(history)):
        return KuhnPoker.utility(cards, history)

    cur_card = cards[cur_player]
    info_set = self.get_information_set(cur_card + history)
    cur_strategy = info_set.getStrategy(reach_probabilities[cur_player])

    cfr_vals = np.zeros(info_set.num_actions)

    for i, val in enumerate(KuhnPoker.get_all_actions()):
        action_prob = cur_strategy[i]
        nxt_reach = reach_probabilities.copy()
        nxt_reach[cur_player] *= action_prob
        cfr_vals[i] = -self.kuhn_cfrm(cards, history + KuhnPoker.map_action[val], nxt_reach, (cur_player + 1) % 2)

    node_value = cfr_vals.dot(cur_strategy)
    for i, val in enumerate(KuhnPoker.get_all_actions()):
        info_set.regretSum[i] += ((reach_probabilities[(cur_player + 1) % 2] * (cfr_vals[i] - node_value)))

    return node_value


