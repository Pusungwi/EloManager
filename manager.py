#!/usr/bin/env python

# EloManager v0.1
# Author : Yi 'Pusungwi' Yeon Jae

INITIAL_RATING = 1200
MAX_INCREASE_RATING = 40

class Player:
	def __init__(self, name, rating=INITIAL_RATING, win=0, loss=0):
		self.name = name
		self.rating = rating
		self.win = 0
		self.loss = 0

	def __str__(self):
		return("Name : " + self.name + " Rating : " + str(self.rating) + " Win : " + str(self.win) + " Loss : " + str(self.loss))

	def getRating(self):
		return self.rating

class EloManager:
	def __init__(self):
		print("Manager Init...")
		self.playersList = []

		newUser = Player('PUSUNGWI')
		oldUser = Player('HAHAHAH')
		thirdUser = Player('HSDFSDFDF')
		fourthUser = Player('ADFASDF')

		self.playersList.append(newUser)
		self.playersList.append(oldUser)
		self.playersList.append(thirdUser)
		self.playersList.append(fourthUser)

	def isEmptyPlayersList(self):
		if len(playersList) == 0:
			return 0
		else:
			return 1

	def getPlayersList(self):
		return self.playersList

	def getPlayerByName(self, targetName):
		for player in self.playersList:
			if targetName == player.name:
				return player

	def getPlayersListByRating(self, minRating, maxRating):
		resultsList = []
		for player in self.playersList:
			if player.rating >= int(minRating) & player.rating <= int(maxRating):
				resultsList.append(player)
		return resultsList

	def setResult(self, winUser, lossUser):
		incDecRating = round(MAX_INCREASE_RATING * 1 / (1 + 10 ** ((winUser.rating - lossUser.rating) / 400)))
		
		winUser.win += 1
		lossUser.loss += 1
		
		winUser.rating += incDecRating
		lossUser.rating -= incDecRating

		print("[Winner : " + winUser.name + " W:" + str(winUser.win) + " L:" + str(winUser.loss) + " Rating:" + str(winUser.rating) +
		 "] [Loser : " + lossUser.name + " W:" + str(lossUser.win) + " L:" + str(lossUser.loss) + " Rating:" + str(lossUser.rating) + "]")

if __name__ == "__main__":
	manager = EloManager()
	playerOne = manager.getPlayerByName("PUSUNGWI")
	playerTwo = manager.getPlayerByName("ADFASDF")
	playerThree = manager.getPlayerByName("HAHAHAH")

	manager.setResult(winUser=playerOne, lossUser=playerTwo)
	manager.setResult(winUser=playerThree, lossUser=playerOne)
	manager.setResult(winUser=playerOne, lossUser=playerThree)
	manager.setResult(winUser=playerTwo, lossUser=playerThree)
	manager.setResult(winUser=playerThree, lossUser=playerTwo)