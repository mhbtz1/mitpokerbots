import random
from collections import deque, defaultdict
import turtle
import numpy as np
import copy
import typing
import math


class HistoryState:
    '''
    Maintain a more complex history state for our CFR algorithm; allows for better utility functions & more reliable strategies

    For our toy game, auxiliary data will cointain : [#hearts in hand, #diamonds in hand, #spades in hand, #clubs in hand, length of attempted straight flush 1, length of attempted straight flush 2, .... ] of length 8
    and our main data will be our hand, and secondary data will maintain the actions taken for CFR
    '''

    burn_recall = 5

    def __init__(self, main_data, secondary_data='', auxiliary_data=np.zeros(8)):
        self.main_data = main_data
        self.secondary_data = secondary_data

class SFG_Trainer:
    def __init__(self, num_iter):
        self.num_iter = num_iter
        self.info_map = {}

    def get_information_set(self, card_plus_history):
        if (card_plus_history not in self.info_map):
            self.info_map[card_plus_history.secondary_data] = InformationSet(12)
        return self.info_map[card_plus_history.secondary_data]

    def sf_train(self):
        util = 0
        strat = []
        for _ in range(self.num_iter):
            t = ToyGame()
            historyState = HistoryState(t.hand1, '')
            reach_probabilities = np.ones(2)
            util += self.sf_cfrm(t, historyState, reach_probabilities, 1)

    def sf_cfrm(self, cards, history: HistoryState, reach_probabilities, cur_player):
        '''
        Apply CFR on our toy game
        '''
        print("CURRENT PLAYER: {}".format(cur_player))
        cards_copy = copy.deepcopy(cards)
        suit_count = []
        straight_count = []
        if (cards_copy.deck == None or len(cards_copy.deck)==0):
            cards_copy.recreate_deck()

        if(len(history.secondary_data) > 0):
            print(history.secondary_data)
            action = history.secondary_data[-1]
            print("PERFORMING ACTION... {}, {}".format(history.secondary_data[-1], type(history.secondary_data[-1])))
            int_action = ToyGame.action_to_index[history.secondary_data[len(history.secondary_data)-1]]
            print("ACTION: {}, {}".format(int_action,type(int_action)))
            cards_copy.perform_action(cur_player,int_action)

        cur_hand = cards_copy.hand1 if cur_player == 1 else cards_copy.hand2
        enemy_hand = cards_copy.hand2 if len(history.secondary_data)%2 == 0 else cards_copy.hand1

        info_set = self.get_information_set(history)
        cur_strategy = info_set.getStrategy(reach_probabilities[cur_player])
        cards_copy.create_auxiliary_information(cur_hand)

        if (cards_copy.is_terminal(straight_count)):
            print("GAME STATE SOLVED")
            return ToyGame.utility(cards, history)

        cfr_vals = np.zeros(info_set.num_actions)
        action_space = (cards_copy.get_all_actions())
        random.shuffle(action_space)

        print("ACTION SPACE: {}".format(action_space))

        for i, val in enumerate(action_space):
            print("PERFORMED ACTION: {}".format(val))

            action_prob = cur_strategy[val]
            nxt_reach = reach_probabilities.copy()
            nxt_reach[cur_player] *= action_prob



            new_history = copy.deepcopy(history)

            if(type(val)==int):
                val = ToyGame.index_to_action[val]

            if(val[-1]==','):
                val=val[0:len(val)-1]

            print("PERFORMED ACTION: {}".format(val))

            new_history.secondary_data += val
            new_history.main_data  = enemy_hand

            cfr_vals[i] = -self.sf_cfrm(cards_copy, new_history, nxt_reach,  (cur_player+1)%2)

        node_value = cfr_vals.dot(cur_strategy)
        for i, val in enumerate(ToyGame.get_all_actions()):
            info_set.regretSum[i] += ((reach_probabilities[(cur_player + 1) % 2] * (cfr_vals[i] - node_value)))

        return node_value

