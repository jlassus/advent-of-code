test = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

cards = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
card_values = {v: i for i, v in enumerate(cards, start=1)}

def get_card_value(card, j):
    if card == 'J' and j:
        return 0
    return card_values[card]

def get_hand_type(hand, j):
    value_counts = {}
    for card in hand:
        value_counts[card] = value_counts.get(card, 0) + 1
    if j and (j_count := value_counts.get('J', 0)):
        if j_count == 5:
            return 6
        del value_counts['J']
        max_value = max(value_counts.items(), key=lambda v: v[1])
        value_counts[max_value[0]] += j_count
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
        if len(value_counts) == 3:
            return 2  # two pair
        return 1  # one pair
    return 0  # high card

def compare_key(hand, j=False):
    return (sum(get_card_value(c, j) << (i << 2) for i, c in enumerate(reversed(hand)))
            + (get_hand_type(hand, j) << 20))

def f(data, part, debug):
    hands_and_bids = [line.split() for line in data]
    hands_and_bids.sort(key=lambda v: compare_key(v[0], part == 2))
    winnings = 0
    for rank, (hand, bid) in enumerate(hands_and_bids, start=1):
        winnings += rank * int(bid)
    return winnings
