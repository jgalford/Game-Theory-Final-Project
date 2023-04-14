import random
from collections import Counter
import itertools

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

    return get_result(random_num, p1_in_or_out, p2_in_or_out)
    
def get_winner(p1_score, p2_score):
    if p1_score > p2_score:
        #print(f"Player 1 wins: {result[0]} to {result[1]}")
        return '1'
    elif p1_score < p2_score:
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

def run_game(runs, p1_strat, p2_strat, isPrint):
    p1_total_score = 0
    p2_total_score = 0
    counter = Counter()
    counter2 = Counter()
    for i in range(runs):
        curr_result1 = play_game(p1_strat, p2_strat)
        p1_total_score += curr_result1[0]
        p2_total_score += curr_result1[1]
        curr_result2 = play_game(p2_strat, p1_strat)
        p1_total_score += curr_result2[1]
        p2_total_score += curr_result2[0]
        counter.update(get_winner(curr_result1[0], curr_result2[1]))
        counter2.update(get_winner(curr_result2[1], curr_result1[0]))

    p1_win_rate = (counter['1'] + counter2['2']) / (counter['1'] + counter['2'] + counter2['1'] + counter2['2'])
    p1_average_score = p1_total_score/runs
    p2_win_rate = (counter['2'] + counter2['1']) / (counter['1'] + counter['2'] + counter2['1'] + counter2['2'])
    p2_average_score = p2_total_score/runs

    if isPrint:
        print(p1_strat)
        print(p2_strat)
        print(counter)
        print(f"Player 1 win rate: {p1_win_rate} with an average score of {p1_average_score}")
        print(f"Player 2 win rate: {p2_win_rate} with an average score of {p2_average_score}")

    return (p1_win_rate, p1_average_score, p2_win_rate, p2_average_score)

def find_best_pure_strat():
    choices = [['low', 'middle', 'high'],
               ['in|yes', 'out|yes'],
               ['in|no', 'out|no'],
               ['in|p1_in_&_prime', 'out|p1_in_&_prime'],
               ['in|p1_out_&_prime', 'out|p1_out_&_prime'],
               ['in|p1_in_&_composite', 'out|p1_in_&_composite'],
               ['in|p1_out_&_composite', 'out|p1_out_&_composite']]
    all_pure_strats = list(itertools.product(*choices))

    # print(all_pure_strats)
    # print(len(all_pure_strats))
    
    best_strat = None
    best_strat_win_rate = 0
    best_strat_score = 0
    i = 1

    for strat1 in all_pure_strats:
        for strat2 in all_pure_strats:
            result = run_game(10000, strat1, strat2, False)
            if result[1] > best_strat_score:
                best_strat = strat1
                best_strat_win_rate = result[0]
                best_strat_score = result[1]
            if result[3] > best_strat_score:
                best_strat = strat2
                best_strat_win_rate = result[2]
                best_strat_score = result[3]
        print('Processing: ' + str(i) + ' of ' + str(len(all_pure_strats)))
        i += 1
    
    return (best_strat, best_strat_win_rate, best_strat_score)

if __name__ == "__main__":
    #EX: p1_strat = ['low', 'in|yes', 'in|no', 'in|p1_in_&_prime', 'in|p1_in_&_composite', 'in|p1_out_&_prime', 'in|p1_out_&_composite']
    #EX: p2_strat = ['low', 'in|yes', 'in|no', 'in|p1_in_&_prime', 'in|p1_in_&_composite', 'in|p1_out_&_prime', 'in|p1_out_&_composite']
    p1_strat = random_strat()
    p2_strat = random_strat()

    #run_game(1000000, p1_strat, p2_strat, True)

    pure_strat = find_best_pure_strat()
    best_pure_strat = pure_strat[0]
    best_pure_strat_win_rate = pure_strat[1]
    best_pure_strat_score = pure_strat[2]

    print(f"Best pure strategy: {best_pure_strat}")
    print(f"Best pure strategy win rate: {best_pure_strat_win_rate}")
    print(f"Best pure strategy score: {best_pure_strat_score}")