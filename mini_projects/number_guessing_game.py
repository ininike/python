import random

print("Let's play a guessing game!");
odds = None
while True:
    odds = input('What are the odds? (The largest of the range)\n');

    if odds.isdigit():
        odds = int(odds);
        
        if odds <= 0:
            print('Please enter a number greater than zero');
            continue;
        else:
            break;
    else:
        print('Please enter a number')

number = random.randint(1,odds);
guess = None ;
number_of_guesses = 0;

while str(number)!=guess:
    number_of_guesses += 1
    guess = input('Guess a number between 1 and ' + str(odds) + '\n');
    if not guess.isdigit():
        print('Please enter a number');
        continue
    if int(guess) != number:
        print('You guessed wrong');
        continue
    print('You guessed right!');
    print('It took you ' + str(number_of_guesses) + ' tries');  
        
    
    
            
            


