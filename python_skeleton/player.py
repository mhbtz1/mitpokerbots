'''
Simple example pokerbot, written in Python.
'''
import eval7


from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import STARTING_STACK
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot
import Preflop
import MCCFR
import random
import boardtype

class Player(Bot):
    '''
    A pokerbot.
    '''

    def do_random_action(self,legal_actions,min_raise):
        action = random.sample(legal_actions,1)[0]
        ans = 0
        if(action is RaiseAction):
            ans = RaiseAction(min_raise)
        else:
            ans = FoldAction()
        print("ACTION: {}".format(ans))
        return ans

    def parse_range(self, eval7_range):
        range = []
        for (card, prob) in eval7_range:
            range.append(card)
        return range

    def locate_closest_strategy(self, current_line):
        max_sim_factor = 0
        ret_strat = []
        make_list = []
        print("CURRENT LINE: {}".format(current_line))
        for line in open('strategies.txt'):
            rep_line = line[0:line.index(':')]
            cur_sim = 1 if rep_line[:3]==current_line[:3] else 0
            cur_sim += 1 if rep_line[3:6] == current_line[3:6] else 0
            for i in range(6, len(rep_line)-3, 3):
                cur_sim += 1 if rep_line[i:i + 3] == current_line[i : i + 3] else 0
            cur_strat = (line[line.index(':') + 2:len(line) - 2]).split(' ')
            true_strat = []
            for i in cur_strat:
                if (i == ''):
                    continue
                true_strat.append(float(i))
            if (max(max_sim_factor, cur_sim) == cur_sim):
                cur_sim = max_sim_factor
                ret_strat = true_strat
            make_list.append(true_strat)

        if (max_sim_factor == 0):
            return make_list[int(random.uniform(0, len(make_list)))]
        return ret_strat



    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.

        Arguments:
        Nothing.

        Returns:
        Nothing.
        '''
        boardtype.initialise_flop_dict()
        self.current_line = ""
        self.count_preflop_actions = 0
        self.map_preflop_ranges = {}
        self.map_preflop_ranges['PREFLOP_SRP'] = (Preflop.PreflopHandRanges.BTN_RFI, Preflop.PreflopHandRanges.BB_CALL)
        self.map_preflop_ranges['PREFLOP_3BET'] = (Preflop.PreflopHandRanges.BTN_CALL_VERSUS_3BET, Preflop.PreflopHandRanges.BB_3BET)
        self.map_preflop_ranges['PREFLOP_4BET'] = (Preflop.PreflopHandRanges.BTN_4BET, Preflop.PreflopHandRanges.BB_CALL_VERSUS_4BET)
        #self.map_preflop_ranges['PREFLOP_5BET'] = (Preflop.PreflopHandRanges.BTN_CALL_VERSUS_5BET, Preflop.PreflopHandRanges.BB_5BET)
        self.cur_range = ()
        self.range_state = -1
        self.PREFLOP_AGGRESSOR = -1
        self.OPPONENT_CURRENT_STACK = 200
        self.OUR_CURRENT_STACK = 200
        self.LAST_ACTION = -1

    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Nothing.
        '''

        #my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        #game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        #round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        #my_cards = round_state.hands[active]  # your cards
        #big_blind = bool(active)  # True if you are the big blind
        pass

    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        terminal_state: the TerminalState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        previous_state = terminal_state.previous_state  # RoundState before payoffs
        street = previous_state.street  # 0, 3, 4, or 5 representing when this round ended
        my_cards = previous_state.hands[active]  # your cards
        opp_cards = previous_state.hands[1-active]  # opponent's cards or [] if not revealed
        self.current_line=""
        self.range_state=-1
        self.OUR_CURRENT_STACK=200
        self.OPPONENT_CURRENT_STACK=200
        self.PREFLOP_AGGRESSOR=False


    def get_action(self, game_state, round_state, active):
        '''
        Where the magic happens - your code should implement this function.
        Called any time the engine needs an action from your bot.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Your action.
        '''
        if(self.range_state==-1):
            self.range_state = active #the actions that we do with ranges depends on our position (i.e. only BB can 3bet)

        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        street = round_state.street  # 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        my_cards = round_state.hands[active]  # your cards
        board_cards = round_state.deck[:street]  # the board cards
        my_pip = round_state.pips[active]  # the number of chips you have contributed to the pot this round of betting
        opp_pip = round_state.pips[1-active]  # the number of chips your opponent has contributed to the pot this round of betting
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        continue_cost = opp_pip - my_pip  # the number of chips needed to stay in the pot
        my_contribution = 200 - my_stack  # the number of chips you have contributed to the pot
        opp_contribution = 200 - opp_stack  # the number of chips your opponent has contributed to the pot



        print("STACK SIZES: {}".format(my_stack, opp_stack))
        pot_size = my_contribution + opp_contribution

        if(self.current_line == '' and street == 3):
            self.current_line = str(my_cards[0])+str(my_cards[1])
        

        print("CARDS: {}".format( (my_cards)))
        print(self.range_state, active)
        if(street==0):
            if(self.range_state ==0 and active == 0):
                print("SRP")
                if( (eval7.Card(my_cards[0]),eval7.Card(my_cards[1])) in self.parse_range(Preflop.PreflopHandRanges.BTN_RFI.hands)):
                    self.range_state += 2
                    print("OPEN")
                    return RaiseAction(6)
                else:
                    return FoldAction()
            elif(self.range_state==1):
                print("3BET")
                if ((eval7.Card(my_cards[0]), eval7.Card(my_cards[1])) in self.parse_range(Preflop.PreflopHandRanges.BB_3BET.hands)):
                    self.range_state += 2
                    print("3BET")
                    return RaiseAction(int(random.uniform(18,27)))
                else:
                    return CallAction()
            elif(self.range_state==2):
                self.range_state += 2
                print("4BET/CALL")
                if ((eval7.Card(my_cards[0]), eval7.Card(my_cards[1])) in self.parse_range(Preflop.PreflopHandRanges.BTN_CALL_VERSUS_3BET.hands)):
                    print("CALL")
                    return CallAction()
                else:
                    if ((eval7.Card(my_cards[0]), eval7.Card(my_cards[1])) in self.parse_range(Preflop.PreflopHandRanges.BTN_4BET.hands)):
                        return RaiseAction(int(random.uniform(65,100)))
                    else:
                        return FoldAction()
            elif(self.range_state==3):
                print("CALL/JAM")
                self.range_state += 2
                if ((eval7.Card(my_cards[0]), eval7.Card(my_cards[1])) in self.parse_range(Preflop.PreflopHandRanges.BB_CALL_VERSUS_4BET.hands)):
                    return CallAction()
                else:
                    if ((eval7.Card(my_cards[0]), eval7.Card(my_cards[1])) in self.parse_range(Preflop.PreflopHandRanges.BB_5BET.hands)):
                        return RaiseAction(my_stack)
                    else:
                        return FoldAction()

        if(street != 0 and self.range_state != -1):
          if(self.range_state == 2):
              self.cur_range = self.map_preflop_ranges['PREFLOP_SRP']
              if(active == 0):
                  self.PREFLOP_AGGRESSOR = True
          elif(self.range_state == 3):
              self.cur_range = self.map_preflop_ranges['PREFLOP_3BET']
              if(active == 1):
                  self.PREFLOP_AGGRESSOR = True
          elif(self.range_state == 4):
              self.cur_range = self.map_preflop_ranges['PREFLOP_4BET']
              if(active == 0):
                  self.PREFLOP_AGGRESSOR = True
          elif(self.range_state == 5):
              self.cur_range = self.map_preflop_ranges['PREFLOP_5BET']
              if (active == 0):
                  self.PREFLOP_AGGRESSOR = True

        if(street != 0):
            if(CallAction in legal_actions): #means we got raised
                sizing = self.OPPONENT_CURRENT_STACK - opp_stack
                proportion = float(sizing)/float(pot_size - sizing)
                self.current_line += 'R' + str(MCCFR.CFR_Game_State.action_translation(proportion))
                self.OPPONENT_CURRENT_STACK = opp_stack
            elif(CallAction not in legal_actions): #means thats opponent checked
                self.current_line += 'CHK'
            else: #opponent called one of our raises (if they folded, game would end)
                sizing = self.OUR_CURRENT_STACK - my_stack
                proportion = float(sizing)/float(pot_size-sizing)
                self.current_line += 'CAL'
                self.OUR_CURRENT_STACK = my_stack


        if(street == 3 or street == 4 or street == 5):
            prs = round_state.deck[:3][:]
            print("PRS: {}".format(prs))
            map_hand = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12,
                        'K': 13, 'A': 14}
            prs = [(map_hand[prs[0][0]], prs[0][1]), ((map_hand[prs[1][0]], prs[1][1])),
                   ((map_hand[prs[2][0]], prs[2][1]))]
            prs.sort()

            current_rep = boardtype.map_names[boardtype.boardtype(prs)[0]] + self.current_line
            recommended_strategy = self.locate_closest_strategy(current_rep)
            print("STRATEGY VECTOR: {}".format(recommended_strategy))
            action = MCCFR.select_random_strategy(recommended_strategy)
            # o = open('newActions.txt', 'w')
            # o.write(action)
            # o.write('\n')

            print("ACTION: {}".format(action))
            print("POT SIZE: {}".format(pot_size))
            print("MY STACK: {}".format(my_stack))
            min_raise, max_raise = round_state.raise_bounds()
            if(action==0):
                print(0.66*pot_size)
                if(RaiseAction in legal_actions):
                    amt = int(0.66*pot_size)
                    amt = min(max_raise,int(0.66*pot_size))
                    amt = max(min_raise,int(0.66*pot_size))
                    r = RaiseAction(amt)
                    return r
                elif(CheckAction in legal_actions):
                    return CheckAction()
                elif(CallAction in legal_actions):
                    return CallAction()
                else:
                    return FoldAction()
            elif(action==1):
                print(0.75 * pot_size)
                if(RaiseAction in legal_actions):
                    amt = int(0.75 * pot_size)
                    amt = min(max_raise, int(0.66 * pot_size))
                    amt = max(min_raise, int(0.66 * pot_size))
                    r = RaiseAction(amt)
                    return r
                elif(CheckAction in legal_actions):
                    return CheckAction()
                else:
                    return FoldAction()
            elif(action == 2):
                print(0.80 * pot_size)
                if(RaiseAction in legal_actions):
                    amt = int(0.80*pot_size)
                    amt = min(max_raise, int(0.80 * pot_size))
                    amt = max(min_raise, int(0.80 * pot_size))
                    r = RaiseAction(amt)
                    return r
                elif(CheckAction in legal_actions):
                    return CheckAction()
                elif (CallAction in legal_actions):
                    return CallAction()
                else:
                    return FoldAction()
            elif(action == 3):
                print(2 * pot_size)
                if(RaiseAction in legal_actions):
                    amt = int(2* pot_size)
                    amt = min(max_raise, int(2 * pot_size))
                    amt = max(min_raise, int(2 * pot_size))
                    r = RaiseAction(amt)
                    return r
                elif(CheckAction in legal_actions):
                    return CheckAction()
                elif (CallAction in legal_actions):
                    return CallAction()
                else:
                    return FoldAction()
            elif(action == 4):
                if(CallAction in legal_actions):
                    return CallAction()
                else:
                    print("RUN THIS")
                    return self.do_random_action(legal_actions,min_raise)
            elif(action==5):
                if(CheckAction in legal_actions):
                    return CheckAction()
                else:
                    print("RUN THIS")
                    return self.do_random_action(legal_actions,min_raise)
            elif(action == 6):
                return FoldAction()

        #note: if cfr bot acts too aggressive and fucks us over, do some river heuristic coding to alleviate



if __name__ == '__main__':
    run_bot(Player(), parse_args())
