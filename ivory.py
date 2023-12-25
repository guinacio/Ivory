import streamlit as st
import pandas as pd
import random
from PIL import Image
from datetime import datetime
import time

scoreboard_path = 'initial_scoreboard.txt'

@st.cache_resource
def initialize_scores():
    if 'scores' not in st.session_state:
        st.session_state['scores'] = {}

        with open(scoreboard_path, 'r') as file:
            for line in file:
                columns = line.strip().split()
                player_name, score, date, time = columns
                game_time_str = f'{date} {time}'
                game_time = datetime.strptime(game_time_str, "%d/%m/%Y %H:%M")
                game_id = f'{player_name} - {game_time.strftime("%d/%m/%y %H:%M")}'
                st.session_state['scores'][game_id] = int(score)
    return st.session_state['scores']

def update_leaderboard(user_scores, game_id, score):
    user_scores[game_id] = score

def show_leaderboard(user_scores,tabLeaderboard):
    with tabLeaderboard:
        if not user_scores:
            st.warning('No user scores at the moment.')
        else:
            sorted_scores = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)
            for i, (user, user_score) in enumerate(sorted_scores, start=1):
                st.write(f"**{i}. {user}**: <code style='color: rgb(9, 171, 59); background: rgb(248, 249, 251); font-family: \"Source Code Pro\", monospace;'>{user_score}</code> points", unsafe_allow_html=True)

class YahtzeeGame:
    def __init__(self):
        self.dice = [0] * 5
        self.rolls_left = 4
        self.turns_left = 13
        self.selected_indices = []
        self.scores = {
            "Ones": None,
            "Twos": None,
            "Threes": None,
            "Fours": None,
            "Fives": None,
            "Sixes": None,
            "Three of a Kind": None,
            "Four of a Kind": None,
            "Full House": None,
            "Small Straight": None,
            "Large Straight": None,
            "Ivory": None,
            "Chance": None
        }
        self.max_scores = {
            "Ones": 5,
            "Twos": 10,
            "Threes": 15,
            "Fours": 20,
            "Fives": 25,
            "Sixes": 30,
            "Three of a Kind": None,
            "Four of a Kind": None,
            "Full House": 25,
            "Small Straight": 30,
            "Large Straight": 40,
            "Ivory": 50,
            "Chance": None
        }
        self.dice_label = {
            0:'A',
            1:'B',
            2:'C',
            3:'D',
            4:'E'
        }

    def roll_dice(self):
        if self.rolls_left > 0:
            if self.selected_indices:
                for i in self.selected_indices:
                    self.dice[i] = random.randint(1, 6)
            else:
                for i in range(5):
                    self.dice[i] = random.randint(1, 6)
            self.rolls_left -= 1
        else:
            st.warning("You have no rolls left! Please choose a category to compute your points.")
    
    def new_turn(self):
        self.turns_left -= 1
        self.rolls_left = 4
        self.selected_indices = []
        self.roll_dice()

    def reset_dice(self):
        self.dice = [0] * 5
        self.rolls_left = 3
        self.selected_indices = []

    def get_dice(self):
        return self.dice

    def get_rolls_left(self):
        return self.rolls_left

    def select_dice(self, index):
        if index in self.selected_indices:
            self.selected_indices.remove(index)
        else:
            self.selected_indices.append(index)

    def calculate_score(self, category):
        dice_counts = [self.dice.count(i) for i in range(1, 7)]
        dict_faces = {'Ones': 1,'Twos': 2,'Threes': 3,'Fours': 4, 'Fives': 5, 'Sixes': 6}
        if category in dict_faces:
            face_value = dict_faces[category]
            score = dice_counts[face_value - 1] * face_value
        elif category == "Three of a Kind":
            if 3 in dice_counts or 4 in dice_counts or 5 in dice_counts:
                score = sum(self.dice)
            else:
                score = 0
        elif category == "Four of a Kind":
            if 4 in dice_counts or 5 in dice_counts:
                score = sum(self.dice)
            else:
                score = 0
        elif category == "Full House":
            if 3 in dice_counts and 2 in dice_counts:
                score = 25
            else:
                score = 0
        elif category == "Small Straight":
            if dice_counts == [0, 1, 1, 1, 1, 1] or dice_counts == [1, 1, 1, 1, 1, 0]:
                score = 30
            else:
                score = 0
        elif category == "Large Straight":
            if dice_counts == [0, 1, 1, 1, 1, 1]:
                score = 40
            else:
                score = 0
        elif category == "Ivory":
            if 5 in dice_counts:
                score = 50
            else:
                score = 0
        elif category == "Chance":
            score = sum(self.dice)
        else:
            score = 0

        self.scores[category] = score

    def get_scores(self):
        return self.scores
    
    def get_total_score(self):
        total = 0
        for score in self.scores.values():
            if score == None:
                total += 0
            else:
                total += score
        return total

