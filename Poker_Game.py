import random

def getSpecsFromUser(name):
	#get inputs from user
    DECK_SIZE = 52
    print "Hi {name}, how many players are there?".format(**locals())
    num_players = input("\tnumber of players: ")
    num_cards_per_player = 5
    too_few_cards = tooFewCards(num_players, num_cards_per_player)
    while too_few_cards:
        print "\n[!] not enough cards (%d requested but we only have %d)" % ((num_players*num_cards_per_player), DECK_SIZE)
        num_cards_per_player = input("\ttry again. number of cards per player: ")
        too_few_cards = tooFewCards(num_players, num_cards_per_player)
    return num_players, num_cards_per_player

def tooFewCards(num_players, num_cards, deckSize=52):
	#check to make sure we have enough cards
    return (num_players * num_cards > deckSize)


def createCards():
	#create cards
    number_names = map(str, range(2,10))
    face_names = ["Ten", "Jack", "Queen", "King", "Ace"]
    all_names = number_names + face_names
    suits = ["Hearts", "Spades", "Diamonds", "Clubs"]
    theDeck = []
    for card_name in all_names:
        for suit in suits:
            card = (card_name[0],suit[0], ' of '.join((card_name, suit)))
            theDeck.append(card)
    return theDeck

def dealCards(num_players, num_cards_per_player, the_deck):
	#deal cards to players
    def make_table(number_of_players):
    	#create a list of lists that is the table
        table = []
        for player in range(number_of_players):
            seat = []
            table.append(seat)
        return table

    table = make_table(num_players) 
    cards_to_deal =  num_players * num_cards_per_player
    random.shuffle(the_deck)
    for i in range(cards_to_deal):
        goes_to_player = i % num_players
        card_to_deal = the_deck[i]
        table[goes_to_player].append(card_to_deal)
    return table

def card_ranks(hand):
#find the rank of cards
    ranks = ['--23456789TJQKA'.index(r) for r, s, prettyboi in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def flush(hand):
#True if player has flush
    suits = [s for r, s, prettyboi in hand]
    return len(set(suits)) == 1

def straight(ranks):
 #True if player has straight
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def getN(ranks):
#get the count of similar cards
    for r in ranks:
        return ranks.count(r)

def four_of_a_kind(n, ranks):
#does player have four of a kind?
    for r in ranks:
        if ranks.count(r) == 4: return r
    return None

def three_of_a_kind(n, ranks):
#does player have three of a kind?
    for r in ranks:
        if ranks.count(r) == 3: return r
    return None

def two_of_a_kind(n, ranks):
#does player have two of a kid
    for r in ranks:
        if ranks.count(r) == 2: return r
    return None

def none_of_a_kind(n, ranks):
#does this player have no pairs
    for r in ranks:
        if ranks.count(r) == 1: return r
    return None

def two_pair(n,ranks):
#does player have two pairs?
        pair = two_of_a_kind(n, ranks)
        lowpair = two_of_a_kind(n, list(reversed(ranks)))
        if pair and lowpair != pair:
            return (pair, lowpair)
        else:
            return None

def hand_rank(hand):
#Return value indicating the ranking of a hand
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif four_of_a_kind(4, ranks):
        return (7, four_of_a_kind(4, ranks), none_of_a_kind(1, ranks))
    elif three_of_a_kind(3, ranks) and two_of_a_kind(2, ranks):
        return (6, three_of_a_kind(3, ranks), two_of_a_kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif three_of_a_kind(3, ranks):
        return (3, three_of_a_kind(3, ranks), ranks)
    elif two_pair(2,ranks):
        return (2, two_pair(2,ranks), ranks)
    elif two_of_a_kind(2, ranks):
        return (1, two_of_a_kind(2, ranks), ranks)
    else:
        return (0, ranks)

def findWinningHand(hands):
#find the winning hand
    return max(hands, key=hand_rank)


def printTable(table):
    
    for i, player in enumerate(table):
        print "Here is player {i}'s cards: ".format(i=i+1)
        for card in player:
            card_name = card[2]
            print "\t> {card_name}".format(**locals())
        print
        
def printResults(table):
	for i, player in enumerate(table):
		print "Here are player {i}'s cards: ".format(i=i+1)
		for card in player:
			card_name = card[2]
			print "\t> {card_name}".format(**locals())
		rank = hand_rank(player)
		if rank[0] == 1:
			print "This player has a pair, nice"
		elif rank[0] == 2:
			print "This player has two pair, cool!"
		elif rank[0] == 3:
			print "This player has three of a kind, whoa"
		elif rank[0] == 4:
			print "This player has a straight, yahoo"
		elif rank[0] == 5:
			print "This player has a flush!"
		elif rank[0] == 6:
			print "This player has a full house, lucky!"
		elif rank[0] == 7:
			print "This player has four of a kind, very rare!"
		elif rank[0] == 8:
			print "This player has a straight flush, WINNER!"
		elif rank[0] == 0:
			print "This player has nothing"
		print
	winner = findWinningHand(table)
	winningHand = []
	print "Here is the winning hand: "
	for card in winner:
		card_name = card[2]
		print "\t> {card_name}".format(**locals())
	print
	
        
def playPoker():
    player_name = 'Kyle'
    num_players, num_cards_per_player = getSpecsFromUser(player_name)
    print "Let's play poker!"
    print "Confirmed number of players: ", num_players
    print "Number of cards per player: ", num_cards_per_player
    print
    theDeck = createCards()
    table = dealCards(num_players, num_cards_per_player, theDeck)
    printResults(table)
playPoker()
