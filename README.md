# Simple Poker Game API #

This API allows users to play a simplified version of poker over the internet. 
It provides endpoints for creating games, joining games, and making moves. 
The API is designed to be easy to use and understand, with clear documentation and examples.
There is no betting functionality here, users can just play the game.

There is authentication and authorization implementation in place but itis not activated yet.
Some more stuff needs to be sorted out first.

### Useful Endpoints ###

- /api/game/all - lists all active games
- /api/game/new - creates a new game
- /api/game/{game_id}/add-player/{player_name} - joins an existing game
- /api/game/{game_id}/replace-cards - makes a move in a game
- /api/game/{game_id}/resolve - evaluates all hands and determine the winner
- /api/game/{game_id}/reveal - prints out all hands and their results

There area also:
- /api/auth/* endpoints to user authentication
- /api/user/* endpoints, but they are not play the role yet.

UI is on the way. 