def display_dice(game, container):
    dice_values = game.get_dice()
    emoji_dict = {
    0: '🅾️',
    1: '1️⃣',
    2: '2️⃣',
    3: '3️⃣',
    4: '4️⃣',
    5: '5️⃣',
    6: '6️⃣'
    }

    table_data = [{"Index": game.dice_label[i],"Dice Values": emoji_dict[value]} for i, value in enumerate(dice_values)]

    table_df = pd.DataFrame(table_data)
    container.dataframe(table_df,hide_index=True)

def clear_multi():
    st.session_state.multiselect = []
    return

def display_score_summary(game, container):
    container.subheader("Score Summary")
    scores = game.get_scores()

    table_data = []
    for category, score in scores.items():
        if score is None:
            score = ' - '
        if game.max_scores[category] is None:
            max_score = 'SUM'
        else:
            max_score = game.max_scores[category]

        table_data.append({"Category": category, "Score": score, "Max Score": max_score})

    df = pd.DataFrame(table_data)

    container.dataframe(df,hide_index=True, use_container_width=True, height=493,
        column_config={
        "Category": st.column_config.TextColumn(
            "Category",
            help="🎲 Score Categories, click 'Show Rules' to view the rules."
        ),
        "Max Score": st.column_config.TextColumn(
            "Max Score",
            help="🎲 Max Scores for your game, the highest score possible is 340 🥇."
        )
        })
    with container:
        st.write("**Total Score:**", game.get_total_score())
    st.sidebar.write("**Total Score:**", game.get_total_score())

def show_help():
    st.subheader("Ivory Rules")
    st.write("Ivory is a dice game based on the popular Yahtzee game that involves rolling five dice in order to achieve specific combinations "
             "and score points. The game consists of 13 rounds, and the player should aim to achieve the highest total score at the "
             "end of all rounds. Here are the rules:")

    st.write("**1. Roll the Dice:**")
    st.write("   - At the beginning of each round, you get a roll of five dice.")
    st.write("   - You can choose to keep any number of dice and re-roll the others.")
    st.write("   - You can re-roll up to three more times during your turn.")

    st.write("**2. Scoring:**")
    st.write("   - Each round, you must choose a scoring category for your roll.")
    st.write("   - The categories include ones, twos, threes, fours, fives, sixes, three of a kind, four of a kind, "
             "full house, small straight, large straight, Ivory, and chance.")
    st.write("   - Once you've chosen a category, you cannot change it for the rest of the game.")
    st.write("   - If your roll meets the requirements of the selected category, you score points based on the "
             "combination achieved.")

    st.write("**3. Scoring Categories:**")
    st.write("   - **Ones, Twos, Threes, Fours, Fives, Sixes:** Sum of all dice that show the corresponding number.")
    st.write("   - **Three of a Kind:** Sum of all dice if there are at least three dice with the same number.")
    st.write("   - **Four of a Kind:** Sum of all dice if there are at least four dice with the same number.")
    st.write("   - **Full House:** 25 points if you have three dice of one number and two dice of another number.")
    st.write("   - **Small Straight:** 30 points if you have the sequence 1, 2, 3, 4, 5 (1-5).")
    st.write("   - **Large Straight:** 40 points if you have the sequence 2, 3, 4, 5, 6 (2-6).")
    st.write("   - **Ivory:** 50 points if you have all five dice showing the same number.")
    st.write("   - **Chance:** Sum of all dice, regardless of the combination.")

    st.write("**4. End of the Game:**")
    st.write("   - After 13 rounds, the game ends, aim to achieve the highest score and break your own record!")

