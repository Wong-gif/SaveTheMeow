import sys
import time

class WeaponEffects:
    active_effects = {} # Tracks how many left

    @staticmethod
    def apply(name, mario, boss):
        effects = {
            "Lion Sword": WeaponEffects.lion_sword,
            "Hawk's Eye": WeaponEffects.hawks_eye,
            "Luna Bow": WeaponEffects.luna_bow,
            "Phoenix Feather": WeaponEffects.phoenix_feather,
            "Hydro Strike": WeaponEffects.hydro_strike,
            "Libra of Eternity": WeaponEffects.libra_eternity,
            "Aegis Shield": WeaponEffects.aegis_shield,
            "Thunder Axe": WeaponEffects.thunder_axe,
            "Essence of Renewal": WeaponEffects.essence_renewal
        }
        if name in effects:
            effects[name](mario, boss)
        else:
            print(f"No effect function for: {name}")

    @staticmethod
    def lion_sword(mario, boss):
        effect_name = "lion_sword"
        if effect_name not in WeaponEffects.active_effects:
            WeaponEffects.active_effects[effect_name] = {"uses_left": 5}

        effect = WeaponEffects.active_effects[effect_name]
        if effect["uses_left"] > 0:
            boss.health -= 2000
            effect["uses_left"] -= 1
            print(f"Lion Sword used! Boss -150 HP. Uses left: {effect['uses_left']}")
        else:
            print("Lion Sword expired. No more uses left.")

    @staticmethod
    def hawks_eye(mario, boss):
        boss.health -= 130
        print("Hawk's Eye used!")

    @staticmethod
    def luna_bow(mario, boss):
        boss.health -= 150
        print("Luna Bow used!")

    @staticmethod
    def phoenix_feather(mario, boss):
        boss.health -= 150
        print("Phoenix Feather used.")

    @staticmethod
    def hydro_strike(mario, boss):
        boss.health -= 200
        print("Hydro strike used.")

    @staticmethod
    def libra_eternity(mario, boss):
        effect_name = "lion_sword"
        if effect_name not in WeaponEffects.active_effects:
            WeaponEffects.active_effects[effect_name] = {"uses_left": 3}

        effect = WeaponEffects.active_effects[effect_name]
        if effect["uses_left"] > 0:
            mario.health -= 0
            effect["uses_left"] -= 1
            print(f"Lion Sword used! Boss -150 HP. Uses left: {effect['uses_left']}")
        else:
            print("Lion Sword expired. No more uses left.")

    @staticmethod
    def aegis_shield(mario, boss):
        boss.health -= 130
        print("Hawk's eye used.")

    @staticmethod
    def thunder_axe(mario, boss):
        boss.health -= 130
        print("Hawk's eye used.")

    @staticmethod
    def essence_renewal(mario, boss):
        effect_name = "essence_renewal"
        if effect_name not in WeaponEffects.active_effects:
            WeaponEffects.active_effects[effect_name] = {"uses_left": 2}

        effect = WeaponEffects.active_effects[effect_name]
        if effect["uses_left"] > 0:
            mario.health += 40
            effect["uses_left"] -= 1
            print(f"Essence of Renewal used! Mario +30 HP. Uses left: {effect['uses_left']}")
        else:
            print("Essence of Renewal expired. No more uses left.")

    


