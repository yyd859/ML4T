""""""  		  	   		  		 		  		  		    	 		 		   		 		  
"""Assess a betting strategy.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
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
  		  	   		  		 		  		  		    	 		 		   		 		  
Student Name: Yingdong Yang (replace with your name)  		  	   		  		 		  		  		    	 		 		   		 		  
GT User ID: yyang3052 (replace with your User ID)  		  	   		  		 		  		  		    	 		 		   		 		  
GT ID: 903952220 (replace with your GT ID)  		  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  

import numpy as np
from matplotlib import pyplot as plot
from pathlib import Path
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
def author():  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		  		 		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    return "yyang3052"  # replace tb34 with your Georgia Tech username.
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
def gtid():  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    :return: The GT ID of the student  		  	   		  		 		  		  		    	 		 		   		 		  
    :rtype: int  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    return 903952220  # replace with your GT ID number
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
def get_spin_result(win_prob):  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
    :param win_prob: The probability of winning  		  	   		  		 		  		  		    	 		 		   		 		  
    :type win_prob: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :return: The result of the spin.  		  	   		  		 		  		  		    	 		 		   		 		  
    :rtype: bool  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    result = False
    if np.random.random() <= win_prob:  		  	   		  		 		  		  		    	 		 		   		 		  
        result = True
    return result

def strategy_without_bank_roll(win_prob):
    '''
    Professor Balch’s actual betting strategy
    '''
    l1=[0]
    episode_winnings = 0
    run_times=1
    while run_times<=1000:
        while episode_winnings <80:
            if run_times>1000:
                break
            won = False
            bet_amount = 1
            while won== False and run_times<=1000:
                won=get_spin_result(win_prob=win_prob)
                if won == True:
                    episode_winnings = episode_winnings + bet_amount
                else:
                    episode_winnings = episode_winnings - bet_amount
                    bet_amount = bet_amount * 2
                l1.insert(run_times,episode_winnings)
                run_times = run_times + 1
        l1.insert(run_times,episode_winnings)
        run_times = run_times + 1
    return(l1)
def strategy_with_bank_roll(win_prob,bank_roll=256):
    '''
    Professor Balch’s actual betting strategy
    '''
    l1 = [0]
    episode_winnings = 0
    run_times=1
    while run_times <= 1000:
        while episode_winnings <80:
                if run_times>1000:
                    break
                if episode_winnings <= -bank_roll:
                    break
                won = False
                bet_amount = 1
                while won== False and run_times<=1000:
                    if episode_winnings<=-bank_roll:
                        break
                    won=get_spin_result(win_prob=win_prob)
                    if won == True:
                        episode_winnings = episode_winnings + bet_amount
                    else:
                        episode_winnings = episode_winnings - bet_amount
                        if episode_winnings - 2*bet_amount>-bank_roll:
                            bet_amount = bet_amount * 2
                        else:
                            bet_amount=bank_roll+episode_winnings
                    l1.insert(run_times, episode_winnings)
                    run_times = run_times + 1
        l1.insert(run_times, episode_winnings)
        run_times = run_times + 1
    return(l1)



def main_run_1(episode_number,win_prob):
    i=[]
    for j in range(0,episode_number):
        results=strategy_without_bank_roll(win_prob=win_prob)
        i.insert(j,results)
    i=np.array(i)
    return i
def main_run_2(episode_number,win_prob):
    i=[]
    for j in range(0,episode_number):
        results=strategy_with_bank_roll(win_prob=win_prob)
        i.insert(j,results)
    i=np.array(i)
    return i
def test_code():
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    Method to test your code  		  	   		  		 		  		  		    	 		 		   		 		  
    """
    script_directory = Path(__file__).resolve().parent
    win_prob = 0.474 #bet on black (18 blacks out of 38 slots)  # set appropriately to the probability of a win
        # add your code here to implement the experiments
    ##set the random seed
    np.random.seed(gtid())
    ##Experiment1 Figure 1
    e1f1=main_run_1(episode_number=10,win_prob=win_prob)
    plot.figure()
    for index, data in enumerate(e1f1):
        plot.plot(data, label=f'Spin {index + 1}')
    #set x,y axis limits
    plot.xlim([0,300])
    plot.ylim([-256,100])
    #add legend
    plot.legend()
    # Add labels
    plot.xlabel('Spin')
    plot.ylabel('Winnings($)')
    plot.title('E1F1(no bankroll limit)')
    plot.savefig(script_directory/'images/E1F1')
    ##Experiment1 Figure 2
    plot.figure()
    e1f2=main_run_1(episode_number=1000,win_prob=win_prob)
    mean_value=np.mean(e1f2,axis=0)
    std_values = np.std(e1f2, axis=0)
    plot.plot(mean_value,label='mean')
    plot.plot(mean_value+std_values,label='mean+std')
    plot.plot(mean_value-std_values,label='mean-std')
    plot.xlim([0,300])
    plot.ylim([-256,100])
    plot.xlabel('Spin')
    plot.ylabel('Winnings($)')
    plot.legend()
    plot.title('E1F2 (no bankroll limit)')
    plot.savefig(script_directory/'images/E1F2')
    ##Experiment1 Figure 3
    plot.figure()
    e1f2=main_run_1(episode_number=1000,win_prob=win_prob)
    median_value=np.median(e1f2,axis=0)
    std_values = np.std(e1f2, axis=0)
    plot.plot(median_value,label='median')
    plot.plot(median_value+std_values,label='median+std')
    plot.plot(median_value-std_values,label='median-std')
    plot.xlim([0,300])
    plot.ylim([-256,100])
    plot.xlabel('Spin')
    plot.ylabel('Winnings($)')
    plot.legend()
    plot.title('E1F3 (no bankroll limit)')
    plot.savefig(script_directory/'images/E1F3')
    ##Experiment2 Figure 1
    e2f1=main_run_2(episode_number=1000,win_prob=win_prob)
    plot.figure()
    mean_value=np.mean(e2f1,axis=0)
    std_values = np.std(e2f1, axis=0)
    plot.plot(mean_value,label='mean')
    plot.plot(mean_value+std_values,label='mean+std')
    plot.plot(mean_value-std_values,label='mean-std')
    plot.xlim([0,1000])
    plot.ylim([-256,300])
    plot.xlabel('Spin')
    plot.ylabel('Winnings($)')
    plot.legend()
    plot.title('E2F1 (with bankroll limit=$256)')
    plot.savefig(script_directory/'images/E2F1')
    ##Experiment 2 Figure 2
    plot.figure()
    median_value=np.median(e2f1,axis=0)
    std_values = np.std(e2f1, axis=0)
    plot.plot(median_value,label='median')
    plot.plot(median_value+std_values,label='median+std')
    plot.plot(median_value-std_values,label='median-std')
    plot.xlim([0,300])
    plot.ylim([-256,100])
    plot.xlabel('Spin')
    plot.ylabel('Winnings($)')
    plot.legend()
    plot.title('E2F2 (with bankroll limit=$256)')
    plot.savefig(script_directory/'images/E2F2.png')
win_prob=0.47

if __name__ == "__main__":
    test_code()
#     a=main_run_2(episode_number=1000,win_prob=win_prob)
# p80=0
# p256=0
# for i in a:
#     if i[-1]==80:
#         p80=p80+1
#     if i[-1]==-256:
#         p256=p256+1
# print(p80)
# print(p256)
