def farming_map(username):
    import pygame, sys
    import json
    from qx_farm_level import Level

    # game setup
    WIDTH    = 1200
    HEIGTH   = 800
    FPS      = 60

    filename = f"{username}.txt"
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        if "inventory" not in data:
            data["inventory"] = {"Weapon for Boss": [], "Weapon for Farm": []}
        if "game3" not in data:  # Initialize game3 if missing
            data["game3"] = {"Coins": 0, "Diamonds": 0}
        total_coins = data["game1"]["Best Coins"] + data["game2"]["Best Coins"] + data["game3"]["Coins"]
        total_diamonds = data["game1"]["Best Diamonds"] + data["game2"]["Best Diamonds"] + data["game3"]["Diamonds"]
        available_weapons = data.get("inventory", {}).get("Weapon for Farm", [])
        available_magic = data.get("inventory", {}).get("Magic for Farm", [])

    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        print("Using default coin and weapon values.")
        total_coins = 700
        total_diamonds = 500
        available_weapons = []
        available_magic = []
    
    class Game:
        def __init__(self):

            #general setup
            pygame.init()
            self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
            pygame.display.set_caption("Farming Map")
            self.clock = pygame.time.Clock()

            self.level = Level(player_coins=total_coins,player_diamonds=total_diamonds,available_weapons=available_weapons,available_magic=available_magic,username=username)

        def run(self):
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    
                    if self.level.player.health <= 0:
                        return

                self.screen.fill("#71ddee")
                self.level.run()
                pygame.display.update()
                self.clock.tick(FPS)

    game = Game()
    game.run()