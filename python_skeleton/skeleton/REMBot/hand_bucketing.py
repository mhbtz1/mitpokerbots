import Hand

cards = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']

preflop_hand_bucketing = []

def create_bucketing():
    '''
    Consider large pocket pairs
    '''
    large_pp = []
    for i in range(6,len(cards)):
        large_pp.append(Hand(cards[i], cards[i], True))

    '''
    middle pocket pairs
    '''




    '''
    Jack, ten, or nine high disconnected hands
    '''

    brunson = []
    for i in range(7,10):
        for j in range(0,7):
            brunson.append(Hand(cards[i], cards[j], True))
            brunson.append(Hand(cards[i], cards[j], True))
    '''
    Offsuited and suited connectors
    '''
    connectors = []
    for i in range(0,len(cards)-1):
        connectors.append(Hand(cards[i], cards[i + 1], True))
        connectors.append(Hand(cards[i], cards[i + 1], True))

    '''
    Shitty broadways
    '''
    trash_broadways = []
    for i in range(9,len(cards)):
        for j in range(0,5):
            trash_broadways.append(Hand(cards[i], cards[j], True))
            trash_broadways.append(Hand(cards[i], cards[j], False))
    trash_broadways.append(Hand(cards[0], cards[0], False))

    '''
    Remaining broadways
    '''
    rem_broadways = []
    for i in range(9,len(cards)):
        for j in range(5,len(cards)):
            if(cards[i]==cards[j]):
                continue
            rem_broadways.append(Hand(cards[i], cards[j], True))
            rem_broadways.append(Hand(cards[i], cards[j], True))









