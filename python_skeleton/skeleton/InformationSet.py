class InformationSet:
    '''
    Maintain information for indistinguishable states in our game tree using this InformationSet class; will be implemented to map a string of actions to an InformationSet
    '''

    def __init__(self, num_actions):
        self.infoSet = ""
        self.num_actions = num_actions
        self.strategy = np.zeros(num_actions)
        self.strategySum = np.zeros(num_actions)
        self.regretSum = np.zeros(num_actions)
        self.regret = np.zeros(num_actions)
        self.actionUtility = np.zeros(num_actions)

    def acc_regret(self, opp, strategy):
        '''
        Used for regret matching with RPS (not used anymore)
        '''
        actions = KuhnPoker.get_all_actions()
        my_action = self.getAction()
        other_action = opp.getAction()

        '''
        Compute action utilities
        '''
        self.kuhn_action_utilities(opp, my_action, other_action)

        for i in range(self.num_actions):
            self.regret[i] = (self.actionUtility[i] - self.actionUtility[my_action])
            self.regretSum[i] += self.regret[i]

    def getAction(self):
        '''
        Actions 0...n indicates discarding card i (0 <= i <= n) and drawing from deck
        Actions n+1...2*n indicates discarding i (n+1 <= i <= 2*n) and drawing from top burn card
        '''
        r = random.uniform(0, 1)
        sm = 0
        cumul_prob = 0
        while (sm < self.num_actions - 1):
            cumul_prob += self.strategy[sm]
            if (r < cumul_prob):
                break
            sm += 1
        return sm

    def normalize(self, strat):
        if (sum(strat) > 0):
            strat /= sum(strat);
            # print("NORMALISED: {}".format(strat))
        else:
            strat = np.array([float(1) / float(self.num_actions)] * self.num_actions)
            # print("NORMALISED: {}".format(strat))
        return strat

    def getStrategy(self, reach_probability):
        strat = np.maximum(0, self.regretSum)
        strat = self.normalize(strat)
        self.strategySum += reach_probability * strat
        self.strategy = strat
        # print("STRATEGY: {}".format(self.strategy))
        return self.strategy

    def getAverageStrategy(self):
        '''
        Gets average mixed strategy over self.num_actions iterations
        '''
        return self.normalize(self.strategySum.copy())

    def __str__(self):
        return self.infoSet + ": " + str(self.getAverageStrategy())