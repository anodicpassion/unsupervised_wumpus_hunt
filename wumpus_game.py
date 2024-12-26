import random
import os


class WumpusGame:
    def __init__(self):
        self.cave = self.generate_cave()
        self.wumpus_location = random.randint(0, 19)
        self.player_location = random.randint(0, 19)
        self.bats_locations = random.sample(range(20), 2)
        self.pits_locations = random.sample(range(20), 2)
        while self.wumpus_location == self.player_location:
            self.wumpus_location = random.randint(0, 19)
        self.arrows = 5

    def generate_cave(self):
        cave = []
        for i in range(20):
            cave.append([i - 1 if i - 1 >= 0 else 19, (i + 1) % 20])
        return cave

    def move_player(self, room):
        if room in self.cave[self.player_location]:
            self.player_location = room
            self.check_current_room_and_print()
        else:
            print("You can't move to that room!")

    def shoot_arrow(self, room):
        if self.arrows > 0:
            self.arrows -= 1
            if room == self.wumpus_location:
                print("You hit the Wumpus! You win!")
                return True
            else:
                print("You missed!")
                self.wumpus_location = random.choice(self.cave[self.wumpus_location])
        else:
            print("You're out of arrows!")
        return False

    def check_current_room_and_print(self):
        if self.player_location == self.wumpus_location:
            print("You've been eaten by the Wumpus! Game over.")
            return True
        elif self.player_location in self.pits_locations:
            print("You fell into a pit! Game over.")
            return True
        elif self.player_location in self.bats_locations:
            print("Bats carried you to another room!")
            self.player_location = random.randint(0, 19)
            self.check_current_room_and_print()
        else:
            print("You are in room", self.player_location)
            if self.wumpus_location in self.cave[self.player_location]:
                print("You smell something terrible nearby.")
            if any(pit in self.cave[self.player_location] for pit in self.pits_locations):
                print("You feel a cold wind blowing from a nearby room.")
            if any(bat in self.cave[self.player_location] for bat in self.bats_locations):
                print("You hear rustling of bat wings.")
        return False

    def check_current_room(self):
        if self.player_location == self.wumpus_location:
            return True
        elif self.player_location in self.pits_locations:
            return True

        return False

    def play(self):
        os.system('clear')
        print("Welcome to Hunt the Wumpus!\n")
        print("You are in room", self.player_location)
        game_over = False
        while not game_over:
            print("Tunnels lead to", self.cave[self.player_location])
            action = input("Do you want to (m)ove or (s)hoot? ")
            if action == 'm':
                room = int(input("Enter the room number you want to move to: "))
                os.system('clear')
                self.move_player(room)
            elif action == 's':
                room = int(input("Enter the room number you want to shoot into: "))
                os.system('clear')
                game_over = self.shoot_arrow(room)
            game_over = game_over or self.check_current_room()


if __name__ == "__main__":
    game = WumpusGame()
    game.play()
    # print(game.generate_cave())
