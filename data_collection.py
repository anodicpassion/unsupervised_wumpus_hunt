import random
import pandas as pd


class WumpusGameDataCollector:
    def __init__(self):
        self.cave = self.generate_cave()
        self.wumpus_location = random.randint(0, 19)
        self.player_location = random.randint(0, 19)
        self.bats_locations = random.sample(range(20), 2)
        self.pits_locations = random.sample(range(20), 2)
        while self.wumpus_location == self.player_location:
            self.wumpus_location = random.randint(0, 19)
        self.arrows = 5
        self.data = []

    def generate_cave(self):
        cave = []
        for i in range(20):
            cave.append([i-1 if i-1 >= 0 else 19, (i+1) % 20])
        return cave

    def move_player(self, room):
        if room in self.cave[self.player_location]:
            self.player_location = room
            self.collect_data()

    def shoot_arrow(self, room):
        if self.arrows > 0:
            self.arrows -= 1

    def collect_data(self):
        state = {
            'player_location': self.player_location,
            'wumpus_nearby': 1 if self.wumpus_location in self.cave[self.player_location] else 0,
            'bats_nearby': 1 if any(bat in self.cave[self.player_location] for bat in self.bats_locations) else 0,
            'pits_nearby': 1 if any(pit in self.cave[self.player_location] for pit in self.pits_locations) else 0,
            'arrows_left': self.arrows
        }
        self.data.append(state)

    def play(self):
        print("Collecting data from the game...")
        for _ in range(100):  # Collect data from 100 moves
            action = random.choice(['m', 's'])
            if action == 'm':
                room = random.choice(self.cave[self.player_location])
                self.move_player(room)
            elif action == 's':
                room = random.choice(self.cave[self.player_location])
                self.shoot_arrow(room)

        return pd.DataFrame(self.data)


if __name__ == "__main__":
    game = WumpusGameDataCollector()
    df = game.play()
    df.to_csv('wumpus_game_data.csv', index=False)
    print("Data collection complete. Data saved to wumpus_game_data.csv.")
