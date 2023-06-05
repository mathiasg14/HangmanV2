import tkinter as tk
import re
import requests
from PIL import Image, ImageTk
import os 

cwd = os.getcwd()
end_point = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
random_word = 'https://random-word-api.herokuapp.com/word'

## 1) Welcome to the Hangman game and choice between playing against another player or against the computer
def find_indices(input_list, item): # Checks for all the instances of an item in the list and returns the indices
    indices = []
    for idx, value in enumerate(input_list):
        if value == item:
            indices.append(idx)
    return indices

def vscomp_event(): # This is what happenes if chooses to play against the computer
    response = requests.get(random_word)
    global sec_wrd
    sec_wrd = response.text[2:-2].lower().strip()

    if text_entry.get() == '':
        greeting_lbl.config(text='Player name cannot be blank, please enter a valid name: ')
        return
    global player_name
    player_name = text_entry.get()
    text_entry.delete(0,tk.END)
    greeting_lbl.config(text=f"Playing against the PC. {player_name} Enter your guess: ")
    
    vscomp_btn.destroy()
    vsplayer_btn.destroy()
    
    global guessed_letters
    guessed_letters = ['__'] * len(sec_wrd)

    guess_lbl.config(text=' '.join(guessed_letters))
    sec_wrd_lbl.config(text=f'Secret Word ({len(sec_wrd)}):\n{" ".join(guessed_letters)}')
   
    enterguess_btn.pack(side=tk.LEFT)
       
    return

def game_loop():
    global hm_counter
    global guessed_letters
    global sec_wrd
    global img

    guess = text_entry.get().lower().strip()
    
    if guess == '' or  not bool(check_letter.findall(guess)):
        greeting_lbl.config(text='Guess cannot be blank and must be a letter: ')
        text_entry.delete(0,tk.END)
        return
    elif len(guess) > 1:
        greeting_lbl.config(text='Guess must be a single letter: ')
        text_entry.delete(0,tk.END)
        return
    elif guess in incorrect_guess_list or guess in guessed_letters:
        greeting_lbl.config(text='You have already guessed that letter! Try again: ')
        text_entry.delete(0,tk.END)
        return
    
    guess_check = find_indices(sec_wrd, guess)

    if not guess_check and hm_counter < (len(hangman_states) - 1):
        hm_counter += 1
        incorrect_guess_list.append(guess)
        greeting_lbl.config(text='That guess was wrong, please try again: ')
        inc_gss_lbl.config(text=f"Incorrect Guesses ({hm_counter}/{len(hangman_states)}):\n{','.join(incorrect_guess_list)}")
        img = ImageTk.PhotoImage(Image.open(hangman_states[hm_counter]))
        frame1.create_image(0,0, image=img, anchor='nw')
        text_entry.delete(0,tk.END)
        return
    
    elif guess_check:
        for pos in guess_check:
            guessed_letters[pos] = guess
        if "".join(guessed_letters) == sec_wrd:
            greeting_lbl.config(text='The word was ' + sec_wrd + '\nYou have guessed correctly. You win!')
            text_entry.destroy()
            text_entry.destroy()
            enterguess_btn.destroy()
            exitgame_btn.pack(side=tk.LEFT)
            return quit
        else:
            greeting_lbl.config(text='That guess was correct. Enter guess: ')
            sec_wrd_lbl.config(text= f'Secret Word ({len(sec_wrd)}):\n {" ".join(guessed_letters)}')
            text_entry.delete(0,tk.END)
            return
       
    elif hm_counter == (len(hangman_states) - 1):
        hm_counter += 1
        img = ImageTk.PhotoImage(Image.open(hangman_states[hm_counter]))
        frame1.create_image(0,0, image=img, anchor='nw')
        greeting_lbl.config(text='That was your last guess. The word was "' + sec_wrd + '" You lost!')
        text_entry.destroy()
        enterguess_btn.destroy()
        exitgame_btn.pack(side=tk.LEFT)
        return quit

def exit_game():
    window.destroy()
    return quit

#Hangman Variables
hm_counter = 0 
incorrect_guess_list = []
check_letter = re.compile(r'[a-zA-Z]')
hangman_states = {
    1:'hm1.png',
    2:'hm2.png',
    3:'hm3.png',
    4:'hm4.png',
    5:'hm5.png',
    6:'hm6.png',
    7:'hm7.png',
}

