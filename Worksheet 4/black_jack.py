import random 

card_values_dict = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10, "A":11}
class BlackJack:
    deck = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]*4
    dealer_cards = []
    player_cards = []

    NUM_DECKS = 1
    SHUFFLE_WHEN_REMAINING_CARDS = 20

    def __init__(self):
        # Setup how many decks 
        self.deck = self.deck * self.NUM_DECKS
        # Shuffle deck before playing
        random.shuffle(self.deck)

    def print_state(self):
        print("Dealer first card:", self.dealer_cards[0])
        print("Player cards:", self.player_cards, "total:", self.calc_player_hand())

    def start_play(self):
        # Check when to shuffle
        if len(self.deck) < self.SHUFFLE_WHEN_REMAINING_CARDS:
            print("Should shuffle - TODO")
        # Deal cards
        self.dealer_cards.append(self.deck.pop())
        self.player_cards.append(self.deck.pop())
        self.dealer_cards.append(self.deck.pop())
        self.player_cards.append(self.deck.pop())
        # start the game loop
        self.game_loop()

    def hit_player(self):
        self.player_cards.append(self.deck.pop())
    def hit_dealer(self):
        self.dealer_cards.append(self.deck.pop())

    def calc_dealer_hand(self):
        # TODO: What about an Ace, when to count it as 1 or 11
        value_count = 0
        for card in self.dealer_cards:
            value = card_values_dict[card]
            value_count += value
        return value_count
    def calc_player_hand(self):
        # TODO: What about an Ace, when to count it as 1 or 11
        value_count = 0
        for card in self.player_cards:
            value = card_values_dict[card]
            value_count += value
        return value_count

    def check_bust_player(self):
        player_hand_value = self.calc_player_hand()
        if player_hand_value > 21:
            raise ValueError("Player busted, value:", player_hand_value)
    def check_bust_dealer(self):
        dealer_hand_value = self.calc_dealer_hand()
        if dealer_hand_value > 21:
            raise ValueError("dealer busted, value:", dealer_hand_value)

    def check_win(self):
        dealer_hand_value = self.calc_dealer_hand()
        player_hand_value = self.calc_player_hand()
        if player_hand_value > 21:
            print("Dealer wins, player busted with hand:", self.player_cards, "total:", player_hand_value)
        elif dealer_hand_value > 21:
            print("Player wins, dealer busted with hand:", self.dealer_cards, "total:", dealer_hand_value)
        elif player_hand_value > dealer_hand_value:
            print("Player wins", self.player_cards, "total:", player_hand_value)
        elif player_hand_value == dealer_hand_value:
            print("It's a draw", self.player_cards, "total:", player_hand_value)
        elif player_hand_value < dealer_hand_value:
            print("Dealer wins", self.player_cards, "total:", player_hand_value)
        else:
            print("Unkown error in check_win()", self.player_cards, "total:", player_hand_value)

    def player_actions(self):
        while True:
            self.print_state()

            # Player decides whether hit or not
            player_wants_to_hit = input("'h' or ''")
            if player_wants_to_hit not in ["h", ""]:
                print("Wrong input...")
            if player_wants_to_hit == "h":
                self.hit_player()
            else:
                return

            self.check_bust_player()

    def dealer_actions(self):
        while True:
            if self.calc_dealer_hand() >= 17:
                return

            self.hit_dealer()
            self.check_bust_dealer()


    def game_loop(self):
        try: # Because an error is thrown when busting 
            self.player_actions()
            self.dealer_actions()
        except:
            pass

        self.print_state()
        self.check_win()



game = BlackJack()
game.start_play()