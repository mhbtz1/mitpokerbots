from python_skeleton.skeleton.actions import CallAction, CheckAction, FoldAction, RaiseAction
import eval7

class PreflopHandRanges:
    BTN_RFI = eval7.HandRange("A2s-AA, K2s-AKo,Q2s-AQo,J2s-AJo,T2s-ATo,92s-A9o,82s-A8o,72s-A7o,62s-A6o,52s-A5o,42s-74s,Q4o-A4p.32s-53o,K3o-A3o,22,K2o-A2o")
    BB_3BET = eval7.HandRange("ATs-AA,KTs-AKo,QTs-QQ,AQo,88-JJ,45s-JTs,0.75(35s-J9s,Q9s,K9s),0.5(AJo,KQo,A2s-A9s,J8s-K8s,T7s-K7s.36s-T7s)")
    BB_CALL = eval7.HandRange('55-22, A9s-A2s, K9s-K2s, Q9s-Q2s, J9s-J2s, T7s-T2s, 97s-92s, 86s-82s, 75s-72s, 64s-62s, 53s-52s, 42s+, 32s, AJo-A2o, K2o+, Q3o+, J5o+, T5o+, 95o+, 85o+, 75o+, 64o+, 53o+, 43o')
    BTN_4BET = eval7.HandRange('TT-AA, AKs, AKo, 0.5(AQs), 0.15(AQo)')
    BTN_CALL_VERSUS_3BET = eval7.HandRange('99-22,AQs-A2s,K2s+,Q2s+,J3s+,T4s+,94s+,84s+,73s+,62s+,52s+,42s+,32s,AQo-A8o,A5o-A4o,K9o+,Q9o+,J9o+,T9o')
    BB_5BET = eval7.HandRange('JJ-AA, AKo, AKs, 0.5(AQs,TT)')
    BB_CALL_VERSUS_4BET = eval7.HandRange('TT-44,AQs-A8s,A5s-A2s,K7s+,Q8s+,J8s+,T8s+,97s+,87s,76s,65s,54s,43s,AQo-AJo,KQo')

    sequence = [BTN_RFI, BB_CALL, BB_3BET, BTN_CALL_VERSUS_3BET, BTN_4BET, BB_CALL, BB_CALL_VERSUS_4BET]



class RangeEvaluator():
    def __init__ (self, our_range, enemy_range, prev_actions, our_position, enemy_position):
        self.our_range = our_range
        self.enemy_range = enemy_range
        self.prev_actions = prev_actions
        self.our_position = our_position
        self.enemy_position = enemy_position

    def update_ranges(self, current_action, stage_in_game):
        if(stage_in_game == "PREFLOP"):
            if(isinstance(current_action, CheckAction)):
                pass
            elif(isinstance(current_action, CallAction)):
                pass
            elif(isinstance(current_action, RaiseAction)):
                amount = current_action['amount']
        else:
            if(isinstance(current_action,CheckAction)):
                pass
            elif(isinstance(current_action, CallAction)):
                pass
            elif(isinstance(current_action, RaiseAction)):
                amount = current_action['amount']
                pass


