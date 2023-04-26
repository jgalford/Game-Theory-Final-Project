import random
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
    if num == 2:
        return 'prime'

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
        #print(f"Player 1 wins: {p1_score} to {p2_score}")
        return '1'
    elif p1_score < p2_score:
        #print(f"Player 2 wins: {p2_score} to {p1_score}")
        return '2'
    else:
        #print(f"Tie: {p1_score} to {p2_score}")
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
    p1_wins = 0
    p2_wins = 0
    for i in range(runs):
        curr_result1 = play_game(p1_strat, p2_strat)
        p1_total_score += curr_result1[0]
        p2_total_score += curr_result1[1]
        curr_result2 = play_game(p2_strat, p1_strat)
        p1_total_score += curr_result2[1]
        p2_total_score += curr_result2[0]
        winner1 = get_winner(curr_result1[0], curr_result1[1])
        if winner1 == '1':
            p1_wins += 1
        elif winner1 == '2':
            p2_wins += 1
        winner2 = get_winner(curr_result2[1], curr_result2[0])
        if winner2 == '1':
            p1_wins += 1
        elif winner2 == '2':
            p2_wins += 1


    p1_win_rate = p1_wins / (p1_wins + p2_wins)
    p1_average_score = p1_total_score/runs
    p2_win_rate = p2_wins / (p1_wins + p2_wins)
    p2_average_score = p2_total_score/runs

    if isPrint:
        print(p1_strat)
        print(p2_strat)
        print(f"Player 1 win rate: {p1_win_rate} with an average score of {p1_average_score} and a total score of {p1_total_score}")
        print(f"Player 2 win rate: {p2_win_rate} with an average score of {p2_average_score} and a total score of {p2_total_score}")

    return (p1_win_rate, p1_average_score, p2_win_rate, p2_average_score, p1_total_score, p2_total_score)

def find_average_winrate_and_score(runs, target_strat, all_strats):
    total_win_rate = 0
    total_score = 0
    num_strats = len(all_strats)

    for strat2 in all_strats:
        win_rate1, score1, win_rate2, score2, total_score1, total_score2 = run_game(runs, target_strat, strat2, False)
        total_win_rate += win_rate1
        total_score += score1
    
    avg_win_rate = total_win_rate/num_strats
    avg_score = total_score/num_strats

    return target_strat, avg_win_rate, avg_score

def find_top_10_pure_strats(runs):
    choices = [['low', 'middle', 'high'],
               ['in|yes', 'out|yes'],
               ['in|no', 'out|no'],
               ['in|p1_in_&_prime', 'out|p1_in_&_prime'],
               ['in|p1_out_&_prime', 'out|p1_out_&_prime'],
               ['in|p1_in_&_composite', 'out|p1_in_&_composite'],
               ['in|p1_out_&_composite', 'out|p1_out_&_composite']]
    all_pure_strats = list(itertools.product(*choices))

    top_10_strats = [([None], 0, 0)] * 10
    i = 1

    def update_top_10_strats(strat, win_rate, score):
        for idx, (s, wr, sc) in enumerate(top_10_strats):
            if score > sc:
                if strat not in [s for s, _, _ in top_10_strats]:
                    top_10_strats.insert(idx, (strat, win_rate, score))
                    top_10_strats.pop(-1)
                    break

    for strat1 in all_pure_strats:
        result = find_average_winrate_and_score(runs, strat1, all_pure_strats)
        update_top_10_strats(result[0], result[1], result[2])
        print('Processing: ' + str(i) + ' of ' + str(len(all_pure_strats)))
        i += 1

    return top_10_strats

def run_game_mixed(runs, percent, mixed1, mixed2, all_strats):
    runs1 = int(runs*percent)
    #print(f"Runs1: {runs1}")
    runs2 = int(runs*(1-percent))
    #print(f"Runs2: {runs2}")
    total_win_rate = 0
    total_score = 0
    num_strats = len(all_strats)

    for strat2 in all_strats:
        if runs1 > 0:
            win_rate1, score1, _, _, _, _ = run_game(runs1, mixed1, strat2, False)
            total_win_rate += win_rate1
            total_score += score1
        if runs2 > 0:
            win_rate2, score2, _, _, _, _ = run_game(runs2, mixed2, strat2, False)
            total_win_rate += win_rate2
            total_score += score2

    avg_win_rate = (total_win_rate/2)/num_strats
    avg_score = (total_score/2)/num_strats

    return avg_win_rate, avg_score, percent, mixed1, mixed2

