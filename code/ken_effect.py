class WeaponEffects:
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
        boss.health -= 500
        print("Lion Sword used! Boss -500 HP")

    @staticmethod
    def hawks_eye(mario, boss):
        # Example: improve Mario's bullet damage
        print("Hawk's Eye used!")

    @staticmethod
    def luna_bow(mario, boss):
        print("Luna Bow used!")

    @staticmethod
    def phoenix_feather(mario, boss):
        mario.health = min(mario.health + 30, 100)
        print("Phoenix Feather used! Mario +30 HP")

    @staticmethod
    def hydro_strike(mario, boss):
        boss.health -= 300
        print("Hydro Strike used! Boss -300 HP")

    @staticmethod
    def libra_eternity(mario, boss):
        mario.health = 100
        boss.health = 10000
        print("Libra of Eternity used! Reset battle!")

    @staticmethod
    def aegis_shield(mario, boss):
        print("Aegis Shield used!")

    @staticmethod
    def thunder_axe(mario, boss):
        boss.health -= 800
        print("Thunder Axe used! Boss -800 HP")

    @staticmethod
    def essence_renewal(mario, boss):
        mario.health += 50
        print("Essence of Renewal used! Mario +50 HP")
