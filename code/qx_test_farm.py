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
        total_coins = data["game1"]["Best Coins"] + data["game2"]["Best Coins"]
    except (FileNotFoundError, KeyError):
        print("Using default coin value.")
        total_coins = 700
    
    class Game:
        def __init__(self):

            #general setup
            pygame.init()
            self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
            pygame.display.set_caption("Farming Map")
            self.clock = pygame.time.Clock()

            self.level = Level(player_coins=total_coins)

        def run(self):
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

                self.screen.fill("#71ddee")
                self.level.run()
                pygame.display.update()
                self.clock.tick(FPS)

    game = Game()
    game.run()