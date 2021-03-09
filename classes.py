from random import randint
from random import choice
from random import shuffle
from enum import Enum
from time import sleep

# Waits 2 seconds to display the steps of the game when necessary
def wait2Seconds(func):
    def wrapper(value):
        sleep(2)
        return func(value)
    return wrapper

class Card:
# ----- Class that represents a single card ------
# Character: name of the card
# Image: Cover image of the card
# Characteristics: {} for skills and values of each card
# faceDown: position of the card

    # Characteristicas by default
    generalChars = ['[1] Strengh','[2] Fly','[3] Water','[4] Fire']
    generalCharacters = ['Black Panther','Black Widow', 'Captain America',
                        'The Collector','Corvus Glaive', 'Doctor Erik Selvig',
                        'Doctor Strange','Drax','Falcon','Groot','Hawkeye','Hulk',
                        'Loki','Mantis','Nebula']

    def __init__(self, character, image, characteristics):    
        self.character = character
        self.image = image
        self.characteristics = characteristics
        self.faceDown = True

    # Get the value from the chosen characteristic 
    def getStrength(self, characteristic):
        characteristic = Card.generalChars[characteristic]
        return self.characteristics[characteristic]
    
    def __str__(self):
        return f'{self.character} - {self.image} - {self.characteristics} - {self.faceDown}'

class Deck:
# ------ Class that represents the full deck of cards -------
# Class vairables:
# valuesSkill = int[] to avoid duplicates in characteristics
# MAX_NO_CARDS = max number of cards in the game
# MIN_NO_CARDS = min number of cards in the game
# Instance variables:
# noCards: number of cards
# cards: cards
# _cards: cards generator to yield each card
# emptyDeck: indicator to know whether the deck is empty

    valuesSkills = None
    MAX_NO_CARDS = len(Card.generalCharacters)
    MIN_NO_CARDS = 10

    def setValuesRange():
        _total_no_cards = Deck.MIN_NO_CARDS * len(Card.generalChars) * 2 
        _max_limit = int(_total_no_cards / 2)
        _min_limit = _max_limit * -1
        Deck.valuesSkills = list(range(_min_limit, _max_limit+1))


    def __init__(self, noCards=0):
        self.noCards = noCards
        self.cards = []
        self._cards = None
        self.emptyDeck = False
    
    # Iterate over the deck, remove the top at the top of the deck and yield that value
    def _initilizeDeck(self):
        for i in range(len(self.cards)-1,-1,-1):
            self.cards[i].faceDown = False
            _card = self.cards.pop()
            self.noCards = len(self.cards)
            yield _card

    @wait2Seconds
    # Suffle cards 
    def suffleDeck(self):
        print('Suffling cards...')
        shuffle(self.cards)
        self._cards = self._initilizeDeck()
    
    # Show cards in the deck
    def showDeck(self):
        print('(Top)')
        for i in range(len(self.cards)-1,-1,-1):
            print(f'{i+1} - {self.cards[i]}')
        print('(Bottom)')

    # Pick up next card on top of deck
    def nextCard(self):
        try:
            return next(self._cards)
        except StopIteration:
            self.emptyDeck = True
            print('No more cards :(')
            return None

    # Get specific card from the deck based on its position
    def getSpecificCard(self,noCard, faceDown=False):
        #print(f'Card to be removed: {noCard} - from this deck {len(self.cards)}')
        self.cards[noCard].faceDown = faceDown
        _card = self.cards.pop(noCard)
        self.noCards = len(self.cards)
        self._cards = self._initilizeDeck()
        return _card

    # Add cards to outdated Deck and suffle them if required
    def addCard(self, card, suffle=True):
        self.cards.append(card)
        self.noCards = len(self.cards)
        if(suffle):
            shuffle(self.cards)
        self._cards = self._initilizeDeck()

    # Get the current number of cards in the deck
    def getNoCards(self):
        return self.noCards

    # Load characteristics in cards
    @wait2Seconds
    def loadCards(self):
        print('Generating cards...')
        characters = self._loadCharacters()
        for i in range(self.noCards):
            self.cards.append(Card(characters[i], '', self._loadCharacteristics()))
        # initialize generator
        #self._cards = self._initilizeDeck()

    # Internal method to load the character for all the cards
    def _loadCharacters(self):
        return Card.generalCharacters

    # Internal method to load the characteristics for each card in the deck
    def _loadCharacteristics(self):
        _chars = []
        for c in Card.generalChars:
            number = choice(Deck.valuesSkills)
            Deck.valuesSkills.remove(number)
            _chars.append(number)
        return dict(zip(Card.generalChars,_chars))
        


