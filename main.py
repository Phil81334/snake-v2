# /*===================================
#     Stock Imports
# ====================================*/

# ...

# /*===================================
#     Main
# ====================================*/

from core.game import Game

def main():
    game = Game(title="Snake Game")
    game.run()

if __name__ == "__main__":
    main()