from actions import FoldAction, RaiseAction, CheckAction
from states import RoundState
from python_skeleton import Evaluator
import math



class SwapPoker:
    def __init__(self, game_state, round_state, board_cards):
        self.game_state = game_state #store pot size, hole c
        self.round_state = round_state
        self.board_cards = board_cards

    def update_board(self, new_board):
        self.board_cards = new_board

    def poker(self, hands):
        scores = [(i, self.score(hand.split())) for i, hand in enumerate(hands)]
        winner = sorted(scores, key=lambda x: x[1])[-1][0]
        return hands[winner]

    def score(self, hand):
        ranks = '23456789TJQKA'
        rcounts = {ranks.find(r): ''.join(hand).count(r) for r, _ in hand}.items()
        score, ranks = zip(*sorted((cnt, rank) for rank, cnt in rcounts)[::-1])
        if len(score) == 5:
            if ranks[0:2] == (12, 3):  # adjust if 5 high straight
                ranks = (3, 2, 1, 0, -1)
            straight = ranks[0] - ranks[4] == 4
            flush = len({suit for _, suit in hand}) == 1
            '''no pair, straight, flush, or straight flush'''
            score = ([1, (3, 1, 1, 1)], [(3, 1, 1, 2), (5,)])[flush][straight]
        return score, ranks


    def utility(cfr_game_state, history, cur_player):
       if(len(history)>= 3 and history[-3:] == 'FLD'):
           return cfr_game_state.pot_size
       else:
           '''
           implement showdown and see who gets the utility
           '''
           board_state = cfr_game_state.board_cards
           p1 = cfr_game_state.p1_hole
           p2 = cfr_game_state.p2_hole


           ret = Evaluator.evaluate_cards(*((board_state + p1)))
           ret2 = Evaluator.evaluate_cards(*((board_state + p2)))


           print("RET VALUES: {}, {}".format(ret, ret2))
           if(ret < ret2):
               if(cur_player==0):
                    return math.log(cfr_game_state.pot_size)
               else:
                    return -math.log(cfr_game_state.pot_size)
           if(ret2 < ret):
                if(cur_player == 1):
                    return math.log(cfr_game_state.pot_size)
                else:
                    return -math.log(cfr_game_state.pot_size)
           return 0



    def train_abstract_actions(self, player_id):
        possible_actions = ['R66', 'R25', 'R75', 'R125', 'F', 'C']



    def get_all_abstracted_actions(self, player_id):
        cur_game_state = self.game_state
        cur_round_state = self.round_state
        stacks = cur_round_state.stacks
        pot_size = (RoundState.STARTING_STACK - stacks[0]) + (RoundState.STARTING_STACK - stacks[1])
        possible_actions = [RaiseAction(0.66*pot_size), RaiseAction(0.25*pot_size), RaiseAction(0.75*pot_size), RaiseAction(1.5*pot_size), CheckAction, FoldAction]

        player_stack = self.stacks[0] if player_id == 0 else self.stacks[1]
        for i in range(len(possible_actions)-1,-1,-1):
            if(isinstance(possible_actions[i], RaiseAction) and possible_actions[i]['amount'] > player_stack):
                del possible_actions[i]

        return possible_actions

