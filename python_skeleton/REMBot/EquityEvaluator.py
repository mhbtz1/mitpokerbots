class EquityEvaluator:
    def __init__(self, hand1, hand2, is_it_suited1, is_it_suited2):
        pass
    def evaluate_hand_equity(self):
        eq_1 = 4 if self.is_it_suited1 else 0
        eq_2 = 4 if self.is_it_suited1 else 0
        (o1, o2, offsuit) = self.hand1
        (e1, e2, offsuit) = self.hand2

    def evaluate_range_equity(self, range1, range2):
        pass
