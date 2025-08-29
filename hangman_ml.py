import random
from collections import Counter, defaultdict
import time

class HangmanMLAgent:
    def __init__(self, dictionary_file):
        self.full_dictionary = self._load_dictionary(dictionary_file)
        self.positional_frequency = defaultdict(Counter)
        self.bigram_frequency = defaultdict(Counter)
        self.overall_frequency = Counter()
        self.train()

    def _load_dictionary(self, file_path):
        with open(file_path, 'r') as f:
            return [word.strip().lower() for word in f if len(word.strip()) > 3]

    def train(self):
        for word in self.full_dictionary:
            for i, letter in enumerate(word):
                self.overall_frequency[letter] += 1
                self.positional_frequency[i][letter] += 1
                if i > 0:
                    prev_letter = word[i-1]
                    self.bigram_frequency[prev_letter][letter] += 1
        print("✅ Agent has been trained with advanced positional and bigram models.")

    def guess(self, current_word, guessed_letters, verbose=False):
        """
        Makes an intelligent guess and prints its thought process if verbose is True.
        """
        possible_words = self._filter_dictionary(current_word, guessed_letters)
        
        # --- Primary Strategy: Analyze the filtered word list ---
        if possible_words:
            possible_letters = "".join(possible_words)
            frequency = Counter(possible_letters)
            
            for letter, _ in frequency.most_common():
                if letter not in guessed_letters:
                    if verbose:
                        print(f"    - Thought Process: Found {len(possible_words)} possible words. Most common letter is '{letter}'.")
                    return letter

        # --- Fallback Strategy: Use the advanced models ---
        letter_scores = defaultdict(float)
        for i, char in enumerate(current_word):
            if char == '_':
                for letter, count in self.positional_frequency[i].items():
                    if letter not in guessed_letters:
                        letter_scores[letter] += count
            else:
                if i + 1 < len(current_word) and current_word[i+1] == '_':
                    for next_letter, count in self.bigram_frequency[char].items():
                        if next_letter not in guessed_letters:
                            letter_scores[next_letter] += count * 1.5
        
        if letter_scores:
            best_guess = max(letter_scores, key=letter_scores.get)
            if verbose:
                print(f"    - Thought Process: Using advanced positional/bigram models. Best guess is '{best_guess}'.")
            return best_guess

        # --- Final Fallback: Use the most common overall letter ---
        for letter, _ in self.overall_frequency.most_common():
            if letter not in guessed_letters:
                if verbose:
                    print(f"    - Thought Process: Using final fallback (overall frequency). Best guess is '{letter}'.")
                return letter
        
        final_guess = random.choice([l for l in "abcdefghijklmnopqrstuvwxyz" if l not in guessed_letters])
        if verbose:
            print(f"    - Thought Process: Using random guess. Chose '{final_guess}'.")
        return final_guess


    def _filter_dictionary(self, current_word, guessed_letters):
        word_len = len(current_word)
        possible_words = []
        for word in self.full_dictionary:
            if len(word) != word_len:
                continue
            matches = True
            for i, char in enumerate(word):
                if current_word[i] == '_' and char in guessed_letters:
                    matches = False
                    break
                if current_word[i] != '_' and current_word[i] != char:
                    matches = False
                    break
            if matches:
                possible_words.append(word)
        return possible_words


class HangmanGame:
    def __init__(self, secret_word, max_tries=6):
        self.secret_word = secret_word.lower()
        self.max_tries = max_tries
        self.tries_left = max_tries
        self.guessed_letters = set()
        self.current_word = ['_'] * len(self.secret_word)

    def make_guess(self, letter):
        if not letter or letter in self.guessed_letters: return
        self.guessed_letters.add(letter)
        if letter in self.secret_word:
            for i, char in enumerate(self.secret_word):
                if char == letter: self.current_word[i] = letter
        else:
            self.tries_left -= 1

    def is_won(self): return '_' not in self.current_word
    def is_lost(self): return self.tries_left <= 0


if __name__ == "__main__":
    NUMBER_OF_GAMES_TO_TEST = 100
    agent = HangmanMLAgent('words.txt')
    total_wins = 0
    start_time = time.time()
    
    print(f"\n--- Running Self-Test for {NUMBER_OF_GAMES_TO_TEST} Games ---")

    for game_number in range(NUMBER_OF_GAMES_TO_TEST):
        # Set verbose to True only for the first game
        verbose = (game_number == 0)
        
        secret_word = random.choice(agent.full_dictionary)
        game = HangmanGame(secret_word)
        
        if verbose:
            print(f"\n--- Tracing Game 1 (Word: {secret_word}) ---")
            print(f"Initial Word: {' '.join(game.current_word)}")

        while not game.is_won() and not game.is_lost():
            guess = agent.guess("".join(game.current_word), game.guessed_letters, verbose=verbose)
            
            if verbose:
                print(f"  > Agent guesses: '{guess}'")
            
            game.make_guess(guess)

            if verbose:
                print(f"    New Word: {' '.join(game.current_word)}")

        if game.is_won():
            total_wins += 1
            print(f"Game {game_number + 1}: WON! Word was '{secret_word}'")
        else:
            print(f"Game {game_number + 1}: LOST. Word was '{secret_word}'")
            
    end_time = time.time()
    
    efficiency = (total_wins / NUMBER_OF_GAMES_TO_TEST) * 100
    total_time = end_time - start_time
    
    print("\n--- Test Results (Corrected Model) ---")
    print(f"Total Games Played: {NUMBER_OF_GAMES_TO_TEST}")
    print(f"Total Wins: {total_wins}")
    print(f"Total Time: {total_time:.2f} seconds")
    print(f"Agent Efficiency (Win Rate): {efficiency:.2f}% 🏆")