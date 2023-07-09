import random

class GamePlay:

    # initialize essential elements of a gameplay: players, deck, card points, etc
    def __init__(self, deck_content, initial_number_of_card, winning_points):

        self.finish = False
        self.player_cards = []
        self.dealer_cards = []
        self.player_card_points = 0
        self.dealer_card_points = 0
        self.player_card_usable_ace = 0;
        self.dealer_first_card_point = 0;

        # describe what cards are contained in the deck
        self.deck_content = deck_content[:]

        # randomly shuffle the deck
        self.shuffle_deck()

        # player draw #initialNumberOfCard cards
        for i in range (initial_number_of_card):
            self.player_cards.append(self.draw_a_card())

        # dealer draw #initialNumberOfCard cards
        for i in range (initial_number_of_card):
            self.dealer_cards.append(self.draw_a_card())
            if (i == 0):
                self.dealer_first_card_point = self.calculate_dealer_first_card_point (self.dealer_cards)

        # calculate total points from the card
        self.player_card_points, self.player_card_usable_ace = self.calculate_card_points (self.player_cards, winning_points)
        self.dealer_card_points, dummy = self.calculate_card_points (self.dealer_cards, winning_points)

    # Randomize the order of the cards in the deck
    def shuffle_deck (self):
        random.shuffle(self.deck_content)

    # draw the toppest card (index 0), remove the drawn card from the deck
    def draw_a_card (self):
        return self.deck_content.pop(0)

    # given dealer first card point
    def calculate_dealer_first_card_point(self, cards):
        # if  card is '2' to '10'
        if cards[0].isdigit():
            return int(cards[0])
        # if card is 'A'
        elif cards[0] == 'A':
            return 1
        # if card is J, Q or K
        else:
            return 10

    # given the player cards, calculate the total points
    def calculate_card_points(self, cards, winning_points):
        points = 0
        ace_quantity = 0
        usable_ace = 0
        for card in cards:
            # if  card is '2' to '10'
            if card.isdigit():
                points += int(card)
            # if card is 'A', assume first an ace worth 11 points, reduce it to 1 point if the total points > winningPoints
            elif card == 'A':
                points += 11
                ace_quantity += 1
            # if card is J, Q or K
            else:
                points += 10
        # adjust the total points if has aces and points > winningPoints
        while ace_quantity > 0 and points > winning_points:
            ace_quantity -= 1
            points -= 10

        # check if there is usable ace
        if (ace_quantity > 0):
            usable_ace = 1

        return points, usable_ace

    # game proceed by the player's action
    def game_proceed(self, gameplay, action, winning_points, dealer_critical_points_to_stick):

        reward = None
        player_card_points = gameplay.player_card_points
        dealer_card_points = gameplay.dealer_card_points
        player_card_usable_ace = gameplay.player_card_usable_ace

        # if player chooses to hit
        if (action == 0):
            gameplay.player_cards.append(gameplay.draw_a_card())
            player_card_points, player_card_usable_ace = gameplay.calculate_card_points(gameplay.player_cards, winning_points)

            if (player_card_points) > winning_points:
                reward = -1
        # if player chooses to stick, then dealer's turn to draw card
        else:
            # dealer only sticks hen his points >= dealerCriticalPointsToStick
            while dealer_card_points < dealer_critical_points_to_stick:
                gameplay.dealer_cards.append(gameplay.draw_a_card())
                dealer_card_points, dummy = gameplay.calculate_card_points(gameplay.dealer_cards, winning_points)

            # when both player and dealer choose to stick, determine which one is winner
            if dealer_card_points > winning_points:
                reward = 1
            else:
                if player_card_points <= winning_points:
                    if player_card_points < dealer_card_points:
                        reward = -1
                    elif player_card_points == dealer_card_points:
                        reward = 0
                    elif player_card_points > dealer_card_points:
                        reward = 1

        return player_card_points, dealer_card_points, player_card_usable_ace, reward

