# Speech-Chess
This python chess code is taken from http://www.pygame.org/project/1099/1990

## Description
From the python chess game I added the ability to give voice commands to the game. You can speak to select a piece, and you can speak to move the selected piece.

I was able to do this by using a Google API to translate speech-to-text, then running the text through the LUIS API and selecting out key
words to better understand what the user's motive was, and then finally I'd take these motives and have them reflect back into the game.
There were two commands I looked for through the LUIS API: the first is a selecting a piece, and the second is moving that piece to which
specific location.
ex.
"Pick Pawn 3" Would prompt the third pawn from the left and highlight its move set.
"Move Pawn 3 to C5" Would then move the piece to the correct location on the chessboard.
