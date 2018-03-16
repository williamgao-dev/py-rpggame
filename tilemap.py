import pygame as py


# Load assets, gamesounds, spriteimages, sound channels.. etc.
class Map:
    def __init__(self,filename):
        # Assign var gameFolder to root folder
        gameFolder = path.dirname(__file__)

        # Creates list mapData to store all lines in map.txt
        self.mDta = []

        # Open map.txt
        with open(path.join(gameFolder, 'map.txt'),'rt') as f:
            for line in f:
                self.data.append(line)
        # # Debug
        # print (mapData)