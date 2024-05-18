# Ivory - Yahtzee-based Dice Game

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ivorydice.streamlit.app)

🎲 **Ivory** is a dice game based on the popular Yahtzee game. Roll the dice, aim for specific combinations, and score points to achieve the highest total score at the end of all rounds.

**Please note that Ivory is still in development and may have bugs or incomplete features.**

## How to Play

1. **Roll the Dice:**
   - At the beginning of each round, you get a roll of five dice.
   - You can choose to keep any number of dice and re-roll the others.
   - You can re-roll up to three more times during your turn.

2. **Scoring:**
   - Each round, you must choose a scoring category for your roll.
   - The categories include ones, twos, threes, fours, fives, sixes, three of a kind, four of a kind, full house, small straight, large straight, Ivory, and chance.
   - Once you've chosen a category, you cannot change it for the rest of the game.
   - If your roll meets the requirements of the selected category, you score points based on the combination achieved.

3. **Scoring Categories:**
   - **Ones, Twos, Threes, Fours, Fives, Sixes:** Sum of all dice that show the corresponding number.
   - **Three of a Kind:** Sum of all dice if there are at least three dice with the same number.
   - **Four of a Kind:** Sum of all dice if there are at least four dice with the same number.
   - **Full House:** 25 points if you have three dice of one number and two dice of another number.
   - **Small Straight:** 30 points if you have the sequence 1, 2, 3, 4, 5 (1-5).
   - **Large Straight:** 40 points if you have the sequence 2, 3, 4, 5, 6 (2-6).
   - **Ivory:** 50 points if you have all five dice showing the same number.
   - **Chance:** Sum of all dice, regardless of the combination.

4. **End of the Game:**
   - After 13 rounds, the game ends, aim to achieve the highest score and break your own record!

## Play the Game

You can play the game by visiting [Ivory](https://ivorydice.streamlit.app).

![Current Inteface](https://github.com/guinacio/Ivory/assets/2325925/7238a331-b898-4d40-bbcf-62af361ef84f)

## Development

This game is still in development. You are welcome to contribute, report bugs, or suggest improvements. To set up the development environment, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/guinacio/Ivory.git
cd Ivory
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

4. Run the game locally:
```
streamlit run ivory.py
```

## Feedback and Contributions
Your feedback is valuable! If you encounter any issues or have suggestions for improvements, please create an issue on GitHub.

If you'd like to contribute to the project, feel free to open a pull request. We welcome contributions from the community!
