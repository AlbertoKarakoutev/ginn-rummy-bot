import random
from copy import deepcopy

card_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
card_suites = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
cards = []
hand = []
in_combination = []
not_in_combination = [0]
cards_passed = 0
chance = 0

# Card deck building
for i in card_suites:
    for j in card_numbers:
        cards.append([i, j])

# Random hand distributing
i = 0
while i < 10:
    candidate = random.choice(cards)
    if candidate not in hand:
        hand.append(candidate)
        i += 1

# Concrete hand distributing (Debug)
hand =[['Spades', 6], ['Spades', 1], ['Hearts', 13], ['Hearts', 12], ['Hearts', 4], ['Diamonds', 7], ['Diamonds', 4], ['Diamonds', 2], ['Clubs', 6], ['Clubs', 1]]

# Sorting hand based on suites and card size
for card_c in cards:
    for card_h in hand:
        if card_h[0] == card_c[0] and card_h[1] == card_c[1]:
            hand.remove(card_h)
            hand.insert(0, card_h)


# Upon creating combination, scan the entire hand for cards to add to that combination
def combination_morph(combination, virt_hand):
    for index in range(1, len(combination)):
        card = combination[index]
        for comp_card in virt_hand:
            if combination[0] == 1:
                if card[0] == comp_card[0]:
                    if abs(card[1] - comp_card[1]) <= 1:
                        combination.append(comp_card)
                        virt_hand.remove(comp_card)
                        combination_morph(combination, virt_hand)
                        return
            if combination[0] == 2:
                if card[1] == comp_card[1]:
                    combination.append(comp_card)
                    virt_hand.remove(comp_card)
                    combination_morph(combination, virt_hand)
                    return


# Sort the cards into card combinations - Sequential or Identical
def configure(player_hand):
    virtual_hand = deepcopy(player_hand)
    current_card = []
    while 1:
        added = False
        if len(virtual_hand) > 0:
            current_card = virtual_hand[0]
        else:
            break
        virtual_hand.remove(current_card)
        # Combination[0] codes:
        # 1 - Sequential combination
        # 2 - Identical combination
        # 0 - Not in combination

        # Creating new seq. combination (if possible)
        for comparing_card in virtual_hand:
            if current_card[0] == comparing_card[0]:
                if abs(current_card[1] - comparing_card[1]) <= 1:
                    virtual_hand.remove(comparing_card)
                    new_combination = [1, current_card, comparing_card]
                    combination_morph(new_combination, virtual_hand)
                    in_combination.append(new_combination)
                    added = True
                    break
        if not added:

            # Creating new identical combination (if possible)
            for comparing_card in virtual_hand:
                if current_card[1] == comparing_card[1]:
                    virtual_hand.remove(comparing_card)
                    in_combination.append([2, comparing_card, current_card])
                    added = True
                    break
        if not added:
            not_in_combination.append(current_card)

    new_hand = [in_combination, not_in_combination]
    for combination in in_combination:
        print(combination)
    print(not_in_combination)
    return new_hand


# Calculate the chance that the next card will be 'valuable' to the player
def chance():
    chance = 0
    for c in in_combination:
        c1 = deepcopy(c)
        if c1[0] == 1:
            c1.remove(c1[0])
            card_in_hand = False
            max_card = max(c1, key=lambda x: x[1])
            min_card = min(c1, key=lambda x: x[1])
            if max_card[1] < 13:
                for comb in in_combination:
                    if [c1[0][0], max_card[1] + 1] in comb:
                        card_in_hand = True
                if not card_in_hand:
                    chance += 1/52
            card_in_hand = False
            if min_card[1] > 1:
                for comb in in_combination:
                    if [c1[0][0], min_card[1] - 1] in comb:
                        card_in_hand = True
                if not card_in_hand:
                    chance += 1 / 52
        if c1[0] == 2:
            c1.remove(c1[0])
            card_in_hand = False
            suites_cpy = deepcopy(card_suites)
            for card in c1:
                suites_cpy.remove(card[0])
            for comb in in_combination:
                if comb[0] == 1:
                    for a in range(1, len(comb)):
                        card = comb[a]
                        if card[0] in suites_cpy:
                            if card[1] == c1[0][1]:
                                card_in_hand = True
            if not card_in_hand:
                chance += (1/52) * len(suites_cpy)
    return chance * 100


# print("hand:")
print(hand)
configure(hand)
print(chance())
