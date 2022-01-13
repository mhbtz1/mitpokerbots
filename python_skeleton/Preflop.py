import eval7

class PreflopHandRanges:
    BTN_RFI = eval7.HandRange('22+,A2s+,K2s+,Q2s+,J2s+,T2s+,92s+,82s+,72s+,62s+,52s+,42s+,32s,A2o+,K2o+,Q2o+,J4o+,T5o+,95o+,85o+,74o+,64o+,53o+,43o')
    BB_3BET = eval7.HandRange('77+, ATs+, K9s+, QTs+, J9s+, T8s+, 98s, 87s, 76s, 65s, 54s, AJo+')
    BB_CALL = eval7.HandRange('66, 33-22, A9s-A2s, K8s-K2s, Q8s-Q2s, J6s-J2s, T7s-T2s, 95s-92s, 84s-82s, 73s-72s, 63s-62s, 52s, 42s+, 32s, AJo-A2o, K2o+, Q3o+, J5o+, T6o+, 96o+, 86o+, 76o')
    BTN_4BET = eval7.HandRange('TT+,AQs+,AKo')
    BTN_CALL_VERSUS_3BET = eval7.HandRange('88-22, AJs-A2s, K2s+, Q4s+, J5s+, T5s+, 95s+, 84s+, 74s+, 63s+, 53s+, 43s, AQo-A8o, A5o-A4o, K9o+, Q9o+, J9o+, T9o')
    BB_5BET = eval7.HandRange('JJ+,AKs,AKo')
    BB_CALL_VERSUS_4BET = eval7.HandRange('TT-55, AQs-A9s, A5s-A4s, K8s+, Q8s+, J8s+, T8s+, 97s+, 87s, 76s, 65s, 54s, AQo')

    sequence = [BTN_RFI, BB_CALL, BB_3BET, BTN_CALL_VERSUS_3BET, BTN_4BET, BB_CALL, BB_CALL_VERSUS_4BET]