def main():
    st.set_page_config(
        page_title="Ivory",
        page_icon="🎲",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    st.sidebar.title("🎲 Ivory",help='Dice game. Have fun!')

    if 'game' not in st.session_state:
        st.session_state.game = YahtzeeGame()

    user_scores = initialize_scores()
    game = st.session_state.game

    label_to_index = {label: index for index, label in game.dice_label.items()}

    selected_dice = st.sidebar.multiselect('Select Dice to Reroll:', options=list(game.dice_label.values()),default=None,help='You can select specific dice to reroll. Use the index of the dice to choose.',key='multiselect')
    game.selected_indices = [label_to_index[label] for label in selected_dice]
    
    tabGame, tabRules, tabLeaderbord = st.tabs(["🎮 Game", "📝 Rules", '🎖️ Leaderboard'])

    with tabGame:
        col1, col2 = st.columns(2)

        col1.header('Dice')
        container = col1.container()

        if st.sidebar.button("Roll Dice",use_container_width=True):
            with container:
                game.roll_dice()

        if game.get_rolls_left() == 4:
            col1.warning('Click "Roll Dice" to start playing.')

        with st.form("form_turn",clear_on_submit=True):
            with st.sidebar:
                st.sidebar.subheader("Select a category:")
                scores = game.get_scores()
                selected_category = st.sidebar.selectbox("Category", ["Select Category"] + [key for key, value in scores.items() if value is None],key='selectbox')

                submitted = st.form_submit_button("Submit", on_click=clear_multi)
                if submitted:
                    if selected_category == 'Select Category':
                        st.sidebar.warning('Please choose a category!')
                        display_dice(game,container)
                        st.stop()
                    elif game.get_scores()[selected_category] != None:
                        st.warning('Please choose a different category!')
                        display_dice(game,container)
                        st.stop()
                    else:
                        if game.max_scores[selected_category] == None:
                            game.max_scores[selected_category] = sum(game.get_dice())
                        game.calculate_score(selected_category)
                        st.success(f"Your score for {selected_category}: **{game.get_scores()[selected_category]}**")
            if submitted:
                display_score_summary(game,col2)
                game.new_turn()
            else:
                display_score_summary(game,col2)

        display_dice(game, container)
        if game.get_rolls_left() != 4:
            container.success(f"Rolls Left: **{game.get_rolls_left()}**")

        if game.turns_left == 0:
            col1.success(f'The End! Your final score is: **{game.get_total_score()}**')
            col1.balloons()
            now = datetime.now()
            time.sleep(3)
            with col1.form("form_leaderboard"):
                player_name = st.text_input('Write a nickname:', 'Player 1')
                score = game.get_total_score()
                submitted = st.form_submit_button("Submit")
                if submitted: 
                    game_time = now.strftime("%d/%m/%y %H:%M")
                    game_id = player_name + ' - ' + game_time
                    update_leaderboard(user_scores, game_id, score)
                    show_leaderboard(user_scores,tabLeaderbord)
                    col1.success(f'Your final score of: **{game.get_total_score()}** was added to the leaderboard!')
                    time.sleep(2)
                    st.session_state.game = YahtzeeGame()
                    game = st.session_state.game
                    st.rerun()
                    
    with tabRules:
        show_help()

    show_leaderboard(user_scores,tabLeaderbord)
        
if __name__ == "__main__":
    main()