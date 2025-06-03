# Contains all basic functionality for a game of blackjack

from flask import Flask, request, jsonify, render_template
import random

app = Flask(
    __name__,
    static_folder="../static",
    template_folder="../templates"
)

game_state = {
'deck': [],
'firstMove': False,
'canSplit': False,
'playerHand': [],
'dealerHand': [],
'output': 'Welcome to Blackjack!',
'status': ''
}

@app.route('/get-state', methods=['GET'])
def get_game_state():
    return jsonify(game_state)


@app.route('/action', methods=['POST'])
def play_hand():
    data = request.json
    action = data.get('action')

    match action:
        case 'deal':
            game_state['playerHand'] = []
            game_state['dealerHand'] = []
            # if the deck is halfway done, it is reset and shuffled
            if len(game_state['deck']) < 52:
                game_state['deck'] = create_deck(2)
            deal_cards()
            # check_blackjack updates game_state['status'] if a blackjack is found
            # if not, 'None' is returned
            bj_result = check_blackjack()
            if bj_result == 'None':
                game_state['firstMove'] = True
                game_state['canSplit'] = can_split()
                game_state['status'] = 'playerTurn'
            else:
                check_win()
        case 'hit':
            hit()
            game_state['firstMove'] = False
        case 'stand':
            stay()
        case 'double':
            double()
        case 'split':
            split()
        case _:
            raise Exception('No valid action provided.')
        
    return jsonify(game_state)


def create_deck(num):
    # Number passed determines how many standard decks to include within the main deck
    new_deck = [2, 3, 4, 5, 6 ,7, 8 ,9, 10, 'J', 'Q', 'K', 'A'] * 4 * num
    random.shuffle(new_deck)
    return new_deck


def deal_cards():
    game_state['playerHand'].append(game_state['deck'].pop())
    game_state['dealerHand'].append(game_state['deck'].pop())
    game_state['playerHand'].append(game_state['deck'].pop())
    game_state['dealerHand'].append(game_state['deck'].pop())


def hand_total(hand):
    total = 0
    aces = 0
    for i in hand:
        if i == 'A':
            aces += 1
            total += 11
        elif i in ['J', 'Q', 'K']:
            total += 10
        else:
            total += i

    while aces > 0:
        if total > 21:
            total -= 10
            aces -= 1
        else:
            break

    return total


def can_split():
    return game_state['playerHand'][0] == game_state['playerHand'][1] and len(game_state['playerHand']) == 2


def split():
    hand1 = [game_state['playerHand'][0], game_state['deck'].pop()]
    hand2 = [game_state['playerHand'][1], game_state['deck'].pop()]
    


def check_bust():
    total = hand_total(game_state['playerHand'])
    if total > 21:
        return True
    elif total == 21:
        stay()
    else:
        return False


def check_win():
    player_total = hand_total(game_state['playerHand'])
    dealer_total = hand_total(game_state['dealerHand'])
    if player_total > 21:
        game_state['output'] = 'Loss. Player bust'
    elif dealer_total > 21:
        game_state['output'] = 'Win. Dealer bust'
    elif player_total < dealer_total:
        game_state['output'] = 'Loss'
    elif player_total > dealer_total:
        game_state['output'] = 'Win'
    else:
        game_state['output'] = 'Push' # Tie
    game_state['status'] = 'roundOver'


def check_blackjack():
    if hand_total(game_state['dealerHand']) == 21:
        game_state['output'] = 'Dealer Blackjack. Loss.'
        game_state['status'] = 'roundOver'
    elif hand_total(game_state['playerHand']) == 21:
        game_state['output'] = 'Player Blackjack. Win.'
        game_state['status'] = 'roundOver'
    else:
        return 'None'


def hit():
    new_card = game_state['deck'].pop()
    game_state['playerHand'].append(new_card)
    if check_bust():
        check_win()
    game_state['firstMove'] = False

def stay():
    dealer_total = hand_total(game_state['dealerHand'])
    while dealer_total < 17:
        game_state['dealerHand'].append(game_state['deck'].pop())
        dealer_total = hand_total(game_state['dealerHand'])
    check_win()


def double():
    new_card = game_state['deck'].pop()
    game_state['playerHand'].append(new_card)
    if check_bust():
        check_win()
    else:
        stay()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    
