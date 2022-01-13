'''
Simple example pokerbot, written in Python.
'''
import eval7


from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import STARTING_STACK
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot
import python_skeleton.Preflop as Preflop
import python_skeleton.MCCFR as MCCFR
import random
import python_skeleton.boardtype as boardtype

class Player(Bot):
    '''
    A pokerbot.
    '''

    def do_random_action(self,legal_actions,pot_size):
        action = legal_actions[random.uniform(0,len(legal_actions))]
        if(action == RaiseAction):
            return RaiseAction(0.25*pot_size)
        return action

    def locate_closest_strategy(current_line):

        max_sim_factor = 0
        ret_strat = []
        make_list = []
        for line in open('strategies.txt'):
            rep_line = line[0:line.index(':')]
            cur_sim = 0
            for i in range(0, len(rep_line), 3):
                cur_sim += rep_line[i:i + 3] == current_line[i + i + 3]
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
        f = open('strategies.txt', 'r')
        for line in f.readlines():
            poker_line = line[0:line.index(':')]
            strategy = line[line.index(':')+1:]
            Player.load_strategies[poker_line] = strategy
        self.current_line = ""
        self.count_preflop_actions = 0
        self.map_preflop_ranges = {}
        self.map_preflop_ranges['PREFLOP_SRP'] = (Preflop.BTN_RFI, Preflop.BB_CALL)
        self.map_preflop_ranges['PREFLOP_3BET'] = (Preflop.BTN_CALL_VERSUS_3BET, Preflop.BB_3BET)
        self.map_preflop_ranges['PREFLOP_4BET'] = (Preflop.BTN_4BET, Preflop.BTN_CALL_VERSUS_4BET)
        self.map_preflop_ranges['PREFLOP_5BET'] = (Preflop.BTN_CALL_VERSUS_5BET, Preflop.BB_5BET)
        self.cur_range = ()
        self.range_state = 0
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
        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        street = round_state.street  # 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        my_cards = round_state.hands[active]  # your cards
        board_cards = round_state.deck[:street]  # the board cards
        my_pip = round_state.pips[active]  # the number of chips you have contributed to the pot this round of betting
        opp_pip = round_state.pips[1-active]  # the number of chips your opponent has contributed to the pot this round of betting
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        continue_cost = opp_pip - my_pip  # the number of chips needed to stay in the pot
        my_contribution = STARTING_STACK - my_stack  # the number of chips you have contributed to the pot
        opp_contribution = STARTING_STACK - opp_stack  # the number of chips your opponent has contributed to the pot

        pot_size = my_contribution + opp_contribution

        if(self.current_line == '' and street == 3):
            self.current_line = str(my_cards[0])+str(my_cards[1])+str(board_cards)
        '''
        Hardcode preflop ranges based on type of actions
        '''

        '''
        code for handling preflop action
        '''
        if(street==0):
            if(active==0):
                if(self.range_state ==0):
                    if( (eval7.Card(my_cards[0]),eval7.Card(my_cards[1])) in Preflop.BTN_RFI.hands):
                        return RaiseAction(6)
                    else:
                        return FoldAction()
                elif(self.range_state==1):
                    if ((eval7.Card(my_cards[0]), eval7.Card(my_cards[1])) in Preflop.BB_3BET.hands):
                        return RaiseAction(random.uniform(18,27))
                    else:
                        return CallAction()
                elif(self.range_state==2):
                    if ((eval7.Card(my_cards[0]), eval7.Card(my_cards[1])) in Preflop.BTN_CALL_VERSUS_3BET.hands):
                        return CallAction()
                    else:
                        if ((eval7.Card(my_cards[0]), eval7.Card(my_cards[1])) in Preflop.BTN_4BET.hands):
                            return RaiseAction(random.uniform(65,100))
                        else:
                            return FoldAction()
                elif(self.range_state==3):
                    if ((eval7.Card(my_cards[0]), eval7.Card(my_cards[1])) in Preflop.BB_CALL_VERSUS_4BET.hands):
                        return CallAction()
                    else:
                        if ((eval7.Card(my_cards[0]), eval7.Card(my_cards[1])) in Preflop.BB_5BET.hands):
                            return RaiseAction(my_stack)
                        else:
                            return FoldAction()
        if(street == 0):
            self.range_state += 1
        elif(street != 0 and self.range_state != -1):
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

        '''
        determine last action taken by opponent
        '''
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
                self.current_line += 'C' + str(MCCFR.CFR_Game_State.action_translation(proportion))
                self.OUR_CURRENT_STACK = my_stack


        recommended_strategy = self.locate_closest_strategy(
            boardtype.boardtype(round_state.deck[:3]) + self.current_line)
        action = MCCFR.select_random_strategy(recommended_strategy)
        print("ACTION: {}".format(action))
        '''
        always apply MCCFR's recommendations with betting on streets
        '''
        if(street == 3 or street == 4 or street == 5):
            if(action==0):
                if(0.66 * pot_size <= my_stack):
                    return RaiseAction(0.66 * pot_size)
                else:
                    return self.do_random_action(legal_actions,pot_size)

            elif(action==1):
                if(0.75 * pot_size <= my_stack):
                    return RaiseAction(0.75 * pot_size)
                else:
                    return self.do_random_action(legal_actions,pot_size)

            elif(action == 2):
                if(0.8 * pot_size <= my_stack):
                    return RaiseAction(0.80 * pot_size)
                else:
                    return self.do_random_action(legal_actions,pot_size)

            elif(action == 3):
                if(2 * pot_size <= my_stack):
                    return RaiseAction(2 * pot_size)
                else:
                    return self.do_random_action(legal_actions,pot_size)

            elif(action == 4):
                if(CallAction in legal_actions):
                    return CallAction()
                else:
                    return self.do_random_action(legal_actions,pot_size)

            elif(action==5):
                if(CheckAction in legal_actions):
                    return CheckAction()
                else:
                    return self.do_random_action(legal_actions,pot_size)
            elif(action == 6):
                return FoldAction()

        #note: if cfr bot acts too aggressive and fucks us over, do some river heuristic coding to alleviate

        '''
        if FoldAction in legal_actions:
            return FoldAction()
        '''


if __name__ == '__main__':
    run_bot(Player(), parse_args())
