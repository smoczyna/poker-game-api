#! /usr/bin/python
#encoding: UTF-8

from model.game import Game

print ("*** This is the free Poker Game ***")

#print ("Give a number of players or their names separated by space:")
#strInput = raw_input()
#try:
#    playersNo = int(strInput)
#except ValueError:
#    print("Can't recognize neither a number of players nor their names")

game = Game()
players = {"HandNo1": game.add_hand("HandNo1"),
           "HandNo2": game.add_hand("HandNo2"),
           "HandNo3": game.add_hand("HandNo3")}

game.serve_all_hands()
game.print_hands()
print("*** Card exchange phase ***")

for name in game.hands.keys():    
    print ("Hand: " + name + " call")
    hand = game.hands[name]
    # get input from user console
    strInput = input()
    inputList = strInput.split()
    inputList = [int(a) for a in inputList]
    # validate input first
    for i in inputList:
        if i<1 or i>5:
            isOK = False
        else:
            isOK = True
            
    if isOK:
        # decrement inputs for list consumption as index starts from 0
        inputList[:]=[i-1 for i in inputList]
        game.replace_cards(hand.name, inputList)
    else:
        print("Incorrect card index found, you lost your chance for the exchange")
        
    s = hand.evaluate()
    print ("Hand resolved to: ", s)
    hand.pretty_print(True)
    print("***")    
    players[name] = s
    
print(" ")
print("*** End of card exchange ***")
print(" ")
game.resolve()
print("Show Hands: ")
for k, v in players.items():
    hand = game.results[k]
    print(f"{k} hand value is: [{hand[0]}:{hand[1]}]")

print ("The winner is: " + game.winner[0] + " !!!")

# if __name__ == '__main__':
#     unittest.main()