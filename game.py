import classes as cl


try:
    game = cl.Game()
    # In case you want show the cards for debugging
    #game.enableDebug(True)
    game.startGame()
except KeyboardInterrupt:
    print('Game Over')