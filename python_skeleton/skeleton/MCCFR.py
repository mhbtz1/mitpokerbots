import copy

import SwapPoker
import numpy as np
import random
import InformationSet
import random

import numpy as np
from SwapPoker import SwapPoker

class InformationSet:
    '''
    Maintain information for indistinguishable states in our game tree using this InformationSet class; will be implemented to map a string of actions to an InformationSet
    '''

    def __init__(self, num_actions):
        self.infoSet = ""
        self.num_actions = num_actions
        self.strategy = np.zeros(num_actions)
        self.strategySum = np.zeros(num_actions)
        self.regretSum = np.zeros(num_actions)
        self.regret = np.zeros(num_actions)
        self.actionUtility = np.zeros(num_actions)

    def getAction(self):
        '''
        Actions 0...n indicates discarding card i (0 <= i <= n) and drawing from deck
        Actions n+1...2*n indicates discarding i (n+1 <= i <= 2*n) and drawing from top burn card
        '''
        r = random.uniform(0, 1)
        sm = 0
        cumul_prob = 0
        while (sm < self.num_actions - 1):
            cumul_prob += self.strategy[sm]
            if (r < cumul_prob):
                break
            sm += 1
        return sm

    def normalize(self, strat):
        if (sum(strat) > 0):
            strat /= sum(strat);
            # print("NORMALISED: {}".format(strat))
        else:
            strat = np.array([float(1) / float(self.num_actions)] * self.num_actions)
            # print("NORMALISED: {}".format(strat))
        return strat

    def getStrategy(self, reach_probability):
        strat = np.maximum(0, self.regretSum)
        strat = self.normalize(strat)
        self.strategySum += reach_probability * strat
        self.strategy = strat
        # print("STRATEGY: {}".format(self.strategy))
        return self.strategy

    def getAverageStrategy(self):
        '''
        Gets average mixed strategy over self.num_actions iterations
        '''
        return self.normalize(self.strategySum.copy())

    def __str__(self):
        return self.infoSet + ": " + str(self.getAverageStrategy())


class History:
    pass

def gen_deck(cards, suits):
    deck = []
    for s in CFR_Game_State.cards:
        for c in CFR_Game_State.suits:
            deck.append(s + c)
    return deck