class ToyGame:
    '''
    A small toy game where both players start with N cards and draw until making a straight flush with their N cards. First to complete wins (i.e. the actual quality of the straight flush doesn't matter)
    '''
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['h', 'd', 's', 'c']
    map_hand = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13,
                'A': 14}
    index_to_action = {}
    action_to_index = {}
    N = 3

    def __init__(self):
        action_rep = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'E']
        for i in range(len(action_rep)):
            ToyGame.index_to_action[i] = action_rep[i]
            ToyGame.action_to_index[action_rep[i]] = i
        self.hand1 = []
        self.hand2 = []
        self.recreate_deck()
        self.create_hand(1)
        self.create_hand(2)

    def recreate_deck(self):
        self.deck = []
        for s in ToyGame.cards:
            for c in ToyGame.suits:
                if( (s+c) in self.hand1 or (s+c) in self.hand2):
                    continue
                self.deck.append(s + c)
        random.shuffle(self.deck)
        self.burn = []
    def create_hand(self, player_num):
        ptr = 0
        m_hand = []
        print("DECK: {}".format(self.deck))
        while (ptr < ToyGame.N):
            e = self.deck.pop()
            m_hand.append(e)
            ptr += 1
        if (player_num == 1):
            self.hand1 = m_hand
        else:
            self.hand2 = m_hand

    def is_terminal(self, condition):
        if (self.N in condition):
            return True
        return False

    def create_auxiliary_information(self, hand):
        '''
        Given a hand, calculate the relevant information needed for our utility function (the count of suits and the length of our straights for each suit in our hand) (NOT COMPLETED)
        '''
        count_suits = defaultdict(list)

        def make_comparator(lt):
            def compare(x, y):
                if( lt(x,y) ):
                    return 1
                else:
                    return -1
            return compare

        self.hand1.sort(key= lambda x : ToyGame.map_hand[x[0]])
        self.hand2.sort(key= lambda x : ToyGame.map_hand[x[0]])
        print("SORTED HAND: {}".format(self.hand1))
        print("SORTED HAND: {}".format(self.hand2))
        map_suit = {'h': 0, 'd': 1, 'c': 2, 's': 3}

        for s in hand:
            count_suits[map_suit[s[1]]].append(s[0])
        suit_count = [len(count_suits[0]), len(count_suits[1]), len(count_suits[2]), len(count_suits[3])]
        straight_count = [0, 0, 0, 0]  # maintain information about the straight we are holding for each suit
        straight_max_count = [0, 0, 0, 0]
        starting_cards = [-1, -1, -1, -1]  # maintain the current length of the straight we are holding


        '''
        Here, we calculate the length of the straight flush draws we are holding
        '''

        print(count_suits)

        for k, v in count_suits.items():
            '''
            The idea is, for each suit, we want to find the longest straight flush draw currently in our hand with that suit
            '''
            print("V: {}".format(v))
            for cards in v:
                print(cards,starting_cards[k])
                if (starting_cards[k] == -1):
                    starting_cards[k] = ToyGame.map_hand[cards]
                    straight_count[k] = 1
                else:
                    if (ToyGame.map_hand[cards] == starting_cards[k] + 1):
                        starting_cards[k] = ToyGame.map_hand[cards]
                        straight_count[k] += 1
                    else:
                        straight_max_count[k] = max(straight_max_count[k], straight_count[k])
                        straight_count[k] = 1
                        starting_cards[k] = ToyGame.map_hand[cards]
                straight_max_count[k] = max(straight_max_count[k], straight_count[k])

        '''
        Then, for each straight flush draw, calculate the number of outs our enemy is holding that we need OR have been burnt (i.e. a hand that cannot be completed should have 0/negative utility)
        '''
        enemy_count = []

        return (suit_count, straight_max_count)

    def utility(self, history: HistoryState):
        '''
        Custom utility function for our toy game using the two hands being played and the auxiliary information calculated (NOT COMPLETED)
        '''
        hand = history.main_data
        action_history = history.secondary_data  # string of actions
        player_num = 1 if len(action_history) % 2 == 0 else 2

        if(len(action_history) > 0):
            self.perform_action(player_num, action_history[len(action_history) - 1])

        our_hand = history.main_data
        (suit_count, straight_count) = self.create_auxiliary_information(our_hand)
        (suit_count_enemy, straight_count_enemy) = self.create_auxiliary_information(self.hand2)

        history.main_data = self.hand1 if player_num == 0 else self.hand2

        enemy_hand = self.hand2 if player_num == 0 else self.hand1


        p1_utility = (np.var(suit_count) * np.max(suit_count)) + (-np.var(straight_count) * np.max(straight_count))
        p2_utility = (np.var(suit_count_enemy) * np.max(suit_count)) + (-np.var(straight_count_enemy)*np.max(straight_count))
        p1_utility -= p2_utility

        return p1_utility #in this case, p1_utility refers to the current player, not necessarily p1




    def get_all_actions(self):
        '''
        Gets all the possible actions that can currently be taken at some time; in this case it is easy since both players will always have the same action space, but this is not the case with NLHE
        Note: convention is index i from 0...N means taking card i, burning it, and taking card from deck; index i from N+1...2*N means taking card (i-1)%N and swapping it with the burnt card
        '''
        if (len(self.deck) == 0):
            for s in ToyGame.cards:
                for c in ToyGame.suits:
                    self.deck.append(s + c)
            self.deck = random.shuffle(self.deck)
            self.burn = []
            return [i for i in range((ToyGame.N),
                                     2 * ToyGame.N)]  # if deck is empty, all the action that can be done is draw from the top burn card
        elif (len(self.burn) == 0):
            return [i for i in range(0, ToyGame.N)]
        else:
            return [i for i in
                    range(0, 2 * ToyGame.N)]  # otherwise, we can choose to get the top card from the deck or top burn card

    def perform_action(self, player_num, action_type):
        if (player_num == 0):
            if (0 <= action_type < ToyGame.N):
                cur_hand = self.hand1[action_type]
                self.hand1[action_type] = self.deck[0]
                self.deck = self.deck[1:]
                self.burn.append(cur_hand)
                return self.hand1
            elif(len(self.burn)>0):
                self.hand1[action_type % len(self.hand1)] = self.burn[0]
                self.burn = self.burn[0:len(self.burn) - 1]
                return self.hand1
        else:
            if (0 <= action_type < ToyGame.N):
                cur_hand = self.hand2[action_type]
                self.hand2[action_type] = self.deck[0]
                self.deck = self.deck[1:]
                self.burn.append(cur_hand)
                return self.hand2
            elif(len(self.burn)>0):
                self.hand2[action_type % len(self.hand1)] = self.burn[len(self.burn) - 1]
                self.burn = self.burn[0:len(self.burn) - 1]
                return self.hand2