class Player:
# ------- Class that represents a single player----------
# name: name of the card
# noOpponent: position of the opponent (0|1) based on the order of the game
# noPlayer: position of the current player (0|1) based on the order of the game
# deck: Cover image of the card
# points: Cover image of the card
# isResurrectSpell: Cover image of the card
# isGoodSpell: Cover image of the card
# computer: simulate a game by the computer

    def __init__(self, name='', deck=None, points=0, computer=False):
        self.name = name
        self.noOpponent = 0
        self.noPlayer = 0
        self.deck = deck
        self.points = points
        self.isResurrectSpell = True
        self.isGoodSpell = True
        self.computer = computer
    
    # Pick card or challenge respond
    def pickCard(self):
        print(f'<< {self.name} >> picking up card...')
        return self.deck.nextCard()
        
    # Set position of the current player
    def setNoPlayer(self,noPlayer):
        self.noPlayer = noPlayer

    # Get the posision of the current player
    def getNoPlayer(self):
        return self.noPlayer

    # Set the position of the opponent
    def setOpponentPlayer(self, noOpponent):
        self.noOpponent = noOpponent

    # Get the position of the opponent as a player
    def getOpponentPlayer(self):
        return self.noOpponent

    # Adds 1 point afther defeating the opponent
    def addPoints(self):
        self.points += 1
        print('+-----------------------------------------')
        print(f'<< {self.name} >> wins and gets 1 point!')
        print('+-----------------------------------------')
    
    # Get the current points of the player
    def getPoints(self):
        print(f'{self.name} gets {self.points}')

    def __str__(self):
        return f'{self.name}'
    
    # Shows the cards in the deck after 2 seconds
    @wait2Seconds
    def showDeck(self):
        print(f'+------------------------Deck {self.name}:----------------+')
        self.deck.showDeck()
    
    # Flag to indicate the use of the God Spell
    def useGodSpell(self):
        self.isGoodSpell = False
    
    # Flag to determine whether the God Spell has been used
    def hasGodSpell(self):
        return self.isGoodSpell
    
    # Flag to indicate the use of the Resurrect Spell
    def useResurrectSpell(self):
        self.isResurrectSpell = False
    
    # Flag to determine whether the Resurrect Spell has been used
    def hasResurrectSpell(self):
        return self.isResurrectSpell
    
    # Get a specific card from the deck based on its position
    def getSpecificCard(self, noCard):
        print(f'---------------------------')
        print(f'Card chosen: {noCard+1}')
        print(f'---------------------------')
        return self.deck.getSpecificCard(noCard)
    
    # Flag to determine whether the palyer is the machine
    def isComputer(self):
        return self.computer
    
    # Suggested approach to apply the Resurrect Spell as the machine
    def likelyResurrectSpell(self):
        if(self.deck.getNoCards() >= 2):
            return False
        return True
    
    # Suggested approach to apply the God Spell as the machine
    def likelyGodSpell(self):
        if(self.deck.getNoCards() >= 3 ):
            return False
        return True

