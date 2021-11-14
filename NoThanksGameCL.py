import sys
from dataclasses import dataclass
import random
from itertools import groupby
from operator import itemgetter
from typing import Generator, Any


@dataclass()
class PlayedCard:
    curent: int | None
    counter: int


class Player:
    _id = 1

    def __init__(self, counters: int):
        self.counters: int = counters
        self.hand: list = []
        self.number = Player._id
        Player._id += 1

    def make_a_choice(self, played_card: PlayedCard, deck_of_cards: list[int]):
        if not deck_of_cards:
            return
        # print("len(deck_of_cards)", len(deck_of_cards), '\n')

        print(f"The card is `{played_card.curent}` with `{played_card.counter}` counters")
        print(f"Player `{self.number}` cards are {self.hand} with `{self.counters}` counters")

        if self.counters <= 0:
            print("You have 0 counters. Take the card")
            input("Press any to continue!")
            self.counters += played_card.counter

            played_card.curent = deck_of_cards.pop()
            played_card.counter = 0
        else:

            while True:

                choice = input(f"[T] take the card, [C] or [P] to plase a token on the card \nPlayer {self.number} >")

                match choice.lower():
                    case "t":
                        self.counters += played_card.counter
                        self.hand.append(played_card.curent)

                        played_card.curent = deck_of_cards.pop()
                        played_card.counter = 0
                        self.make_a_choice(played_card, deck_of_cards)
                        break
                    case "c" | "p":
                        played_card.counter += 1
                        self.counters -= 1
                        break
                    case _:
                        print("REENTER ANSWERE")



def info(list_of_players: list[Player]):
    print("\n----------------------------")
    for player_n in list_of_players:
        print(f"Player {player_n.number} with a hand {player_n.hand} and counters {player_n.counters}")
    print("----------------------------\n")


def consecutive_groups(iterable, ordering=lambda x: x) -> Generator[map, Any, None]:
    for k, g in groupby(enumerate(iterable), key=lambda x: x[0] - ordering(x[1])):
        yield map(itemgetter(1), g)


def game_end(list_of_players: list[Player]):
    winner_score: int = sys.maxsize
    winner_number: int = 0

    print("\n----------------------------")
    for player_n in list_of_players:

        total_score: list[int] = []
        for group in consecutive_groups(sorted(player_n.hand)):

            items: list[int] = list(group)
            # print("group", items)
            if items:
                total_score.append(min(items))

        print(total_score)

        potencial_winner_score: int = sum(total_score) - player_n.counters

        print(f"Player {player_n.number} with a hand {potencial_winner_score} and counters {player_n.counters}")

        if winner_score > potencial_winner_score:
            winner_score = potencial_winner_score
            winner_number = player_n.number

    print("----------------------------\n")
    print(f"WINNER IS PLAYER {winner_number} with {winner_score}")


def main():
# ---- SETUP
    deck_of_cards: list[int] = [n for n in range(3, 36)]

    cards_to_remove: int = 9
    print(deck_of_cards)

    while cards_to_remove > 0:
        remove_card: int = random.choice(deck_of_cards)
        deck_of_cards.remove(remove_card)
        print("removed card", remove_card)

        cards_to_remove -= 1

    # print(deck_of_cards)
    print("shuffle deck_of_cards !")
    random.shuffle(deck_of_cards)
    # print(deck_of_cards)

    list_of_players: list[Player] = [Player(counters=11), Player(counters=11), Player(counters=11), Player(counters=11)]

    played_card = PlayedCard(deck_of_cards.pop(), 0)

# ---- MAIN LOOP
    is_running = True
    while is_running:

        for player_n in list_of_players:
            if not deck_of_cards:
                is_running = False
                break

            info(list_of_players)
            player_n.make_a_choice(played_card, deck_of_cards)


    game_end(list_of_players)


if __name__ == '__main__':
    main()
