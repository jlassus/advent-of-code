from collections import defaultdict

test = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

card_values = {v: i for i, v in enumerate(('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'))}

def get_hand_type(hand):
    value_counts = defaultdict(int)
    for card in hand:
        value_counts[card] += 1
    max_count = max(value_counts.values())
    if max_count == 5:
        return 6  # five of a kind
    if max_count == 4:
        return 5  # four of a kind
    if max_count == 3:
        if len(value_counts) == 2:
            return 4  # full house
        return 3  # three of a kind
    if max_count == 2:
        if list(value_counts.values()).count(2) == 2:
            return 2  # two pair
        return 1  # one pair
    return 0  # high card

def compare(hand):
    return (get_hand_type(hand) * 100 ** 5
            + card_values[hand[0]] * 100 ** 4
            + card_values[hand[1]] * 100 ** 3
            + card_values[hand[2]] * 100 ** 2
            + card_values[hand[3]] * 100
            + card_values[hand[4]])

def f1(data, debug):
    hands_and_bids = [line.split() for line in data]
    hands_and_bids.sort(key=lambda v: compare(v[0]))
    winnings = 0
    for rank, (hand, bid) in enumerate(hands_and_bids, start=1):
        winnings += rank * int(bid)
    return winnings
