class ActionWrapper:
    '''
    Describe action (CallAction, FoldAction, CheckAction, RaiseAction), and the corresponding amount if there is one
    '''
    def __init__(self, true_action, action_amount):
        self.true_action = true_action
        self.action_amount = action_amount

class RangeEvaluator():
    def __init__ (self, our_range, enemy_range, prev_actions):
        self.our_range = our_range
        self.enemy_range = enemy_range
        self.prev_actions = prev_actions


