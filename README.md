battleship
=

battleship, this project, a set of rest calls to play the game of Battleship

Table of contents:

* Remarks
* API details  
* Installation
* References

# Remarks
battleship currently supports Python 3.5 and higher.

# Installation (development)
* for some reason the paprika connector dependency is not installed, use the following command to install it
```
$ pip install git+https://github.com/janripke/paprika-connector.git@0.0.4
```

battleship depends on the battleship database, in the folder db 
Before you start the installation of battleship it is recommended you install the database first, see also  [database installation instructions](https://github.com/janripke/battleship/blob/main/docs/postgresql.md) first.


# Start Game
request a game id. A game ID is given when 2 players are requesting a match within the same minute.
In the request you also send the grid this reflects where you have placed your ships.  
You need to place 5 ships:

* 1x Carrier (5 holes, using id #1)
* 1x Battleship (4 holes, using id #2)
* 1x Cruiser (3 holes using id #3)
* 1x Submarine (3 holes using id #4)
* 1x Distroyer (2 holes using id #5)

The grid is reflected by a single string
"0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000" 
In human readable form this looks like this:
```html
  1 2 3 4 5 6 7 8 9 10
A 0 3 0 0 2 2 2 2 0 0
B 0 3 0 0 0 0 0 0 0 0
C 0 3 1 0 0 0 0 0 0 0
D 0 0 1 0 0 0 5 0 0 0
E 0 0 1 0 0 0 5 0 0 0
F 0 0 1 0 0 4 4 4 0 0
G 0 0 1 0 0 0 0 0 0 0
H 0 0 0 0 0 0 0 0 0 0
I 0 0 0 0 0 0 0 0 0 0
J 0 0 0 0 0 0 0 0 0 0
```

Request:
```html
POST battleship/game

{ 
  "username": "jan",
  "grid" : "0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000",
}
```
Response:
```html
{
  "game_id": "02e9e591-e35d-4ea2-839a-a85bd0190cc0"
}
```

# Check the status of the game.
After retrieving your game_id you have to check if the other player is ready.
This is realised through the status request.
This request returns the following statuses:
* pending
* active, another player joined you can start the game
* dropped, your game is dropped by you or the other player.

Request:
```html
GET battleship/status?game_id=02e9e591-e35d-4ea2-839a-a85bd0190cc0
```
Response:
```html
{
  "status": "active"
}
```

# Fire a shot
When your game is active, the other player joined, you can start firing shots.
This is realised by using the shot request.

Request:
```html
POST battleship/shot

{ 
  "game_id": "",
  "username": "jan"
  "shot": {
    "row": "2",
    "col": "2"
  }
}
```

Response:
```html
{
  "status": "active",
  "result": "hit/miss/twice"
}
```
When the game is ended, there is a winner te following is shown:

```html
{
  "status": "ended",
  "winner": "kees"
}
```



# Limitations
* No authentication is required, other then your username
* usernames are not checked, if you use a username which is already used you could end-up in a different game. 
  In that case it is bad luck. 
* To make the battleship rest server more easy to run, the datasource file battleship-ds.json is in the package, this is not secure.  
* The grid is not check on having all the ships placed according to the game rules.
* The shot is not validated in using the correct format, and or if the given shot is valid
* If you know the other username you could tweak being the other user.
* Not all scenarios are tested, for example ending the game
* The status request does not show the winner when a game is ended
* The json configuration files are not part of the setup.py, so installation through pip fails. When you have an IDE like intellij/pycharm it works.

# Testing
Some test can be found in the module test_rest in the tests folder.
It contains 10 tests, so the test coverage is limited.


# References
* https://github.com/restgames/battleship-client
* https://www.hasbro.com/common/instruct/Battleship.PDF




