import random 
import time

operators = ['+', '*' , '-']
min_operand = 3
max_operand = 12
total_questions = 10

def generate_question():
    left = random.randint(min_operand,max_operand)
    right = random.randint(min_operand,max_operand)
    operator = random.choice(operators)
    question = str(left) + operator + str(right)
    answer = eval(question)
    print(answer)
    return question, answer

wrong = 0
start_time = time.time()

print('Supply the correct answers to the following questions')
for i in range(total_questions):
    question, answer = generate_question()
    while True:
        print('Question ', i+1)
        guess = input(f'{question}: ')
        if int(guess) == answer:
            break
        print('Wrong')
        wrong += 1
        
end_time = time.time()

time_elasped = end_time - start_time
print(f'You finished in {time_elasped:.2f} seconds')
print('You guessed wrong ', wrong, ' times') 
