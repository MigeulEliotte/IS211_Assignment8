import random
import time

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn_total = 0
        self.roll_count = 0
        self.sixes_count = 0

    def roll_die(self, die):
        roll = die.roll()
        self.roll_count += 1

        if roll == 1:
            print(f"{self.name} rolled a 1! No points this turn.")
            self.turn_total = 0
            self.sixes_count = 0
        elif roll == 6:
            self.turn_total += roll
            self.sixes_count += 1
            print(f"{self.name} rolled a {roll}. Turn total: {self.turn_total}")
            if self.sixes_count == 6:
                print(f"{self.name} rolled six sixes in a row! {self.name} wins!")
                return True
        else:
            self.turn_total += roll
            self.sixes_count = 0
            print(f"{self.name} rolled a {roll}. Turn total: {self.turn_total}")

        return False

    def hold(self):
        self.score += self.turn_total
        print(f"{self.name} holds. Total score: {self.score}")
        self.turn_total = 0

    def reset_turn(self):
        self.turn_total = 0

class Die:
    def __init__(self, sides=6):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)

class Game:
    def __init__(self):
        self.players = [Player("Player 1"), Player("Player 2")]
        self.die = Die()
        self.current_player = 0
        self.total_rolls = 0

    def play(self):
        while True:
            player = self.players[self.current_player]
            player.reset_turn()
            print(f"{player.name}'s turn:")
            while True:
                if self.total_rolls % 100 == 0 and self.total_rolls > 0:
                    d20_roll = random.randint(1, 20)
                    print(f"Bonus roll! You rolled a d20: {d20_roll}")

                choice = input("Roll (r) or Hold (h)? ")
                if choice == 'r':
                    if player.roll_die(self.die):
                        return
                    self.total_rolls += 1
                    if player.turn_total == 0:
                        break
                elif choice == 'h':
                    player.hold()
                    break
            if player.score >= 100:
                print(f"{player.name} wins!")
                break
            self.switch_turn()

    def switch_turn(self):
        self.current_player = (self.current_player + 1) % len(self.players)

class TimedGameProxy:
    def __init__(self, game, time_limit=60):
        self.game = game
        self.time_limit = time_limit

    def play(self):
        start_time = time.time()
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time >= self.time_limit:
                print("Time is up! Determining the winner based on current scores...")
                self.determine_winner()
                break
            self.game.play()
            if any(player.score >= 100 for player in self.game.players):
                break

    def determine_winner(self):
        player1, player2 = self.game.players
        if player1.score > player2.score:
            print(f"{player1.name} wins with {player1.score} points!")
        elif player2.score > player1.score:
            print(f"{player2.name} wins with {player2.score} points!")
        else:
            print("It's a tie!")

# Main program
if __name__ == "__main__":
    random.seed(0)
    game = Game()
    timed_game = TimedGameProxy(game)
    timed_game.play()
