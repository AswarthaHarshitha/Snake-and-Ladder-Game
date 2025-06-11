from snake_ladder_gui import SnakeLadderGUI

def main():
    print("Starting Snake and Ladder Game GUI...")
    print("Instructions:")
    print("1. Press SPACE to roll the dice")
    print("2. The blue circle represents your position")
    print("3. Red lines are snakes (going down)")
    print("4. Green lines are ladders (going up)")
    print("5. Reach position 100 to win!")
    print("\nPress SPACE to start playing...")
    
    game = SnakeLadderGUI()
    game.run()

if __name__ == "__main__":
    main() 