class CFR_Game_State:
    MAX_ACTIONS_PER_STREET = 2
    BETS_ARE_DONE = False
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['h', 'd', 's', 'c']

    def __init__(self, board_cards, p1_hole, p1_stack, p2_hole, p2_stack, IP_PLAYER, pot_size):
        '''
        Preflop is hardcoded, so we will assume that board_cards start out as the flop cards, and the pot size is just preflop bets
        '''
        self.board_cards = board_cards
        self.p1_hole = p1_hole
        self.p2_hole = p2_hole
        self.p1_stack = p1_stack
        self.p2_hole = p2_hole
        self.p2_stack = p2_stack
        self.pot_size = pot_size
        self.IP_PLAYER = IP_PLAYER
        self.ACTIONS_PER_STREET = 0

        self.deck = []
        for s in CFR_Game_State.cards:
            for c in CFR_Game_State.suits:
                self.deck.append(s + c)
        random.shuffle(self.deck)
        self.deck.remove(p1_hole[0])
        self.deck.remove(p1_hole[1])
        self.deck.remove(p2_hole[0])
        self.deck.remove(p2_hole[1])
        self.deck.remove(board_cards[0])
        self.deck.remove(board_cards[1])
        self.deck.remove(board_cards[2])

    def sample_chance(self, history, player):
        possible_actions = self.get_all_actions(history, player)
        ran_num = int(random.uniform(0,len(possible_actions)))
        return possible_actions[ran_num]
    def is_chance(self, history, player_num):
        if(len(self.get_all_actions(history, player_num)) >= 2):
            return True

    def is_terminal(self,history):
        if(len(history)==0):
            return False
        if(history[-3:] == 'FLD'):
            return True
        elif(len(self.board_cards)==5 and len(history)>=27): #we only allow 2 actions per street, and we fully solve preflop using precomputed range charts
            return True
        else:
            return False

    def action_translation(self, sizing):
        '''
        Translates the action of a bet to a bet size we can understand
        '''
        if (sizing >= 200):
            return 200
        elif (80 <= sizing <= 200):
            if (abs(sizing - 80) <= abs(sizing - 200)):
                return 80
            else:
                return 200
        elif (75 <= sizing <= 80):
            if (abs(sizing - 80) <= abs(sizing - 75)):
                return 80
            else:
                return 75
        elif (66 <= sizing <= 75):
            if (abs(sizing - 66) <= abs(sizing - 75)):
                return 66
            else:
                return 75
        else:
            return 66

    def apply_action(self, history, action_string, player_num):
       print("HISTORY: {}, ACTION: {}".format(history,action_string))
       if(action_string[0]=='R'):#raise
           relsize = 2 if action_string[1:]=='CC' else float(int(action_string[1:]))/100
           raiseamt = relsize*self.pot_size
           self.pot_size += raiseamt
           if(player_num==0):
               self.p1_stack -= raiseamt
           else:
               self.p2_stack -= raiseamt
           self.ACTIONS_PER_STREET += 1
       elif(action_string=='CHK'):#check
           self.ACTIONS_PER_STREET += 1
       elif(action_string=='CAL'): #call a raise
           last_action = '' if len(history) < 3 else history[-3:]
           if(last_action != ''):
               conv_bet = 2 if last_action[1:] == 'CC' else float(int(last_action[1:])) / 100
               original_bet_size = (conv_bet)/float(1+conv_bet) * self.pot_size
               if(player_num == 0):
                   self.p1_stack -= original_bet_size
                   self.pot_size += original_bet_size
               else:
                   self.p2_stack -= original_bet_size
                   self.pot_size += original_bet_size


       if(self.ACTIONS_PER_STREET == self.MAX_ACTIONS_PER_STREET):
           self.ACTIONS_PER_STREET=0
           print("ADVANCED BOARD")
           if(len(self.board_cards)<5):
              self.board_cards += [self.deck[0]]
              del self.deck[0]


    def get_all_actions(self, history, player_num):
        '''
        Default ordering is: R66, R75, R80, R200, C66, C75, C80, C200, CHK, FLD
        '''
        default_actions = ['R66', 'R75', 'R80', 'RCC', 'CAL', 'CHK', 'FLD']
        last_action = '' if len(history) < 3 else history[-3:]
        '''
        remove actions based upon the bet sizes our stack allows us to do
        '''
        for i in range(len(default_actions)-1,-1,-1):
            action = default_actions[i]
            if(action == 'CHK' or action == 'CAL' or action == 'FLD'):
                continue
            sizing = 2 if action[1:]=='CC' else float(int(action[1:]))/100
            truesize = sizing * self.pot_size
            if(player_num == 0):
                if(truesize > self.p2_stack):
                    del default_actions[i]
            else:
                if(truesize > self.p1_stack):
                    del default_actions[i]

        '''
        remove actions based on the last action
        '''
        if(last_action != ''):
            if(last_action[0]=='R'):
                #if the last action is a raise, we can either reraise, call, or fold
                del default_actions[default_actions.index('CHK')]
                for i in range(len(default_actions)-1,-1,-1):
                    if(default_actions[i] == 'FLD'):
                        continue
                    if(default_actions[i] == 'CHK'):
                        del default_actions[i]
                    if(default_actions[i][0] == 'R'):
                        amt = 2 if default_actions[i][1:]=='CC' else float(int(default_actions[i][1:]))/100
                        betsize = amt * self.pot_size
                        lamt = 2 if last_action[1:]=='CC' else float(int(last_action[1:]))/100
                        lsize = (float(lamt)/(1 + lamt)) * self.pot_size
                        print("LAST BET SIZE: {}".format(lsize), 'CURRENT BET SIZE: {}'.format(betsize))
                        if(player_num==0):
                            if(betsize > self.p2_stack or lsize * 2 > betsize):
                                del default_actions[i]
                        elif(player_num==1):
                            if(betsize > self.p1_stack or lsize * 2 > betsize):
                                del default_actions[i]
                    if(default_actions[i]== 'CAL'):
                        conv_bet = 2 if last_action[1:]=='CC' else float(int(last_action[1:]))/100
                        original_bet_size = (conv_bet)/float(1+conv_bet) * self.pot_size
                        if(player_num==0):
                            if(original_bet_size > self.p2_stack):
                                del default_actions[i]
                        else:
                            if(original_bet_size > self.p1_stack):
                                del default_actions[i]
            elif(last_action=='CHK'):
                if('FLD' in default_actions):
                    del default_actions[default_actions.index('FLD')]
                if('CAL' in default_actions):
                    del default_actions[default_actions.index('CAL')]
                #if the last action is a check, then we can bet or check back
            elif(last_action=='CAL'):
                if('FLD' in default_actions):
                    del default_actions[default_actions.index('FLD')]
                if('CAL' in default_actions):
                    del default_actions[default_actions.index('CAL')]
                self.ACTIONS_PER_STREET = 0
                if(len(self.board_cards)<5):
                    self.board_cards += [self.deck[0]]
                    del self.deck[0]
                #if the last action is a call, then there is nothing else to do
        else:
            for i in range(len(default_actions)-1,-1,-1):
                if(default_actions[i][0]=='C' and default_actions[i] != 'CHK'):
                    del default_actions[i]
        print("ANSWER: {}".format(default_actions))
        return default_actions







