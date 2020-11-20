#!/usr/bin/env Python3

import cmd
import sys
import os
import time
import math
import random
import collections



  ### Define Classes ###

class Player:
    def __init__(self, name):
        self.name = name
        self.bank = 20.00
        self.blind = ''
        self.start_hand = []
        self.full_hand = {}
        self.set = []
        self.royal = False
        self.flush = False
        self.straight = False
        self.hand_rank = ''

class Hand:
    def __init__(self, name, rank):
        self.name = ''
        self.rank = 0

class Card:
    def __init__(self, name, value):
        self.name = ''
        self.value = 0
        self.suit = ''

myPlayer = Player('')
oppo = Player('Poker Trainer')


deck = []
community = []

  ### Establish rules for ranking ###
values = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
}

hand_ranks = {
    'Royal Flush': 10,
    'Straight Flush': 9,
    'Four of a Kind': 8,
    'Full House': 7,
    'Flush': 6,
    'Straight': 5,
    'Three of a Kind': 4,
    'Two Pair': 3,
    'Pair': 2,
    'High Card': 1
}


  ### Function that shuffles deck and deals to players ###
def shuffle_deck():
    deck.clear()
    community.clear()
    card_type = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    card_suit = ['H', 'D', 'C', 'S']
    for _type in card_type:
        for _suit in card_suit:
            deck.append(_type + _suit)
    random.shuffle(deck)
    for i in range(2):
        myPlayer.start_hand.append(deck.pop(0))
        oppo.start_hand.append(deck.pop(0))

  ### Function that executes Flop, Turn, and River ###
def flip():
    if len(community) == 0:
        for i in range(3):
            community.append(deck.pop(0))

    elif len(community) < 5:
        community.append(deck.pop(0))
  ### Function that evaluates player's hand ###
def hand_eval(player):
    player.full_hand = {}
    hand = player.start_hand + community
#    hand =[]
    player.full_hand = dict.fromkeys(hand) # Create dictionary of all cards available to player


  ### Assign values to the cards in the dictionary for ranking ###
    for i in hand:
        temp = [i[1]]
        if len(i) == 3:
            temp = [i[2], 10]
            player.full_hand[i] = temp
        elif not i[0].isdigit():
            temp.append(values[i[0]])
            player.full_hand[i] = temp
        else:
            temp.append(int(i[0]))
            player.full_hand[i] = temp

  ### Determine hand type ###
    # First, look for Flush #
    test_list = []
    flush_suit = ''
    def sort_key(x): #function for defining sort parameters
        if len(x) == 3:
            return 10
        elif x[0] in values:
            return values[x[0]]
        else:
            return int(x[0])

    for i in player.full_hand:
            test_list.append(player.full_hand[i][0])
    c = collections.Counter(test_list)
    for i in c:
        if c[i] == 5:
            player.flush = True
            player.hand_rank = 'Flush'
            flush_suit = i
            hand = sorted(hand, key=sort_key, reverse=True)

    # Next, look for straight #
    num_val = []
    sorted_list = sorted(hand, key=sort_key, reverse=True) #sort list from high value to low

    def extractor(list, list2):
        for i in list: #extract sorted values into new list
            if len(i) == 3:
                list2.append(10)
            elif i[0] in values:
                list2.append(values[i[0]])
            else:
                list2.append(int(i[0]))
    extractor(sorted_list, num_val)
    num_val2 = list(dict.fromkeys(num_val)) #remove duplicates

    if len(num_val2) >= 5: #check for running straight
        count = 0
        x = 0
        for i in num_val2:
            if x == len(num_val2) - 1:
                break
            elif not num_val2[x] - num_val2[x + 1] == 1:
                x += 1
                count = 0
            else:
                count += 1
                x += 1
            if count >= 4:
                player.straight = True
                if not player.hand_rank == 'Flush':
                    player.hand_rank = 'Straight'
                    print(num_val2)
                    hand = sorted_list
                    break
  ### Next, determine if hand is straight flush or royal flush###
    if player.flush is True:
        ext_list = []
        ext_list2 = []
        for i in hand:
            if flush_suit in i:
                ext_list.append(i)
                ext_list = sorted(ext_list, key=sort_key, reverse=True)
        extractor(ext_list, ext_list2)
        if len(ext_list2) >= 5:  # check for running straight in flush hand
            count = 0
            x = 0
            for i in ext_list2:
                if x == len(ext_list2) - 1:
                    break
                elif not ext_list2[x] - ext_list2[x + 1] == 1:
                    x += 1
                    count = 0
                else:
                    count += 1
                    x += 1
                if count >= 4:
                    if ext_list2[0] == 14:
                        player.royal = True
                        player.hand_rank = 'Royal Flush'
                    else:
                        player.hand_rank = 'Straight Flush'

  ### Next, look for pairs and pair sequences ###
    new = []
    if player.flush is False:
        for i in sorted_list:
            if len(i) == 3:
                new.append(10)
            else:
                new.append(i[0])

        new = collections.Counter(new)
        for i in new:
            if new[i] == 4:
                if player.hand_rank == '' or player.hand_rank in ['Straight Flush', 'Royal Flush']:
                    player.hand_rank = 'Four of a Kind'
                    player.set.append(i)
                break
            elif new[i] == 3:
                player.set.append(i)
                for x in new:
                    if new[x] == 2:
                        player.set.append(x)
                        player.set = sorted(player.set, key=sort_key, reverse=True)
                        player.hand_rank = 'Full House'
                        break
                    else:
                        player.hand_rank = 'Three of a Kind'
                break
            elif new[i] == 2:
                player.set = [] # not sure why I have to reset this list here
                for x in new:
                    if (len(player.set) < 2) and new[x] == 2:
                        player.set.append(x)
                    else:
                        pass
                if (len(player.set) == 2) and  not player.hand_rank == 'Full House':
                    player.hand_rank = 'Two Pair'
                elif not player.hand_rank == 'Full House':
                    player.hand_rank = 'Pair'
                    break
                break
            elif (player.flush is False) and (player.straight is False):
                player.hand_rank = 'High Card'
                if len(player.set) == 0:
                    player.set.append(i)


    print(player.set)
    print(hand)











shuffle_deck()
flip()
flip()
flip()
hand_eval(myPlayer)

print('You have {}'.format(myPlayer.hand_rank))



'''samp = [
    ['AH', 'KH', 'QH', 'JH', '10H'],
    ['5S', '6S', '7S', '8S', '9S'],
    ['AH', 'AC', 'AD', 'AS', '2H'],
    ['AH', 'AC', 'AD', 'KS', 'KH'],
    ['5S', '6S', '7S', '8S', 'JS'],
    ['5C', '6S', '7H', '8S', '9S'],
    ['AH', 'AC', 'AD', '3S', '2H'],
    ['AH', 'AC', 'KD', 'KS', '2H'],
    ['AH', 'AC', 'QD', 'JS', '2H'],
    ['AH', '4C', 'QD', 'JS', '2H']
]'''

