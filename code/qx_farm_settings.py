# game setup
WIDTH    = 1200
HEIGTH   = 800
FPS      = 60
TILESIZE = 64
HITBOX_OFFSET = {
    "player": -26,
    "object": -40,
    "grass": -10,
    "invisible":0
}

#ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = "graphics_qx/font/joystix.ttf"
UI_FONT_SIZE = 18

#general colour
WATER_COLOUR = "#71ddee"
UI_BG_COLOUR = "#222222"
UI_BORDER_COLOUR = "#111111"
TEXT_COLOUR = "#EEEEEE"

#ui colours 
HEALTH_COLOUR = "red"
UI_BORDER_COLOUR_ACTIVE = "gold"

#weapons
weapons_data = {    
    "Shadow Saber" : {"cooldown" : 1500, "damage" : 30, "graphic" : "graphics_qx/weapons_farming/Shadow_Saber/full.png"},
    "Thunder Axe" : {"cooldown" : 300, "damage" : 20, "graphic" : "graphics_qx/weapons_farming/Thunder_Axe/full.png"},
    "Lion Sword" : {"cooldown" : 50, "damage" : 8, "graphic" : "graphics_qx/weapons_farming/Lion_Sword/full.png"}
}

#magic
magic_data = {
    "Essence of Renewal" : {"strength": 20, "cost": 10, "graphic": "graphics_qx/special_effects_farming/heal/heal.png"}
}

#enemy
monster_data = {
    "squid":{'health':100,"exp":100,"damage":10,"attack_type":"slash","attack_sound":"audio_qx/attack/slash.wav","speed":3,"resistance":3,"attack_radius":80,"notice_radius":360},
    "raccoon":{'health':300,"exp":250,"damage":40,"attack_type":"slash","attack_sound":"audio_qx/attack/claw.wav","speed":2,"resistance":3,"attack_radius":120,"notice_radius":400},
    "spirit":{'health':100,"exp":110,"damage":8,"attack_type":"slash","attack_sound":"audio_qx/attack/fireball.wav","speed":4,"resistance":3,"attack_radius":60,"notice_radius":350},
    "bamboo":{'health':70,"exp":120,"damage":6,"attack_type":"slash","attack_sound":"audio_qx/attack/slash.wav","speed":3,"resistance":3,"attack_radius":50,"notice_radius":300}
}