class MCCFR():
    def __init__(self):
        self.info_map = {}

    def get_information_set(self, card_plus_history):
        if (card_plus_history not in self.info_map):
                self.info_map[card_plus_history] = InformationSet(11)
        return self.info_map[card_plus_history]



    def mc_cfrm(self, game_state : CFR_Game_State, history_state, reach_probabilities, cur_player):

        cur_game_state = copy.deepcopy(game_state)
        if(len(history_state)==3):
            cur_game_state.apply_action('', history_state, cur_player) #if history state is 0, technically the last action is the one we need to apply, so there is no history
        elif(len(history_state)>=3):
            cur_game_state.apply_action(history_state[0:-3],history_state[-3:],cur_player)
        all_actions = cur_game_state.get_all_actions(history_state, (cur_player+1)%2)

        print("HISTORY: {}".format(history_state))
        print("BOARD STATE: {}".format(cur_game_state.board_cards))
        print("STACKS: {}, {}".format(cur_game_state.p1_stack, game_state.p2_stack))
        print("POT: {}".format(cur_game_state.pot_size))
        print("NUM OF ACTIONS ON CURRENT STREET: {}".format(cur_game_state.ACTIONS_PER_STREET))
        if (cur_game_state.is_terminal(history_state)):
            print("TERMINAL STATE REACHED")
            utility = SwapPoker.utility(cur_game_state,history_state,cur_player)
            print("UTILITY: {}".format(utility))
            return utility

        #add code for if we have a chance node here, and apply chance sampling


        cur_hand = cur_game_state.p1_hole if cur_player == 0 else cur_game_state.p2_hole
        concat = ''.join(cur_hand)
        info_set = self.get_information_set(concat + history_state)
        cur_strategy = info_set.getStrategy(reach_probabilities[cur_player])
        cfr_vals = np.zeros(info_set.num_actions)
        print("ALL ACTIONS: {}".format(all_actions))

        for i, val in enumerate(all_actions):
            action_prob = cur_strategy[i]
            nxt_reach = reach_probabilities.copy()
            nxt_reach[cur_player] *= action_prob
            history_state += val
            cfr_vals[i] = -self.mc_cfrm(cur_game_state, history_state, nxt_reach, (cur_player + 1) % 2)

        node_value = cfr_vals.dot(cur_strategy)
        for i, val in enumerate(all_actions):
            info_set.regretSum[i] += ((reach_probabilities[(cur_player + 1) % 2] * (cfr_vals[i] - node_value)))

        return node_value

    def vanilla_cfrm(self, game_state, history_state, reach_probabilities, cur_player):
        pass




cfr_run = MCCFR()
util = 0
for i in range(200):
    print('----------------------------------------------------------------------------------------------------------')
    reach_prob = np.ones(2)
    ip_player = 1 if random.uniform(0,1) <= 0.5 else 0

    cfr_test = CFR_Game_State(['2d', '3s', '4c'], ['Ad', 'Ah'], 2000, ['Qc', 'Qs'], 2000, 0, 20)
    util += cfr_run.mc_cfrm(cfr_test, '', reach_prob, (ip_player+1)%2)
    print("ITERATION COMPLETE!")
    CFR_Game_State.BETS_ARE_DONE=False
    print('-----------------------------------------------------------------------------------------------------------')
print("UTILITY: {}".format(util))



info_sets = cfr_run.info_map
for (pos, strat) in info_sets.items():
    rep_strat = [float(s) for s in strat.strategy]
    print(pos,rep_strat)



'''
cfr_test_run = CFR_Game_State(['Ac', '5s', 'Qd'], ['Qs', '9s'], 2000, ['Kc', '9c'], 2000, 0, 25)
print(cfr_test_run.get_all_actions('',0))

print("POT SIZE: {}".format(cfr_test_run.pot_size))
cfr_test_run.apply_action('', 'RCC', 1)
print("POT SIZE: {}".format(cfr_test_run.pot_size))
print(cfr_test_run.board_cards)
print(cfr_test_run.p1_stack, cfr_test_run.p2_stack)
print(cfr_test_run.get_all_actions('RCC', 0))
cfr_test_run.apply_action('RCC', 'RCC', 0)
print("POT SIZE: {}".format(cfr_test_run.pot_size))
print(cfr_test_run.board_cards)
print(cfr_test_run.p1_stack, cfr_test_run.p2_stack)
print(cfr_test_run.get_all_actions('RCCRCC',1))
cfr_test_run.apply_action('RCCRCCC', 'RCC', 1)
print("POT SIZE: {}".format(cfr_test_run.pot_size))
print(cfr_test_run.board_cards)
print(cfr_test_run.p1_stack, cfr_test_run.p2_stack)
print(cfr_test_run.get_all_actions('RCCRCC',0))
cfr_test_run.apply_action('RCCCRCCRCC','RCC',0)
print("POT SIZE: {}".format(cfr_test_run.pot_size))
print(cfr_test_run.board_cards)
print(cfr_test_run.p1_stack, cfr_test_run.p2_stack)
print(cfr_test_run.get_all_actions('RCCRCCRCCRCC',1))
cfr_test_run.apply_action('RCCCRCCRCCRCC','CAL',1)
print("POT SIZE: {}".format(cfr_test_run.pot_size))
print(cfr_test_run.board_cards)
print(cfr_test_run.p1_stack, cfr_test_run.p2_stack)
print(cfr_test_run.get_all_actions('RCCRCCRCCRCCCAL',1))
'''





