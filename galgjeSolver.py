#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from operator import itemgetter

def listWords(wordFile):

	with open(wordFile, "r") as w:

		wordList = w.readlines()

	wordList = [l.strip() for l in wordList]
	wordList = [word.lower() for word in wordList if word.isalpha()]

	return wordList



def getCharFreq(wordList):

	characters 	= "".join(wordList)
	totalChars 	= len(characters)
	alphabet 	= list(set(characters))

	alphabet.sort()

	alphaFreq = []

	for char in alphabet:

		alphaFreq.append((char, characters.count(char) / float(totalChars) * 100))

	return alphaFreq



def getCharWordFreq(wordList):

	# Percentage of the words the character appears in

	alphabet 	= list(set("".join(wordList)))

	alphabet.sort()

	alphaWordFreq = []

	for char in alphabet:

		alphaWordFreq.append((char, sum([1 for word in wordList if char in word]) / float(len(wordList)) * 100))

	return alphaWordFreq



def viewCharFreq(charFreq, guessCharCorrect, guessCharFalse):

	charRanked = sorted(charFreq, key=lambda x: x[1], reverse=True)
	charRanked = [char for char in charRanked if char[0] not in guessCharCorrect and char[0] not in guessCharFalse]

	top 	= min([5, len(charRanked)])
	count 	= 0

	while count < top:

		print("%d. %s" %(count+1, charRanked[count]))

		count += 1



def updateWordList(wordList, length=None, containsChar=None, notContainsChar=None, places=None):

	if length:

		return [word for word in wordList if len(word) == length]

	if containsChar and places:

		return [word for word in wordList if all([word[place] == containsChar for place in places]) and word.count(containsChar) == len(places)]

	if notContainsChar:

		return [word for word in wordList if notContainsChar not in word]



def solver(wordList):

	wordLength = int(input("\nEnter the length of the word: "))

	# Limit word list to word length
	wordList = updateWordList(wordList, length=wordLength)

	#Update character frequencies for word length
	characterFreq 		= getCharFreq(wordList)
	characterWordFreq	= getCharWordFreq(wordList)

	# Parameters for progress-keeping
	guesses 			= 10
	guessCharCorrect 	= []
	guessCharFalse 		= []
	charLeft 			= wordLength
	wordView 			= ["-" for i in range(wordLength)]

	while guesses > 0 and charLeft > 0 and len(wordList) > 1:

		print("\nTop 5 character freqs (not picked):")

		viewCharFreq(characterFreq, guessCharCorrect, guessCharFalse)

		print("\nTop 5 character freqs (not picked, word-based):")

		viewCharFreq(characterWordFreq, guessCharCorrect, guessCharFalse)

		# Input guess
		guessChar = input("\nWhich character are you going to guess? (lowercase) ")
		guessCorrect = input("\nWas this guess correct? [y/n] ")

		while guessCorrect != "y" and guessCorrect != "n":

			guessCorrect = input("\nWas this guess correct? [y/n] ")

		if guessCorrect == "y":

			placeChar = input("\nWhat are the positions of %s? (1-indexed) " %(guessChar)).strip().split(" ")
			placeChar = [int(p)-1 for p in placeChar]

			wordList = updateWordList(wordList, containsChar=guessChar, places=placeChar)

			characterFreq = getCharFreq(wordList)
			characterWordFreq = getCharWordFreq(wordList)

			guessCharCorrect.append(guessChar)

			charLeft -= len(placeChar)

			for p in placeChar:

				wordView[p] = guessChar

		elif guessCorrect == "n":

			 guesses -= 1

			 wordList = updateWordList(wordList, notContainsChar=guessChar)

			 characterFreq = getCharFreq(wordList)
			 characterWordFreq = getCharWordFreq(wordList)

			 guessCharFalse.append(guessChar)

		print("\nProgress: %s" %(" ".join(wordView)))

		if len(wordList) < 10 or guesses == 0 or charLeft == 0:

			print("\nRemaining words:")

			for remains in wordList:

				print(remains)



if __name__ == "__main__":
	
	wordFile = "woorden.lst"

	wordList = listWords(wordFile)

	solver(wordList)

	print("\n")