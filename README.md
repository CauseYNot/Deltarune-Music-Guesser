# Deltarune Music Guesser
A discord quiz bot coded for the Deltarune Chapter 1 & 2 Soundtrack.
### Commands:
- `/start_quiz [channel] [rounds]`: Starts a quiz in `channel` for however many rounds specified. Players are everybody in the voice channel
- `/guess [guess]`: Used to guess while playing (cannot be used while not in quiz). Options will come up for songs in soundtrack.

### Game Structure
A quiz is started with `/start_quiz` specifying the voice channel to join and the number of rounds to play.
Each round, the bot will play a song in the voice channel and you have as much time as you want to guess using `/guess`.
Every time you guess, the bot will respond with either 'Correct!' or 'Incorrect!'.
Once all players have guessed, the song is revealed and the next song plays.
Once all the rounds have been played, the bot will send an embed showing scores and guesses for each player.

### Notes
Add to your server here: ||will insert link later||
