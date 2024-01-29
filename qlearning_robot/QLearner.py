""""""  		  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  
Template for implementing QLearner  (c) 2015 Tucker Balch  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		  		 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		  		 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		  		 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		  		 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 		  		  		    	 		 		   		 		  
or edited.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		  		 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		  		 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		  		 		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		  	   		  		 		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
import random
  		  	   		  		 		  		  		    	 		 		   		 		  
import numpy as np  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
class QLearner(object):  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    This is a Q learner object.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
    :param num_states: The number of states to consider.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type num_states: int  		  	   		  		 		  		  		    	 		 		   		 		  
    :param num_actions: The number of actions available..  		  	   		  		 		  		  		    	 		 		   		 		  
    :type num_actions: int  		  	   		  		 		  		  		    	 		 		   		 		  
    :param alpha: The learning rate used in the update rule. Should range between 0.0 and 1.0 with 0.2 as a typical value.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type alpha: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :param gamma: The discount rate used in the update rule. Should range between 0.0 and 1.0 with 0.9 as a typical value.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type gamma: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :param rar: Random action rate: the probability of selecting a random action at each step. Should range between 0.0 (no random actions) to 1.0 (always random action) with 0.5 as a typical value.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type rar: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :param radr: Random action decay rate, after each update, rar = rar * radr. Ranges between 0.0 (immediate decay to 0) and 1.0 (no decay). Typically 0.99.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type radr: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :param dyna: The number of dyna updates for each regular update. When Dyna is used, 200 is a typical value.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type dyna: int  		  	   		  		 		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    def __init__(  		  	   		  		 		  		  		    	 		 		   		 		  
        self,  		  	   		  		 		  		  		    	 		 		   		 		  
        num_states=100,  		  	   		  		 		  		  		    	 		 		   		 		  
        num_actions=4,  		  	   		  		 		  		  		    	 		 		   		 		  
        alpha=0.2,  		  	   		  		 		  		  		    	 		 		   		 		  
        gamma=0.9,  		  	   		  		 		  		  		    	 		 		   		 		  
        rar=0.5,  		  	   		  		 		  		  		    	 		 		   		 		  
        radr=0.99,  		  	   		  		 		  		  		    	 		 		   		 		  
        dyna=0,  		  	   		  		 		  		  		    	 		 		   		 		  
        verbose=False,  		  	   		  		 		  		  		    	 		 		   		 		  
    ):
        # Initialize parameters
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.verbose = verbose


        self.Q = np.zeros((num_states, num_actions))


        self.s = None
        self.a = None

        # For Dyna-Q, initialize model T and R (used to store experiences)
        self.T = dict()  # transition probabilities
        self.R = dict()  # rewards
        self.experiences = []

    def author(self):
        """
        :return: The GT username of the student
        :rtype: str
        """
        return "yyang3052"  # replace tb34 with your Georgia Tech username.
    def _choose_action(self, state):
        if random.random() < self.rar:  # Choose a random action with probability rar
            return random.randint(0, self.num_actions - 1)
        else:  # Choose the action with the maximum Q value for the current state
            return np.argmax(self.Q[state, :])

    def _update_dyna(self):
        for _ in range(self.dyna):
            s, a, s_prime, r = random.choice(self.experiences)
            max_q_next = np.max(self.Q[s_prime, :])
            self.Q[s, a] = (1 - self.alpha) * self.Q[s, a] + self.alpha * (r + self.gamma * max_q_next)

    def query(self, s_prime, r):
        """Update Q table and return the next action."""
        # Update Q table if s and a are not None (i.e., not the first time step)
        if self.s is not None and self.a is not None:
            max_q_next = np.max(self.Q[s_prime, :])
            self.Q[self.s, self.a] = (1 - self.alpha) * self.Q[self.s, self.a] + self.alpha * (
                        r + self.gamma * max_q_next)

            # For Dyna-Q, store the experience and update model T and R
            if self.dyna:
                self.experiences.append((self.s, self.a, s_prime, r))

                # Update model for T
                if (self.s, self.a) not in self.T:
                    self.T[(self.s, self.a)] = dict()
                if s_prime not in self.T[(self.s, self.a)]:
                    self.T[(self.s, self.a)][s_prime] = 0
                self.T[(self.s, self.a)][s_prime] += 1

                # Update model for R
                self.R[(self.s, self.a)] = r

                self._update_dyna()

        # Update the current state and action
        self.s = s_prime
        self.a = self._choose_action(s_prime)

        # Decay the random action rate
        self.rar *= self.radr

        return self.a

    def querysetstate(self, s):
        """Set the state without updating the Q table and return the next action."""
        self.s = s
        self.a = self._choose_action(s)
        return self.a


if __name__ == "__main__":
    print("Remember Q from Star Trek? Well, this isn't him")  		  	   		  		 		  		  		    	 		 		   		 		  
