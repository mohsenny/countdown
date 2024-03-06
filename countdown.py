import random
from colorama import Fore, Style, init
import threading
import time
import sys

# Initialize Colorama
init()

def load_word_list(file_path):
    with open(file_path, 'r') as file:
        return {line.strip().lower() for line in file if "'" not in line}

WORDS = load_word_list("en_US-large.txt")

# Define vowels and consonants with frequencies (weights)
VOWELS = 'AEIOU'
CONSONANTS = 'BCDFGHJKLMNPQRSTVWXYZ'
VOWEL_WEIGHTS = [8.167, 12.702, 8.496, 7.507, 12.072]  # Example weights, adjust based on real frequencies
CONSONANT_WEIGHTS = [4.49, 6.78, 5.85, 5.21, 6.09, 6.96, 7.50, 4.92, 6.01, 5.40, 5.74, 7.50, 2.36, 6.32, 9.05, 8.75, 5.97, 3.03, 3.32, 2.10, 2.15]  # Example weights

def is_word_valid(word, letters):
    word = word.lower()  # Convert to lowercase for comparison
    return word in WORDS and all(word.count(c) <= ''.join(letters).lower().count(c) for c in word)

def get_longest_word(letters):
    letters = ''.join(letters).lower()  # Work with lowercase
    longest_word = ""
    for word in WORDS:
        if all(letters.count(c) >= word.count(c) for c in word) and len(word) <= len(letters):
            if len(word) > len(longest_word):
                longest_word = word
    return longest_word.upper()  # Return in uppercase for consistent display


def countdown(t):
    for i in range(t, 0, -1):
        mins, secs = divmod(i, 60)
        print(f"{mins:02d}:{secs:02d}", end='\r')
        time.sleep(1)
    print("\nTime is up! Enter your word now.")

def weighted_choice(choices, weights):
    return random.choices(choices, weights=weights, k=1)[0]

def main():
    letters = ['_'] * 9  # Initialize with underscores for empty slots
    print("Letters so far: " + ' | '.join(letters), end='\r')
    sys.stdout.flush()

    for i in range(9):
        # Clear the line and reprint instructions to avoid confusion
        sys.stdout.write("\033[K")  # ANSI escape sequence to clear the line
        print("Hello and welcome to Countdown! \nA show about letters, numbers, and conundrum! \nChoose 'v' for a vowel, 'c' for a consonant: ", end='', flush=True)
        choice = sys.stdin.readline().strip().lower()  # Use readline to avoid line break
        if choice == 'v':
            letter = weighted_choice(VOWELS, VOWEL_WEIGHTS).upper()
        elif choice == 'c':
            letter = weighted_choice(CONSONANTS, CONSONANT_WEIGHTS).upper()
        else:
            print(Fore.RED + "\nInvalid choice. Please enter 'v' for vowel or 'c' for consonant." + Style.RESET_ALL)
            continue

        letters[i] = letter  # Update the selected letter
        sys.stdout.write("\rLetters so far: " + ' | '.join(letters) + ' ' * 20)  # Overwrite the previous line, add space to ensure previous text is cleared
        sys.stdout.flush()

    # Start 30 seconds countdown in a separate thread
    print("\nYou have 30 seconds starting now!")
    countdown_thread = threading.Thread(target=countdown, args=(30,))
    countdown_thread.start()
    countdown_thread.join()

    # Input word after the countdown
    print("Your time is up! Please enter your word: ", end='')
    player_word = sys.stdin.readline().strip()

    longest_word = get_longest_word(letters)
    if longest_word and player_word.upper() == longest_word:
        print(Fore.GREEN + f"Congratulations! You've found the longest possible word: {player_word} ({len(player_word)} letters)" + Style.RESET_ALL)
    elif is_word_valid(player_word, letters):
        print(Fore.GREEN + f"Valid word! Length: {len(player_word)}" + Style.RESET_ALL)
        print(Fore.CYAN + f"The longest word possible was: {longest_word} ({len(longest_word)} letters)" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Invalid word." + Style.RESET_ALL)
        if longest_word:
            print(Fore.CYAN + f"The longest word possible was: {longest_word} ({len(longest_word)} letters)" + Style.RESET_ALL)
        else:
            print(Fore.CYAN + "No valid words could be formed from the selected letters." + Style.RESET_ALL)

if __name__ == "__main__":
    main()