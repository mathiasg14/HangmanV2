# Hangman Game

import re
import requests


# Function to identify the positions in which the guessed letter appears in the secret word
def find_indices(input_list, item):
    indices = []
    for idx, value in enumerate(input_list):
        if value == item:
            indices.append(idx)
    return indices


def hangman_ui(sec_wrd, plyr_name):
    hangman_states = [
        r"""
            _______
            |      |
            |
            |
            |
            |
            |
            |___
            """,
        r"""
            _______
            |      |
            |      O
            |
            |
            |
            |
            |___
            """,
        r"""
            _______
            |      |
            |      O
            |      |
            |      |
            |
            |
            |___
            """,
        r"""
            _______
            |      |
            |      O
            |     /|
            |      |
            |
            |
            |___
            """,
        r"""
            _______
            |      |
            |      O
            |     /|\
            |      |
            |
            |
            |___
            """,
        r"""
            _______
            |      |
            |      O
            |     /|\
            |      |
            |     /
            |
            |___
            """,
        r"""
            _______
            |      |
            |      O
            |     /|\
            |      |
            |     / \
            |
            |___
            """]
    hm_counter = 0
    guessed_letters = ['_'] * len(sec_wrd)
    incorrect_guesses = []
    check_letter = re.compile(r'[a-zA-Z]')

    while hm_counter < len(hangman_states):

        print('The secret word is: ', "".join(guessed_letters))
        if hm_counter == 0 or not incorrect_guesses:
            print('Status: No wrong guesses yet!')
        else:
            print('Status: \n' + hangman_states[hm_counter] + '\n' + 'Incorrect Guesses: ' + ','.join(incorrect_guesses))

        while True:
            guess = input(plyr_name + ' please input a letter as your guess: ').lower().strip()
            if guess in incorrect_guesses or guess in guessed_letters:
                print('You have already entered that letter! Try another one.')
            elif not guess or not bool(check_letter.findall(guess)):
                print('Guess cannot be a blank and must be a letter a-z. Please try again.')
            elif len(guess) > 1:
                print('Guess must be a single letter. Please try again.')
            else:
                break

        guess_check = find_indices(sec_wrd, guess)

        if not guess_check:
            hm_counter += 1
            incorrect_guesses.append(guess)
        else:
            for pos in guess_check:
                guessed_letters[pos] = guess

        if "".join(guessed_letters) == secret_word:
            print('The word was ' + secret_word + '\nYou have guessed correctly. You win!')
            break

        if hm_counter == len(hangman_states) - 1:
            print(hangman_states[-1] + '\nThe secret word was: ' + secret_word +
                                       '\nYou have lost the game. Sorry!')
            break


# api addresses for dictionary check and for random word generator
end_point = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
random_word = 'https://random-word-api.herokuapp.com/word'

# 1) One player is the host, one player is the guesser, or the player can play vs. the computer
# 2) If against a player, the host chooses a secret word, if against the computer a random word is generated
game_mode = ''

while True:
    game_mode = input(''''Welcome to the Hangman Game. Please choose if you want to play against a player or computer: 
    1 Player
    2 Computer
    ''')

    if game_mode not in ['1', '2']:
        print('That is not a valid choice.')
    else:
        break

if game_mode == '1':
    host_name = ''
    while True:
        host_name = input('You have chosen to play against a player, please input the host\'s name: ').strip()
        if not host_name:
            print('That is not a valid host name, please try again.')
        else:
            break
    while True:
        secret_word = input(host_name + ' please choose your secret word: ').strip().lower()
        response = requests.get(end_point + secret_word)
        if not secret_word:
            print('The secret word cannot be blank, please try again')
        elif not response.status_code == 200:
            print('That word is not in our dictionary. Please try again.')
        else:
            break
elif game_mode == '2':
    host_name = 'Computer'
    print('You have chosen to play against the computer. I will choose a secret word.')
    response = requests.get(random_word)
    secret_word = response.text[2:-2].lower().strip()

player_name = ''
while True:
    player_name = input('Please input the players name: ').strip()
    if not player_name:
        print('That is not a valid player name, please try again.')
    else:
        break

hangman_ui(secret_word, player_name)
