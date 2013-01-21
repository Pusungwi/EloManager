#!/usr/bin/env python

# EloManager v0.1
# Author : Yi 'Pusungwi' Yeon Jae

INITIAL_RATING = 1200
MAX_INCREASE_RATING = 40
DEFAULT_DB_NAME = "EloManager"

import uuid

class Player:
	def __init__(self, name, rating=INITIAL_RATING, win=0, loss=0, uuid=str(uuid.uuid1())):
		self.name = name
		self.uuid = uuid
		self.rating = rating
		self.win = 0
		self.loss = 0

	def __str__(self):
		return("Name : " + self.name + " Rating : " + str(self.rating) + " Win : " + str(self.win) + " Loss : " + str(self.loss))

	def getRating(self):
		return self.rating

	def getName(self):
		return self.name

	def getWinCount(self):
		return self.win

	def getLossCount(self):
		return self.loss

	def getPlayerUUID(self):
		return self.uuid

class EloManager:
	def __init__(self):
		print("Manager Init...")
		self.playersList = []

	def savePlayersListToRedis(self, address, port=27910, dbName=DEFAULT_DB_NAME):
		print("tmp")

	def loadPlayersListFromRedis(self, address, port=27910, dbName=DEFAULT_DB_NAME):
		print("TMP")

	def isEmptyPlayersList(self):
		if len(playersList) == 0:
			return 0
		else:
			return 1

	def isAvailablePlayerName(self, playerName):
		#RETURN CODE TYPE : 1 - no problem, 0 - somebody already use this name
		returnCode = 1

		for tmpPlayer in self.playersList:
			tmpPlayerName = tmpPlayer.getName()
			if tmpPlayerName == playerName:
				returnCode = 0
				return returnCode

		return returnCode


	def getPlayersList(self):
		return self.playersList

	def getPlayerByUUID(self, targetUUID):
		for player in self.playersList:
			if targetUUID == player.uuid:
				return player

	def getPlayerByName(self, targetName):
		for player in self.playersList:
			if targetName == player.name:
				return player

	def getPlayersListByRating(self, minRating, maxRating):
		resultsList = []
		for player in self.playersList:
			playerRating = player.getRating()
			if playerRating >= int(minRating) & playerRating <= int(maxRating):
				print("rating : " + str(playerRating))
				resultsList.append(player)
		return resultsList

	def appendPlayer(self, player):
		type(player)

	def addNewPlayer(self, name):
		if self.isAvailablePlayerName(name) == 1:
			tmpPlayer = Player(name)
			self.playersList.append(tmpPlayer)
		else:
			print("ERROR: not available this name") 

	def removePlayerByName(self, targetName):
		for player in self.playersList:
			if targetName == player.name:
				self.playersList.remove(player)
				break

	def setResult(self, winUser, lossUser):
		incDecRating = round(MAX_INCREASE_RATING * 1 / (1 + 10 ** ((winUser.rating - lossUser.rating) / 400)))
		
		winUser.win += 1
		lossUser.loss += 1
		
		winUser.rating += incDecRating
		lossUser.rating -= incDecRating

		print("[Winner : " + winUser.name + " W:" + str(winUser.win) + " L:" + str(winUser.loss) + " Rating:" + str(winUser.rating) +
		 "] [Loser : " + lossUser.name + " W:" + str(lossUser.win) + " L:" + str(lossUser.loss) + " Rating:" + str(lossUser.rating) + "]")

	def setResultByName(self, winUserName, lossUserName):
		tmpWinUser = self.getPlayerByName(winUserName)
		tmpLossUser = self.getPlayerByName(lossUserName)

		self.setResult(tmpWinUser, tmpLossUser)

if __name__ == "__main__":
	manager = EloManager()

	manager.addNewPlayer("ASDF")
	manager.addNewPlayer("rokucha")
	manager.addNewPlayer("1234")
	manager.addNewPlayer("666")

	asdf = manager.getPlayerByName("ASDF")
	rokucha = manager.getPlayerByName("rokucha")
	numbers = manager.getPlayerByName("1234")
	devil = manager.getPlayerByName("666")

	manager.setResultByName(winUserName="666", lossUserName="1234")

	#playerOne = manager.getPlayerByName("PUSUNGWI")
	#playerTwo = manager.getPlayerByName("ADFASDF")
	#playerThree = manager.getPlayerByName("HAHAHAH")

	tmp = manager.getPlayersListByRating(1180,1200)