import classes as cl
from random import randint
from random import choice
from time import sleep

def testCards():
    noCards = cl.Deck.MIN_NO_CARDS
    player1 = cl.Player(name='Player1', deck=Deck(noCards))
    player2 = cl.Player(name='PlayerC', deck=Deck(noCards), computer=True)

# Simulate choosing a characteristic
def testCard():
    _chars = [randint(-10,10) for c in cl.Card.generalChars]
    card1 = cl.Card('char1','',dict(zip(cl.Card.generalChars,_chars)))
    print(card1)
    for i in range(15):
        characteristic = randint(0,3)
        print(f'Which skill would you like to choose? [1,2,3,4]: {characteristic+1}')
        card1.getStrength(characteristic)


# Simulate choosing a characteristic
def testCardsPoints():

    _chars = [randint(-10,10) for c in cl.Card.generalChars]
    card1 = cl.Card('char1','',dict(zip(cl.Card.generalChars,_chars)))
    _chars = [randint(-10,10) for c in cl.Card.generalChars]
    card2 = cl.Card('char2','',dict(zip(cl.Card.generalChars,_chars)))
    print(card1)
    print(card2)
    
def testLoadCards():
    cl.Deck.setValuesRange()
    print(cl.Deck.valuesSkills)    
    deck = cl.Deck(cl.Deck.MIN_NO_CARDS)
    deck.loadCards()
    deck.suffleDeck()
    deck.showDeck()
    print(cl.Deck.valuesSkills)    
    deck2 = cl.Deck(cl.Deck.MIN_NO_CARDS)
    deck2.loadCards()
    deck2.suffleDeck()
    deck2.showDeck()
    print(cl.Deck.valuesSkills)
                





#testCardsPoints()
testLoadCards()
#testCard()
