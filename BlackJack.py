#-=-=-=-=-=-=-=-=-=-
#    IMPORTS
#-=-=-=-=-=-=-=-=-=-
from CardDeck import Spade
from CardDeck import Heart
from CardDeck import Diamond
from CardDeck import Club
from CardDeck import FaceDown
from random import choice


#-=-=-=-=-=-=-=-=-=-
#    FUNCTIONS
#-=-=-=-=-=-=-=-=-=-
def find_card_art(_num,_suit):
    '''
    INPUT: _num = the number on the card. _suit = the suit of the card.
    OUTPUT: The text art of the card with that num and suit.
    '''
    if _suit == 'Spade':
        return Spade.SpadeDeck[_num]
    elif _suit == 'Heart':
        return Heart.HeartDeck[_num]
    elif _suit == 'Diamond':
        return Diamond.DiamondDeck[_num]
    elif  _suit == 'Club':
        return Club.ClubDeck[_num]
    else:
        return FaceDown.face_down

def check_repeat(_card):
    '''
    INPUT: a Card object
    OUTPUT: return True if this card is already used in the game. Return False if it is not yet used.
    '''
    for i in PlayedDeck:
        if i == _card:
            return True
    else:
        return False

def get_rand_card():
    '''
    OUTPUT: Return a random card that has not been used in the game.
    '''
    while True:
        _num = choice(Card.NumList)
        _suit = choice(Card.SuitList)
        rand_card = Card(_num,_suit)
        if not check_repeat(rand_card):
            break
    return rand_card

def print_card(card_list):
    return_str = ''
    for i in range(9):
        for card in card_list:
            return_str += card.card_art[i] + '     '
        return_str += '\n'
    return return_str

def check_blackjack(card_list):
    return (card_list[0].num == 'A' and card_list[1].num == '10') or (card_list[1].num == 'A' and card_list[0].num == '10')

def count_point(card_list):
    point = 0
    a_counter = 0
    for card in card_list:
        _num = card.num
        if _num in ['1','2','3','4','5','6','7','8','9','10']:
            point += int(_num)
        elif _num in ['J','Q','K']:
            point += 10
        else:
            a_counter += 1
            point += 1
    for i in range(a_counter):
        if (point + 10) > 21:
            break
        else:
            point += 10

    return point

def print_game():
    print("{player1.name}'s Deck:\nPoints: {player1.point}\n")
    print(print_card(player1.card_list))

    print('\n')

    print("Dealer's Deck:\n")
    print(print_card(dealer.cards_to_print))
    #print(print_card(dealer.card_list))


#-=-=-=-=-=-=-=-=-=-
#    CLASSES
#-=-=-=-=-=-=-=-=-=-
class Card:
    SuitList = ['Spade','Heart','Diamond','Club']
    NumList = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']

    def __init__(self,num,suit):
        self.num = num
        self.suit = suit
        self.card_art = find_card_art(num,suit)

    def __str__(self):
        return self.num +  ' ' + self.suit

class Player:
    def __init__(self, name = 'Player 1', balance = 1500):
        self.name = name
        self.balance = balance
        self.card_list = []
        self.point = 0

    def add_card(self):
        self.card_list.append(get_rand_card())
        self.update_point()

    def update_point(self):
        self.point = count_point(self.card_list)

    def reset(self):
        self.card_list = []
        self.point = 0

class Dealer:
    def __init__(self):
        self.card_list = []
        self.cards_to_print = [FaceDownCard]
        self.point = 0

    def add_card(self):
        card_to_add = get_rand_card()
        self.card_list.append(card_to_add)
        self.cards_to_print.append(card_to_add)
        self.update_point()

    def set_up_game(self):
        self.card_list.append(get_rand_card())
        self.add_card()

    def update_point(self):
        self.point = count_point(self.card_list)

    def reset(self):
        self.card_list = []
        self.point = 0

# -=-=-=-=-=-=-=-=-=-
#    THE GAME
# -=-=-=-=-=-=-=-=-=-



#---- Game Beginning Setup -------

PlayedDeck = []
FaceDownCard: Card = Card('FaceDown','FaceDown')

print('-=-=-=-=-=-=-=-=-=-=-=-=-\n      BLACKJACK 1.0\n-=-=-=-=-=-=-=-=-=-=-=-=-\n\n')
name = input('Please enter your name ---> ')

print('┌' + '─'*(len(name)+11) + '┐' + '\n│ Welcome! '+ name + ' │\n└' + '─'*(len(name)+11) + '┘')
player1 = Player(name,1500)

