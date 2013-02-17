#!/usr/bin/env python

# EloManager v0.1
# Author : Yi 'Pusungwi' Yeon Jae

INITIAL_RATING = 1200
MAX_INCREASE_RATING = 40
DEFAULT_DB_NAME = "EloManager"
DEBUG_MODE = 1

from datetime import datetime
from uuid import uuid4
import xml.etree.ElementTree as ET

class Player:
	def __init__(self, name, uuid=None, rating=INITIAL_RATING, win=0, loss=0):
		self.name = name
		if uuid == None:
			self.uuid = uuid4()
		else:
			self.uuid = uuid
		self.rating = rating
		self.win = win
		self.loss = loss
		self.history = []

	def __str__(self):
		return("Name : " + self.name + "	Rating : " + str(self.rating) + " Win : " + str(self.win) + " Loss : " + str(self.loss))

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

	def loadMatchesResultFromXml(self, xmlPath):
		# RETURN CODE 0 - fail 1 - success
		print("loading matches result file...")
		tree = ET.parse(xmlPath)
		resultXmlRoot = tree.getroot()
		if resultXmlRoot.tag != "elomanager":
			print("ERROR: incorrect xml file")
			return 0
		else:
			for match in resultXmlRoot.iter("match"):
				winner = match.find("winner").text
				loser = match.find("loser").text

				if self.getPlayerByName(winner) == None:
					self.addNewPlayer(winner)
				if self.getPlayerByName(loser) == None:
					self.addNewPlayer(loser)

				self.setResultByName(winner, loser)
			
			print("load success!")
			return 1

	def exportPlayersListToXml(self, xmlPath):
		print("saving players list file...")

	def importPlayersListFromXml(self, xmlPath):
		print("loading players list file...")
		tree = ET.parse(xmlPath)
		resultXmlRoot = tree.getroot()
		if resultXmlRoot.tag != "elomanager":
			print("ERROR: incorrect xml file")
			return 0
		else:
			for player in resultXmlRoot.iter("player"):
				playerName = player.find('name').text
				playerUUID = player.find('uuid').text
				playerRating = int(player.find('rating').text)
				playerWinCount = int(player.find('winCount').text)
				playerLossCount = int(player.find('lossCount').text)

				tmpPlayer = Player(playerName, uuid=playerUUID, rating=playerRating, win=playerWinCount, loss=playerLossCount)

				#get match result
				for match in player.iter('match'):
					matchDict = {'result':int(match.find('result').text), 'opponentUUID':match.find('opponentUUID').text, 'date':float(match.find('date').text)}
					tmpPlayer.history.append(matchDict)

				self.appendPlayerByClass(tmpPlayer)
			print("load success!")
			return 1

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
		return None

	def getPlayerByName(self, targetName):
		for player in self.playersList:
			if targetName == player.name:
				return player
		return None

	def getPlayersListByRating(self, minRating, maxRating):
		resultsList = []
		for player in self.playersList:
			playerRating = player.getRating()
			if playerRating >= int(minRating) and playerRating <= int(maxRating):
				if DEBUG_MODE == 1:
					print("getPlayersListByRating - rating : " + str(playerRating)) DEBUG CODE
				resultsList.append(player)
		return resultsList

	def appendPlayerByClass(self, player):
		# NEED SOME CLASS CHECK METHOD
		self.playersList.append(player)

	def addNewPlayer(self, name):
		if self.isAvailablePlayerName(name) == 1:
			tmpPlayer = Player(name)
			self.appendPlayerByClass(tmpPlayer)
		else:
			print("ERROR: not available this name") 

	def removePlayerByName(self, targetName):
		for player in self.playersList:
			if targetName == player.name:
				self.playersList.remove(player)
				break

	def setResult(self, winUser, lossUser):
		currTimeStamp = datetime.timestamp(datetime.today())
		incDecRating = round(MAX_INCREASE_RATING * 1 / (1 + 10 ** ((winUser.rating - lossUser.rating) / 400)))
		
		winUser.win += 1
		lossUser.loss += 1
		
		winUser.rating += incDecRating
		lossUser.rating -= incDecRating

		#DICT INFO : result 0 - loss, 1 - win, opponentUUID - nuff said.
		winUser.history.append({'result': 1,'opponentUUID': lossUser.uuid, 'date':currTimeStamp})
		lossUser.history.append({'result': 0,'opponentUUID': winUser.uuid, 'date':currTimeStamp})

		if DEBUG_MODE == 1:
			print("[Winner : " + winUser.name + " W:" + str(winUser.win) + " L:" + str(winUser.loss) + " Rating:" + str(winUser.rating) +
		 	"] [Loser : " + lossUser.name + " W:" + str(lossUser.win) + " L:" + str(lossUser.loss) + " Rating:" + str(lossUser.rating) + "]")

	def setResultByName(self, winUserName, lossUserName):
		if winUserName == lossUserName:
			return 0

		tmpWinUser = self.getPlayerByName(winUserName)
		tmpLossUser = self.getPlayerByName(lossUserName)

		self.setResult(tmpWinUser, tmpLossUser)

		return 1

if __name__ == "__main__":
	manager = EloManager()

	#matches result test code
	#manager.loadMatchesResultFromXml("matchExample.xml")
	#tmp = manager.getPlayersList()

	#player list xml test code
	manager.importPlayersListFromXml('playerExample.xml')
	tmp = manager.getPlayersList()

	print("init test...")
	for player in tmp:
		print(player)
	print("END")