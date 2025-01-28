with open('story.txt','r') as f:
    story = f.read()

start_of_word = '<'
end_of_word = '>'

start_index = -1
words = set() #set cuz the same fill in words are repeated in the story and we just want one of each

for i, char in enumerate(story):
    if char == start_of_word:
        start_index = i
    
    if char == end_of_word and start_index != -1:
        word = story[start_index:i+1]
        words.add(word)
        start_index = -1

print('Fill in the story with (a/an)')

for word in words:
    answer = input(f'{word[1:-1]}: ')
    story = story.replace(word, answer)
     
print(story)