class RPS:
    '''
    Test class for initial regret matching algorithm using RPS
    '''

    def get_all_actions():
        return [0, 1, 2]

    def utility(m1, m2):
        '''
        ROCK = 0, PAPER = 1, SCISSORS = 2
        '''
        if (m1 == 0 and m2 == 2):
            return 1
        elif (m1 == 1 and m2 == 0):
            return 1
        elif (m1 == 2 and m2 == 1):
            return 1
        elif (m1 == m2):
            return 0
        else:
            return -1

    def trainer(state_obj, num_iter):
        state_opp = State(3)
        for i in range(num_iter):
            print(state_obj.strategy)
            strat = state_obj.getStrategy()
            ac = state_obj.getAction()

            strat2 = state_opp.getStrategy()
            ac2 = state_opp.getAction()

            state_obj.acc_regret(state_opp, strat)
            state_opp.acc_regret(state_obj, strat2)
        return (state_obj.getAverageStrategy(), state_opp.getAverageStrategy())

    def train_cfrm(state_obj, num_iter):
        '''
        Counterfactual regret minimization on Kuhn Poker
        '''
        util = 0
        for i in range(num_iter):
            my_cards = random.shuffle(KuhnPoker.cards, 2)
            print("CARDS: {}".format(my_cards))
            util += KuhnPoker.kuhn_cfrm(my_cards, "", 1, 0)


