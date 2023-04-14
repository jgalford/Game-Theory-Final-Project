import random
from collections import Counter

# Number is 1-3
matrix1 = [
    [(3,3), (1,2)],
    [(0,2), (2,1)]
]

# Number is 4-6
matrix2 = [
    [(0,5), (2,2)],
    [(1,1), (5,3)]
]

# Number is 7-9
matrix3 = [
    [(1,1), (7,2)],
    [(2,5), (3,3)]
]

def get_in_out_p1(player1_strat, num):
    guess = player1_strat[0]
    yes_response = player1_strat[1]
    no_response = player1_strat[2]

    if guess == 'low' and num >= 1 and num <=4:
        return yes_response.split('|')[0]
    elif guess == 'middle' and num >= 5 and num <=7:
        return yes_response.split('|')[0]
    elif guess == 'high' and num >= 8 and num <=9:
        return yes_response.split('|')[0]
    else:
        return no_response.split('|')[0]
    
def get_in_out_p2(player2_strat, p1_in_or_out, p_or_c):
    if p1_in_or_out == 'in':
        if p_or_c == 'prime':
            return player2_strat[3].split('|')[0]
        else:
            return player2_strat[4].split('|')[0]
    else:
        if p_or_c == 'prime':
            return player2_strat[5].split('|')[0]
        else:
            return player2_strat[6].split('|')[0]
    
def is_prime(num):
    if num > 1:
        for i in range(2, int(num/2)+1):
            if num % i == 0:
                return 'composite'
        return 'prime'
    else:
        return 'composite'
    
def get_result(num, p1_in_or_out, p2_in_or_out):
    payoff_table = None
    if num >= 1 and num <= 3:
        payoff_table = matrix1
    elif num >= 4 and num <= 6:
        payoff_table = matrix2
    else:
        payoff_table = matrix3

    if p1_in_or_out == 'in' and p2_in_or_out == 'in':
        return payoff_table[0][0]
    elif p1_in_or_out == 'in' and p2_in_or_out == 'out':
        return payoff_table[0][1]
    elif p1_in_or_out == 'out' and p2_in_or_out == 'in':
        return payoff_table[1][0]
    else:
        return payoff_table[1][1]

def play_game(player1_strat, player2_strat):
    random_num = random.randint(1,9)

    p1_in_or_out = get_in_out_p1(player1_strat, random_num)

    p_or_c = is_prime(random_num)

    p2_in_or_out = get_in_out_p2(player2_strat, p1_in_or_out, p_or_c)

    result = get_result(random_num, p1_in_or_out, p2_in_or_out)

    if result[0] > result[1]:
        #print(f"Player 1 wins: {result[0]} to {result[1]}")
        return '1'
    elif result[0] < result[1]:
        #print(f"Player 2 wins: {result[1]} to {result[0]}")
        return '2'
    else:
        #print(f"Tie: {result[0]} to {result[1]}")
        return 'T'

def random_strat():
    return [random.choice(['low', 'middle', 'high']), 
            random.choice(['in|yes', 'out|yes',]),
            random.choice(['in|no', 'out|no',]),
            random.choice(['in|p1_in_&_prime', 'out|p1_in_&_prime',]),
            random.choice(['in|p1_out_&_prime', 'out|p1_out_&_prime',]),
            random.choice(['in|p1_in_&_composite', 'out|p1_in_&_composite',]),
            random.choice(['in|p1_out_&_composite', 'out|p1_out_&_composite',])]

if __name__ == "__main__":
    #p1_strat = ['low', 'in|yes', 'in|no', 'in|p1_in_&_prime', 'in|p1_in_&_composite', 'in|p1_out_&_prime', 'in|p1_out_&_composite']
    #p2_strat = ['low', 'in|yes', 'in|no', 'in|p1_in_&_prime', 'in|p1_in_&_composite', 'in|p1_out_&_prime', 'in|p1_out_&_composite']
    p1_strat = random_strat()
    print(p1_strat)
    p2_strat = random_strat()
    print(p2_strat)

    counter = Counter()
    for i in range(1000000):
        counter.update(play_game(p1_strat, p2_strat))
        counter.update(play_game(p2_strat, p1_strat))

    #NOTE:
    #currently setup for two random pure strategies
    #in order to do mixed strategyies do something like this:
    #for i in range(1000000):
    #    if random.random() < 0.5:
    #        counter.update(play_game(p1_strat_mixed1, p2_strat))
    #        counter.update(play_game(p2_strat, p1_strat_mixed1))
    #    else:
    #        counter.update(play_game(p1_strat_mixed2, p2_strat))
    #        counter.update(play_game(p2_strat, p1_strat_mixed2))

    print(counter)
    p1_win_rate = counter['1'] / (counter['1'] + counter['2'])
    p2_win_rate = counter['2'] / (counter['1'] + counter['2'])

    print(f"Player 1 win rate: {p1_win_rate}")
    print(f"Player 2 win rate: {p2_win_rate}")