class Game:
# -------- Class that represents a game --------
# players: array of players in the game [Player 1|Player 2] (used for the opponent of the player)
# outdatedDeck: deck for the discarded cards after each challenge
# statusGame: Flag to keep playing the game
# currentPlayer: player that begins each round

    def __init__(self, players=None, outdatedDeck=None):
        self.players = players
        self.outdatedDeck = Deck()
        self.statusGame = True
        self.currentPlayer = None
        self.debug = False

    # Required steps to play
    def startGame(self):
        self.choosePlayer()
        self.setTurns()
        self.isGameOver()

    # Enable debug to look at the cards on the deck
    def enableDebug(self,debug):
        self.debug = debug

    # Show the cards in the outdated deck
    def showOutdatedDeck(self):
        self.outdatedDeck.showDeck()

    # Get random card from the outdated deck when playing the Resurrect spell
    def getRandomCard(self):
        card = None
        _noCards = self.outdatedDeck.getNoCards()
        print(f'Getting random card from Outdated deck {_noCards}')
        # Validate that there is at least one card to choose
        if  _noCards > 0 :
            _card = randint(0,_noCards-1)
            #print(f'Random card chosen: {_card}')
            print(f'Adding card to the top of the deck')
            card = self.outdatedDeck.getSpecificCard(_card, True)
            if(self.debug):
                print(f'---------------------------')
                print(f'Added card: {card}')
                print(f'---------------------------')
        else:
            print('No available cards')
        return card

    # Simulate a dice to choose the first player to play
    @wait2Seconds
    def choosePlayer(self):
        #print('Please, select the option of the game: 1- Player vs Player | 2- Player vs Computer')
        try:
            res = int(input('Please, select the option of the game: [1] Player vs Player - [2] Player vs Computer '))
            if(res < 1 or res > 2):
                res = randint(1,2)
                print(f'Option not valid. Randomly choosing one: {res}')
                
        except ValueError:
            res = randint(1,2)
            print(f'Option not valid. Randomly choosing one: {res}')           

        noCards = Deck.MIN_NO_CARDS
        Deck.setValuesRange()
        player1 = Player(name='Player1', deck=Deck(noCards))
        player2 = (Player(name='Player2', deck=Deck(noCards)) if res == 1 else Player(name='PlayerC', deck=Deck(noCards), computer=True))
        # loading cards
        print('Starting deck...')
        player1.deck.loadCards()
        player2.deck.loadCards()
        player1.deck.suffleDeck()
        player2.deck.suffleDeck()
        # For validation purposes
        if(self.debug):
            player1.showDeck()
            player2.showDeck()
        self.players = [player1, player2]
    
    # Determine the order of the players during the first round to start the game
    @wait2Seconds
    def setTurns(self):
        print('================== Setting turns =================')
        print('Rolling dice to see who goes first...')
        firstDice, secondDice = randint(1,6), randint(1,6)
        # Additional validation in case they get same numbers with the dice
        while (firstDice == secondDice):
            print('Oops. Same numbers. Rolling dice once again...')
            firstDice, secondDice = randint(1,6), randint(1,6)
        # Establish the order
        if(firstDice > secondDice):
            print(f'<< {self.players[0].name} >> goes first: {firstDice}:{secondDice}')
            self.setCurrentPlayer(self.players[0])
            self.currentPlayer.setNoPlayer(0)
            self.currentPlayer.setOpponentPlayer(1)
            self.players[1].setNoPlayer(1)
            self.players[1].setOpponentPlayer(0)
        else:
            print(f'<< {self.players[1].name} >> goes first: {firstDice}:{secondDice}')
            self.setCurrentPlayer(self.players[1])
            self.currentPlayer.setNoPlayer(1)
            self.currentPlayer.setOpponentPlayer(0)   
            self.players[0].setNoPlayer(0)
            self.players[0].setOpponentPlayer(1)

    # Typical steps in one turn
    @wait2Seconds
    def oneTurn(self):
        print('+-------------------------+')
        print('+------ Starting turn -----+')
        # Validate if the current player has not used the Resurrect Spell
        if(self.currentPlayer.hasResurrectSpell()):
            # Validate whether the player is a computer or not
            if(not self.currentPlayer.isComputer()):
                try:
                    option = int(input(f'<< {self.currentPlayer.name} >>, Would you like to play the Resurrect spell? [1] Yes - [2] No : '))
                    if(option < 1 or option > 2):
                        option = randint(1,2)
                        print(f'Option not valid. Randomly choosing one: {option}')
                        
                except ValueError:
                    option = 1 if self.currentPlayer.likelyResurrectSpell() else 2
                    print(f'Option not valid. Randomly choosing one: {option}')
            else:
                option = 1 if self.currentPlayer.likelyResurrectSpell() else 2
                print(f'<< {self.currentPlayer.name} >>, Would you like to play the Resurrect spell? [1] Yes - [2] No : {option}')
                sleep(1)
            # Validate answer
            if(option == 1):
                self.resurrectSpell(self.currentPlayer)
                if(self.debug):
                    self.currentPlayer.showDeck()
        # Picking up card at the top 
        card1 = self.currentPlayer.pickCard()
        if card1 is not None:
            print(f'---------------------------')
            print(f'Showing card current player: [{card1}]')
            print(f'---------------------------')
            if(not self.currentPlayer.isComputer()):
                try:
                    characteristic = int(input('Which skill would you like to choose? [1,2,3,4]: '))-1
                    if(characteristic < 0 or characteristic > 3):
                        characteristic = randint(0,3)
                        print(f'Option not valid. Randomly choosing one: {characteristic+1}')
                        
                except ValueError:
                    characteristic = randint(0,3)
                    print(f'Option not valid. Randomly choosing one: {characteristic+1}')
                    
            else:
                characteristic = randint(0,3)
                print(f'Which skill would you like to choose? [1,2,3,4]: {characteristic+1}')
            
            sleep(1)
            if(self.currentPlayer.hasGodSpell()):
                if(not self.currentPlayer.isComputer()):
                    try:
                        option = int(input(f'What would you like to do? [1] Challenge player - [2] Play God spell: '))
                        if(option < 1 or option > 2):
                            option = randint(1,2)
                            print(f'Option not valid. Randomly choosing one: {option}')
                            
                    except ValueError:
                        option = randint(1,2)
                        print(f'Option not valid. Randomly choosing one: {option}')
                        
                else:
                    option = 2 if self.currentPlayer.likelyGodSpell() else 1
                    print(f'What would you like to do? [1] Challenge player - [2] Play God spell: {option}')
                
                sleep(1)
                if option == 2:
                    self.goodSpell(self.currentPlayer, characteristic, card1)
                else:
                    print('Challenging opponent!')
                    self.challenge(self.currentPlayer, characteristic, card1)    
                sleep(1)
            else:
                print('Challenging opponent')
                self.challenge(self.currentPlayer, characteristic, card1)
            print(' +-------- End of turn ---------')
            if(self.debug):
                self.players[0].showDeck()
                self.players[1].showDeck()
            else:
                print(f'Deck1: [{self.players[0].deck.getNoCards()}]')
                print(f'Deck2: [{self.players[1].deck.getNoCards()}]')
            self.score()
        else: # No more cards. Game over
            self.statusGame = False

    def isGameOver(self):
        # Pick cards and start each round if there are any cards
        while self.statusGame:
            self.oneTurn()
        print('Game over!')
        #self.score()
    
    # Indicate the playere to begins the round
    def setCurrentPlayer(self, player):
        self.currentPlayer = player

    # Show the points of the game for each player
    def score(self):
        print('+-------Score-------+')
        for p in self.players:
            p.getPoints()
        print('+-------------------+')

    # Use God Spell
    def goodSpell(self, player, characteristic, card1):
        _opponent = self.players[player.getOpponentPlayer()]
        if(_opponent.hasResurrectSpell()):
            if(not _opponent.isComputer()):
                try:
                    option = int(input(f'<< {_opponent.name} >>, Would you like to use Resurrect Spell? [1] Yes | [2] No: '))
                    if(option < 1 or option > 2):
                        option = randint(1,2)
                        print(f'Option not valid. Randomly choosing one: {option}')
                        
                except ValueError:
                    option = randint(1,2)
                    print(f'Option not valid. Randomly choosing one: {option}')
                
            else:
                option = 1 if _opponent.likelyResurrectSpell() else 2
                print(f'<< {_opponent.name} >>, Would you like to use Resurrect Spell? [1] Yes | [2] No: {option}')
                sleep(1)
            if(option == 1):
                self.resurrectSpell(_opponent)
        
        if(player.hasGodSpell()):
            print('+ ---------- God Spell -----------')
            print('Showing opponent cards:')
            _opponent.showDeck()
            _max = 1 if _opponent.deck.getNoCards() == 1 else _opponent.deck.getNoCards()-1
            if(not player.isComputer()):
                try:
                    option = int(input('Which card would you like to choose? '))
                    if(option < 1 or option > _max):
                        option = randint(0,_max)
                        print(f'Option not valid. Randomly choosing one: {option+1}')
                    else:
                        option -= 1
                        
                except ValueError:
                    option = randint(0,_max)
                    print(f'Option not valid. Randomly choosing one: {option+1}')
                    
            else:
                option = randint(0,_max)
                print(f'Which card would you like to choose? {option+1}')
            
            sleep(1)
            # Choose any card
            card2 = _opponent.getSpecificCard(option)
            self._challenge(player, characteristic, card1, card2)
            player.useGodSpell()
        else:
            print('You can only challenge the other player')
            self.challenge(player, characteristic, card1)
    
    # Use Resurrect Spell
    def resurrectSpell(self, _player):
        # Validate whether the player has not used Resurrect spell and 
        # if there are enough cards in the ourdated Deck
        print(_player.name)
        if self.outdatedDeck.getNoCards() == 0:
            print('There are no cards to choose yet. Maybe next turn')
            return
        if(_player.hasResurrectSpell()):
            print('+ ---------- Resurrect Spell -----------')
            print('Adding one card on top of your deck')
            _player.deck.addCard(self.getRandomCard(),False)
            _player.useResurrectSpell()
            sleep(1)
        else:
            print('You cannot play Resurrect spell anymore')
        
    
    
    # Challenge the opponent with a single card
    def challenge(self, player, characteristic, card1):
        #print(f'Current Player: << {player.name} >>')
        print(f'Opponent: {player.getOpponentPlayer()}' )
        _opponent = self.players[player.getOpponentPlayer()]
        card2 = _opponent.pickCard()
        self._challenge(player, characteristic, card1, card2)
    
    # Internal evaluation of the challenged cards
    def _challenge(self, player, characteristic, card1, card2):
        _opponent = self.players[player.getOpponentPlayer()]
        if card2 is not None:
            print(f'---------------------------')
            print(f'Showing card opponent: [{card2}]')
            print(f'---------------------------')
            # Update points & set turn
            self.outdatedDeck.addCard(card1)
            self.outdatedDeck.addCard(card2)
            card1 = card1.getStrength(characteristic)
            card2 = card2.getStrength(characteristic)
            # Evaluate result
            if (card1 > card2):
                player.addPoints()
                self.setCurrentPlayer(player)
            else:
                _opponent.addPoints()
                self.setCurrentPlayer(_opponent)
            sleep(2)
            # else:
            #     print('Same values!!')
        else: # Game over in case there are no more cards
            self.statusGame = False