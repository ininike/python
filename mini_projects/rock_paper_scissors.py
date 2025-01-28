import random

user_wins = 0;
user_losses = 0;

options = ['rock', 'paper', 'scissors'];

print('Let play rock-paper-scissors');
while True:
    
    user_pick =input('Enter rock, paper, or scissors or enter q to quit\n');
    
    if user_pick == 'q':
        print('You won ' + str(user_wins) + ' rounds and lost ' + str(user_losses) +' rounds')
        print('YOU WIN!' if user_wins > user_losses else 'YOU LOSE!')
        print('bye');
        quit();
    
    if user_pick not in options:
        print('Please enter rock paper or scissors');
        continue
    
    num = random.randint(0,2);
    computer_pick = options[num]
    
    rock_win = user_pick.lower() == 'rock' and computer_pick == 'scissors'
    paper_win = user_pick.lower() == 'paper' and computer_pick == 'rock'
    scissors_win = user_pick.lower() == 'scissors' and computer_pick == 'paper'
    
    class Vars:
        win = rock_win or paper_win or scissors_win
        draw = user_pick.lower() == computer_pick 
        lose = not win and not draw

    match True:
        case Vars.win: 
            print('You win this round')
            user_wins += 1
            continue
        case Vars.draw: 
            print('You drew this round')
            continue
        case Vars.lose: 
            print('You lose this round')
            user_losses += 1
            continue
            
    