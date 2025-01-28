print('Hello');
playing = input("Do you want to play a game? (yes/no) \n");
if playing.lower() != "yes":
    quit(print('Bye'));
print("Okay let's play!");
score = 0
print("Attempt these 5 questions with a full name ");
answer = input('1. Who is the GOAT of Manhua  \n');
if answer.lower() == 'sung jin-woo':
    print('Correct');
    score += 1;
else:
    print('Incorrect');
answer = input('2. Who is the GOAT of Football \n');
if answer.lower() == 'lionel messi':
    print('Correct');
    score += 1;
else:
    print('Incorrect');
answer = input('3. Who is the GOAT of Basketball \n');
if answer.lower() == 'lebron james':
    print('Correct');
    score += 1;
else:
    print('Incorrect')
answer = input('4. Who is the GOAT of Twitch \n');
if answer.lower() == 'kai cenat':
    print('Correct');
    score += 1;
else:
    print('Incorrect');
answer = input('5. Who is the GOAT of Seinen Anime \n');
if answer.lower() == 'guts':
    print('Correct');
    score += 1;
else:
    print('Incorrect');
print('You got ' + str(score) + ' out of 5 questions correct.');
print('You got ' + str((score /5) * 100) + '%.');
