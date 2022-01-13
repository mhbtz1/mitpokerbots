import eval7
import typing

class EquityEvaluator:
    def __init__(self, range1, range2, board):
        self.range1 = range1
        self.range2 = range2
        self.board = board

    def evaluate_hand_vs_range_equity(self, hand, range, board):
        ans = eval7.py_hand_vs_range_exact(hand, range, board)
        return ans

    def evaluate_range_vs_range_equity(self):
        ans = 0
        range1 = self.range1
        range2 = self.range2
        board = self.board
        prop_range = {}
        for hand in range1.hands:
            (act_hand, prob) = hand
            ret = self.evaluate_hand_vs_range_equity(act_hand,range2,board)
            if(ret not in prop_range):
                prop_range[ret] = 0
            prop_range[ret] += 1

        get_sum = 0
        for i in prop_range.values():
            get_sum += i
        ans = 0
        for i,k in prop_range.items():
            ans += (float(k)/float(get_sum))*i
        return ans

hr = eval7.HandRange("AJ+, ATs, KQ+, 33-JJ, 0.8(QQ+, KJs)")
hr2 = eval7.HandRange("AA, KK")
board = [eval7.Card("As"), eval7.Card("9c"), eval7.Card("Qh")]

eqev = EquityEvaluator(hr, hr2, board)
print(eqev.evaluate_range_vs_range_equity())

