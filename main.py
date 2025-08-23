import json
import random
from pathlib import Path
from pyfiglet import Figlet

DATA_FILE= Path("flashcards.json")

f = Figlet(font='slant')



def load_flashcards():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def save_flashcards(cards):
    with open(DATA_FILE, "w") as file:
        json.dump(cards, file, indent=2)

def add_flashcard(cards):
    q = input("Input Question: ")
    a = input("Input Answer: ")
    cards.append({"question": q, "answer": a})
    save_flashcards(cards)
    print("Flashcars added successfully")

def list_flashcards(cards): 
    if not cards:
        print("No cards found :< ")
        return
    for i, card in enumerate(cards, start=1):
        print(f"{i}. {card['question']} -> {card['answer']}")

def study(cards):
    if not cards:
        print("No cards found :< ")
        return
    card = random.choice(cards)
    print(f"Question {card['question']}")
    input("Press enter to reveal the answer...")
    print(f'Answeer: {card['answer']}')

def main():
    cards = load_flashcards()
    while True:
        print('\n')
        print(f.renderText('ALQUIZAM'))
        print("1. Add flashcards")
        print("2. List flashcards")
        print("3. Study flashcards")
        print("4. Quit")

        choice = input("Choice: ")
        if choice == "1":
            add_flashcard(cards)
        elif choice =='2':
            list_flashcards(cards)
        elif choice == '3':
            study(cards)
        elif choice == '4':
            print("tsk... that's what i thought")
            break
        else: 
            print("Why are you tryna break me??? ")
        
if __name__ == "__main__":
    main()