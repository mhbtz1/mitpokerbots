from python_skeleton.skeleton.actions import CallAction, CheckAction, FoldAction, RaiseAction


class RangeEvaluator():
    def __init__ (self, our_range, enemy_range, prev_actions):
        self.our_range = our_range
        self.enemy_range = enemy_range
        self.prev_actions = prev_actions

    def update_ranges(self, current_action):
        if(isinstance(current_action, CheckAction)):
            pass
        elif(isinstance(current_action, CallAction)):
            pass
        elif(isinstance(current_action, RaiseAction)):
            pass

