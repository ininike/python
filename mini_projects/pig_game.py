import random

def roll():
    return random.randint(1,6);

players = 0
while True:
    players = input('Enter the amount of players (2-4)\n');
    if not players.isdigit():
        print('Please enter a number');
        continue
    players = int(players)
    if not (2 <= players <= 4):
        print('Please enter a numeber between 2 and 4');
        continue
    break
        
players_scores = [0 for x in range(players)]

max_score = 50

while max(players_scores) < max_score:
    for player_index in range(players):
        print('Player ', player_index +1 , "it's your turn!")
        current_score = 0
        
        while True:
            should_roll = input('Would you lke to roll? (y/n)\n')
            if should_roll == 'n':
                break
            
            value = roll()
            
            if value == 1:
                print('You rolled a 1 ... tough :(')
                current_score = 0
                break
            
            if value != 1:
                print('You rolled a ', value, '!')
                current_score += value
                print('You have accumulated ', current_score, 'points!')
                
        players_scores[player_index] += current_score
        print('Turn ended\nYour total points are ', players_scores[player_index], ' points!')
        if players_scores[player_index] >= 50:
            print('Player ', player_index, ' wins!!!!')

        
        
            
            
    
    