class KuhnPoker:
    '''
    Application of CFR on Kuhn Poker game; properly approaches Nash Equilibrium for ['K', 'Q', 'J']
    '''

    PASS = 0
    BET = 1
    NUM_ACTIONS = 2
    map_action = {}
    cards = ['K', 'Q', 'J']

    def __init__(self):
        self.info_map = {}
        KuhnPoker.map_action[0] = 'b'
        KuhnPoker.map_action[1] = 'c'

    @staticmethod
    def utility(cards, history):
        '''
        Utility function for Kuhn Poker which uses the action history and the hands being played to assign utilities
        Uses the length of history to find the current player also
        '''
        if (history in ['bc', 'cbc']):
            return 1
        else:
            payoff = 2 if 'b' in history else 1
            f = len(history) % 2
            cur_card = cards[f]
            opp_card = cards[(f + 1) % 2]
            if (cur_card == 'K' or opp_card == 'J'):
                return payoff
            return -payoff

    def is_terminal(history):
        return history in ['bc', 'bb', 'cc', 'cbc', 'cbb']

    def get_information_set(self, card_plus_history):
        if (card_plus_history not in self.info_map):
            self.info_map[card_plus_history] = InformationSet(2)
        return self.info_map[card_plus_history]

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

    def sf_cfrm(self, cards: ToyGame, history: HistoryState, reach_probabilities, cur_player):
        '''
        Apply CFR on our toy game (NOT COMPLETED)
        '''
        if (ToyGame.is_terminal(history)):
            return ToyGame.utility(cards, history)

        cards_copy = cards.copy()
        cards_copy.perform_action(history[len(history) - 1], cur_player)
        cur_hand = cards_copy.hand1 if cur_player == 1 else cards_copy.hand2
        info_set = self.get_information_set(cur_hand)
        cur_strategy = info_set.getStrategy(reach_probabilities[cur_player])

        cfr_vals = np.zeros(info_set.num_actions)

        for i, val in enumerate(cards_copy.get_all_actions()):
            action_prob = cur_strategy[i]
            nxt_reach = reach_probabilities.copy()
            nxt_reach[cur_player] *= action_prob

            new_history = history.copy()
            new_history.secondary_data += ToyGame.index_to_action[val]
            cfr_vals[i] = -self.vanilla_cfrm(cards_copy, new_history, nxt_reach, (cur_player + 1) % 2)

        node_value = cfr_vals.dot(cur_strategy)
        for i, val in enumerate(ToyGame.get_all_actions()):
            info_set.regretSum[i] += ((reach_probabilities[(cur_player + 1) % 2] * (cfr_vals[i] - node_value)))

        return node_value

    def train(self, num_iter):
        util = 0
        strat = []
        for _ in range(num_iter):
            cards = random.sample(KuhnPoker.cards, 2)
            reach_probabilities = np.ones(2)
            util += self.kuhn_cfrm(cards, '', reach_probabilities, 0)
        print("Expected average utility: {}".format(float(util) / float(num_iter)))
        return util

    def get_all_actions():
        return [0, 1]


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

    def acc_regret(self, opp, strategy):
        '''
        Used for regret matching with RPS (not used anymore)
        '''
        actions = KuhnPoker.get_all_actions()
        my_action = self.getAction()
        other_action = opp.getAction()

        '''
        Compute action utilities
        '''
        self.kuhn_action_utilities(opp, my_action, other_action)

        for i in range(self.num_actions):
            self.regret[i] = (self.actionUtility[i] - self.actionUtility[my_action])
            self.regretSum[i] += self.regret[i]

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


'''
s = InformationSet(3)
(a,b) = RPS.trainer(s,1000)
print(a,b)
'''

k = KuhnPoker()
total_utility = k.train(3000)
for (history, info_set) in k.info_map.items():
    print(history, info_set.getAverageStrategy())

t = ToyGame()
t.create_hand(1)
t.create_hand(2)

print("HAND 1: {}".format(t.hand1))
print("HAND 2: {}".format(t.hand2))

'''
print("DECK: {}".format(t.deck))
print("ACTION SPACE: {}".format(t.get_all_actions()))
t.perform_action(1,4)
print("NEW HAND: {}".format(t.hand1))
print("BURN: {}".format(t.burn))
t.perform_action(1,6)
print("NEW HAND: {}".format(t.hand1))
print("BURN: {}".format(t.burn))
'''

print("AUXILIARY INFORMATION FOR HAND 1: {}".format(t.create_auxiliary_information(t.hand1)))
print("AUXILIARY INFORMATION FOR HAND 2: {}".format(t.create_auxiliary_information(t.hand2)))
history1 = HistoryState(t.hand1, '')
print("HAND UTILITY: {}".format(t.utility(history1)))


test_cfr = ToyGame()
run_cfr = SFG_Trainer(1000)
run_cfr.sf_train()