def find_best_mixed(iterator, runs):
    choices = [['low', 'middle', 'high'],
               ['in|yes', 'out|yes'],
               ['in|no', 'out|no'],
               ['in|p1_in_&_prime', 'out|p1_in_&_prime'],
               ['in|p1_out_&_prime', 'out|p1_out_&_prime'],
               ['in|p1_in_&_composite', 'out|p1_in_&_composite'],
               ['in|p1_out_&_composite', 'out|p1_out_&_composite']]
    all_pure_strats = list(itertools.product(*choices))

    top_10_strats = [('middle', 'out|yes', 'in|no', 'in|p1_in_&_prime', 'in|p1_out_&_prime', 'in|p1_in_&_composite', 'in|p1_out_&_composite'),
                     ('middle', 'out|yes', 'in|no', 'in|p1_in_&_prime', 'in|p1_out_&_prime', 'in|p1_in_&_composite', 'out|p1_out_&_composite'),
                     ('high', 'in|yes', 'out|no', 'in|p1_in_&_prime', 'in|p1_out_&_prime', 'in|p1_in_&_composite', 'in|p1_out_&_composite'),
                     ('middle', 'out|yes', 'in|no', 'in|p1_in_&_prime', 'in|p1_out_&_prime', 'out|p1_in_&_composite', 'in|p1_out_&_composite'),
                     ('high', 'in|yes', 'out|no', 'in|p1_in_&_prime', 'in|p1_out_&_prime', 'in|p1_in_&_composite', 'out|p1_out_&_composite'),
                     ('middle', 'out|yes', 'in|no', 'in|p1_in_&_prime', 'in|p1_out_&_prime', 'out|p1_in_&_composite', 'out|p1_out_&_composite'),
                     ('middle', 'out|yes', 'in|no', 'out|p1_in_&_prime', 'in|p1_out_&_prime', 'in|p1_in_&_composite', 'in|p1_out_&_composite'),
                     ('high', 'in|yes', 'out|no', 'in|p1_in_&_prime', 'in|p1_out_&_prime', 'out|p1_in_&_composite', 'in|p1_out_&_composite'),
                     ('low', 'in|yes', 'in|no', 'in|p1_in_&_prime', 'in|p1_out_&_prime', 'in|p1_in_&_composite', 'in|p1_out_&_composite'),
                     ('middle', 'in|yes', 'in|no', 'in|p1_in_&_prime', 'in|p1_out_&_prime', 'in|p1_in_&_composite', 'in|p1_out_&_composite')]
    
    mixed_strat_set = list(itertools.combinations(top_10_strats, 2))
    #print(mixed_strat_set[0][0])
    #print(mixed_strat_set[0][1])

    top_10_mixed_strats = [([None], [None], 0, 0, 0)] * 10
    curr_progress = 1

    def update_best_mixed_strats(strat1, strat2, percent1, win_rate, score):
        for idx, (s1, s2, p, wr, sc) in enumerate(top_10_mixed_strats):
            if score > sc:
                    top_10_mixed_strats.insert(idx, (strat1, strat2, percent1, win_rate, score))
                    top_10_mixed_strats.pop(-1)
                    break
            
    for strat1, strat2 in mixed_strat_set:
        for i in range(iterator):
            percent = (i/iterator)
            result = run_game_mixed(runs, percent, strat1, strat2, all_pure_strats)
            update_best_mixed_strats(strat1, strat2, percent, result[0], result[1])
        print('Processing: ' + str(curr_progress) + ' of ' + str(len(mixed_strat_set)))
        curr_progress += 1

    return top_10_mixed_strats

if __name__ == "__main__":
    #EX: p1_strat = ['low', 'in|yes', 'in|no', 'in|p1_in_&_prime', 'in|p1_in_&_composite', 'in|p1_out_&_prime', 'in|p1_out_&_composite']
    #EX: p2_strat = ['low', 'in|yes', 'in|no', 'in|p1_in_&_prime', 'in|p1_in_&_composite', 'in|p1_out_&_prime', 'in|p1_out_&_composite']
    #p1_strat = random_strat()
    #p2_strat = random_strat()
    #p1_strat = ['middle', 'out|yes', 'in|no', 'in|p1_in_&_prime', 'in|p1_out_&_prime', 'in|p1_in_&_composite', 'in|p1_out_&_composite']
    #p2_strat = ['high', 'in|yes', 'out|no', 'in|p1_in_&_prime', 'in|p1_out_&_prime', 'in|p1_in_&_composite', 'in|p1_out_&_composite']

    #run_game(1000000, p1_strat, p2_strat, True)

    # top_10_pure_strats = find_top_10_pure_strats(10000)
    # with open('best_pure_strats.txt', 'w') as f:
    #     for idx, (strat, win_rate, score) in enumerate(top_10_pure_strats):
    #         print(f"{idx + 1}. Strategy: {strat}, Win Rate: {win_rate}, Average Score: {score}")
    #         f.write(f"{idx + 1}. Strategy: {strat}, Win Rate: {win_rate}, Average Score: {score}" + '\n')

    top_10_mixed_strats = find_best_mixed(10, 10000)
    with open('best_mixed_strats.txt', 'w') as f:
        for idx, (strat1, strat2, percent1, win_rate, score) in enumerate(top_10_mixed_strats):
            print(f"{idx + 1}. Strategy 1: {strat1}, Strategy 2: {strat2}, Percent Strategy 1: {percent1}, Win Rate: {win_rate}, Average Score: {score}")
            f.write(f"{idx + 1}. Strategy 1: {strat1}, Strategy 2: {strat2}, Percent Strategy 1: {percent1}, Win Rate: {win_rate}, Average Score: {score}" + '\n')