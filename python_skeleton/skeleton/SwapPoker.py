from python_skeleton.skeleton.actions import FoldAction, CallAction, RaiseAction, CheckAction
from python_skeleton.skeleton.states import GameState, RoundState
import typing
import MCCFR

class SwapPoker:
    def __init__(self, game_state, round_state, board_cards):
        self.game_state = game_state
        self.round_state = round_state
        self.board_cards = board_cards
        self.monte_carlo_solver = MCCFR()

    def update_board(self, new_board):
        self.board_cards = new_board


    @staticmethod
    def utility(self, history):
        current_player = 0 if len(history)%2 == 0 else 1
        if(isinstance(self.p1_last_action, FoldAction)):
            pass
        else:
            pass



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

