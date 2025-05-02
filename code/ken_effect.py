import pygame

class WeaponEffects:
    @staticmethod
    def lion_sword():
        return {
            "name": "Lion Sword",
            "type": "attack",
            "attack_bonus": 150,
            "description": "Each swing of the sword has 100 points of attack. Only 5 chances."
        }

    @staticmethod
    def hawks_eye():
        return {
            "name": "Hawk's Eye",
            "type": "attack",
            "attack_bonus": 130,
            "description": "Each arrow has 130 damage. Only for 10 seconds."
        }

    @staticmethod
    def luna_bow():
        return {
            "name": "Luna Bow",
            "type": "attack",
            "attack_bonus": 150,
            "description": "Each arrow has 150 damage. Only for 10 seconds."
        }

    @staticmethod
    def phoenix_feather():
        return {
            "name": "Phoenix Feather",
            "type": "attack",
            "attack_bonus": 120,
            "description": "Each arrow has 150 damage. Only for 10 seconds."
        }

    @staticmethod
    def hydro_strike():
        return {
            "name": "Hydro Strike",
            "type": "attack",
            "splash_damage": 200,
            "description": "Each bullet has 200 points of attack. Only for 10 seconds."
        }

    @staticmethod
    def libra_of_eternity():
        return {
            "name": "Libra of Eternity",
            "type": "defense",
            "defense_bonus": 100,
            "description": "The shield can block 3 attacks."
        }

    @staticmethod
    def aegis_shield():
        return {
            "name": "Aegis Shield",
            "type": "defense",
            "block_chance": 0.3,
            "description": "30% probability to block attack."
        }

    @staticmethod
    def thunder_axe():
        return {
            "name": "Thunder Axe",
            "type": "stun",
            "stun_chance": 0.3,
            "description": "30% probability to stun the enemy for 3 seconds within 20 seconds."
        }

    @staticmethod
    def essence_of_renewal():
        return {
            "name": "Essence of Renewal",
            "type": "heal",
            "heal": 30,
            "description": "Restore 30 health points for twice."
        }

    @staticmethod
    def get_all():
        return {
            "Lion Sword": WeaponEffects.lion_sword(),
            "Hawk's Eye": WeaponEffects.hawks_eye(),
            "Luna Bow": WeaponEffects.luna_bow(),
            "Phoenix Feather": WeaponEffects.phoenix_feather(),
            "Hydro Strike": WeaponEffects.hydro_strike(),
            "Libra of Eternity": WeaponEffects.libra_of_eternity(),
            "Aegis Shield": WeaponEffects.aegis_shield(),
            "Thunder Axe": WeaponEffects.thunder_axe(),
            "Essence of Renewal": WeaponEffects.essence_of_renewal(),
        }