#---- Loop through all the round ----
again = True
while again:

    while True:
        #---- Initial setup -------
        player1.reset()
        player1.add_card()
        player1.add_card()

        dealer = Dealer()
        dealer.reset()
        dealer.set_up_game()

        #---- Bidding Start -----
        print('\n')
        input('Press enter to start bidding!')

        print(f'\n----- BIDDING -----\nBalance: ${player1.balance}')

        #------ place bid and check for invalid input --------
        bid = input('Please place your bid ---> ')
        while True:
            try:
                bid = int(bid)
            except ValueError:
                bid = input('Input has to be an integer! Please try again ---> ')
            except:
                bid = input('Invalid Input! Please try again ---> ')
            else:
                if bid <= player1.balance:
                    break
                else:
                    bid = input(f'Insufficient balance! Your balance is {player1.balance}. Please try again ---> ')

        print(f'You bade ${bid}')
        player1.balance -= bid
        print('\n')


        #---- Game Start ------
        input('Press enter to start playing!')
        print('\n\n-=-=-=- GAME ON -=-=-=-\n\n')

        print_game()

        if check_blackjack(player1.card_list):
            print('\n\n* * * * * * * * * * * * * * * *\n* ┌─────────────────────────┐ *\n* │        YOU WIN!         │ *\n* │-=-=-=-=-=-=-=-=-=-=-=-=-│ *\n* │       BLACKJACK!        │ *\n* └─────────────────────────┘ *\n* * * * * * * * * * * * * * * *')
            player1.balance += bid * 2.5
            break

        if check_blackjack(dealer.card_list):
            print('\n' * 40)
            print(f"{player1.name}'s Deck:\nPoints: {player1.point}\n")
            print(print_card(player1.card_list))

            print('\n')

            print("Dealer's Deck:\n")
            print(f"Dealer's point: {dealer.point} points")
            print(print_card(dealer.card_list))

            print('\n\n┌───────────────────────────┐\n│         YOU LOST!         │\n│-=-=-=-=-=-=-=-=-=-=-=-=-=-│\n│The dealer has a BlackJack!│\n└───────────────────────────┘')
            break


        #---- Player's Turn ----
        stand = False
        while not stand and player1.point <= 21:
            HitOrStand = input('Choose an option number:   1 - Hit    2 - Stand\n---> ')
            while True:
                if HitOrStand == '1':
                    player1.add_card()
                    print('\n'*40)
                    print_game()
                    break
                elif HitOrStand == '2':
                    stand = True
                    break
                else:
                    HitOrStand = input('Invalid input! Try again (1 or 2) ---> ')
        if player1.point > 21:
            print('\n┌─────────────────────┐\n│      YOU LOST!      │\n│-=-=-=-=-=-=-=-=-=-=-│\n│       BUSTED        │\n└─────────────────────┘')
            break

        #---- Dealer's Turn
        while dealer.point <= 16:
            dealer.add_card()

        #--- Print game with dealer's cards faced up

        print('\n'*40)
        print(f"{player1.name}'s Deck:\nPoints: {player1.point}\n")
        print(print_card(player1.card_list))

        print('\n')

        print("Dealer's Deck:")
        print(f"Points: {dealer.point} points")
        print(print_card(dealer.card_list))

        if dealer.point >21:
            print('┌──────────────────────┐\n│       YOU WIN!       │\n│-=-=-=-=-=-=-=-=-=-=-=│\n│The dealer goes busted│\n└──────────────────────┘')
            player1.balance += bid * 2
            break
        else:
            if dealer.point > player1.point:
                print("┌─────────────────────┐\n│      YOU LOST!      │\n│-=-=-=-=-=-=-=-=-=-=-│\n│You have less points │\n└─────────────────────┘")
                break
            elif dealer.point < player1.point:
                print("┌─────────────────────┐\n│      YOU WIN!       │\n│-=-=-=-=-=-=-=-=-=-=-│\n│You have more points │\n└─────────────────────┘")
                player1.balance += bid*2
                break
            else:
                print('┌───────────────────────────┐\n│        GAME TIED!         │\n└───────────────────────────┘')
                player1.balance += bid
                break

    if player1.balance <= 0:
        print('\n\nYou ran out of money!')
        break

    replay = input('\n\nDo you want to play again? (Y/N) ---> ').upper()
    while True:
        if replay == 'Y':
            again = True
            break
        elif replay == 'N':
            again = False
            break
        else:
            replay = input('Invalid input! Do you want to play again? (Y/N) ---> ').upper()

print('\n\nGame ended')
input('Press enter to exit program!')