# Main Window Generation


img = None
                        
window = tk.Tk()
window.title('HANGMAN GAME')
frame0 = tk.Frame(master=window, relief=tk.RIDGE, borderwidth=2, width = 400, height = 250, bg='gray') # This is the status frame
frame1 = tk.Canvas(master=window, relief=tk.RIDGE, borderwidth=2, width= 400, height = 400, bg='white') # This will be the main HUD with hangman figurine
frame2 = tk.Frame(master=window, relief=tk.RIDGE, borderwidth=2, height=100) # Here go the instructions
frame3 = tk.Frame(master=window, relief=tk.RIDGE, borderwidth=2, height=100) # Here go the interactive elements for the player
                        
                        # Initial Window Greeting and Layouts
inc_gss_lbl = tk.Label(master=frame0, text= f"Incorrect Guesses ({hm_counter}/{len(hangman_states)}):")
inc_list_lbl = tk.Label(master=frame0)
sec_wrd_lbl = tk.Label(master=frame0, text= "Secret Word: ")
guess_lbl = tk.Label(master=frame0)
img = ImageTk.PhotoImage(Image.open(cwd + "\\HangmanTitleCard.png"))
frame1.create_image(0,0, image=img, anchor='nw')
greeting_lbl = tk.Label(master=frame2, text="Welcome to the Hangman Game, please enter your name and choose your game mode:")

text_entry = tk.Entry(master=frame3)
vscomp_btn = tk.Button(master=frame3, text="Vs. Computer", command = vscomp_event)
vsplayer_btn = tk.Button(master=frame3, text="Vs. Player")
enterguess_btn = tk.Button(master=frame3, text='Enter Guess', command = game_loop)
exitgame_btn = tk.Button(master=frame3, text='Exit Game', command = exit_game)

frame0.grid(row=0,column=0)
frame1.grid(row=0,column=1)
frame2.grid(row=1,columnspan=2)
frame3.grid(row=2,columnspan=2)

inc_gss_lbl.pack(fill='x')
inc_list_lbl.pack(fill='x')
sec_wrd_lbl.pack(fill="x")

greeting_lbl.pack()

text_entry.pack(side=tk.LEFT, padx='100')
vscomp_btn.pack(side=tk.LEFT)
vsplayer_btn.pack(side=tk.LEFT)

window.mainloop()


## 2) Players enter names of guesser and host 



# def vsplayer_event(event):
#     greeting_lbl = tk.Label(master=frame2, text="You have chosen to play against another player.")
#     plyrnm_lbl = tk.Label(text="Please enter guesser's name: ")
#     plyrnm_entry = tk.Entry()
#     plyrnm_btn = tk.Button(text="Enter")


    # while True:
    #     player_name = input('Please input the players name: ').strip()
    #     if not player_name:
    #         print('That is not a valid player name, please try again.')
    #     else:
    #         break
    # while True:
    #     host_name = input('You have chosen to play against a player, please input the host\'s name: ').strip()
    #     if not host_name:
    #         print('That is not a valid host name, please try again.')
    #     else:
    #         break
    # while True:
    #     secret_word = input(host_name + ' please choose your secret word: ').strip().lower()
    #     response = requests.get(end_point + secret_word)
    #     if not secret_word:
    #         print('The secret word cannot be blank, please try again')
    #     elif not response.status_code == 200:
    #         print('That word is not in our dictionary. Please try again.')
    #     else:
    #         break

## 3) If against a Host, he chooses a secret word; if against a computer, a random word is generated from a predefined list
## 4) Main Game Loop continues until the word is guessed or the player runs out of guesses
##      a) Interface lets the player know how many letters in the secret word (and that there are no guesses or wrong guesses)
##      b) Player chooses a letter to guess, rules to follow: it must be a letter, it shouldn't have been guessed before
##      c) If the letter is in the secret word, all the positions in which that letter appears must be revealed
##      d) If the letter is not in the secret word, its added to the incorrect guesses and the hangman counter (represented by a drawing) increases by 1
## 5) Once Main Game Loop concludes the player loses (and the secret word is revealed) or the player wins by guessing the whole word
