class Data: #data class to store level progress 
    def __init__(self): #automatically called when object is created 
        self.unlocked_level = 6 #tracks the highest level that has been unlocked
        self.current_level = 0 #tracls the player current level