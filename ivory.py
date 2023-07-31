import streamlit as st
import random
from PIL import Image

class YahtzeeGame:
    def __init__(self):
        self.dice = [0] * 5
        self.rolls_left = 4
        self.selected_indices = []
        self.scores = {
            "1": None,
            "2": None,
            "3": None,
            "4": None,
            "5": None,
            "6": None,
            "Three of a Kind": None,
            "Four of a Kind": None,
            "Full House": None,
            "Small Straight": None,
            "Large Straight": None,
            "Ivory": None,
            "Chance": None
        }
        self.max_scores = {
            "1": 5,
            "2": 10,
            "3": 15,
            "4": 20,
            "5": 25,
            "6": 30,
            "Three of a Kind": None,
            "Four of a Kind": None,
            "Full House": 25,
            "Small Straight": 30,
            "Large Straight": 40,
            "Ivory": 50,
            "Chance": None
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
        if category in ("1", "2", "3", "4", "5", "6"):
            score = dice_counts[int(category) - 1] * int(category)
        elif category == "Three of a Kind":
            if 3 in dice_counts:
                score = sum(self.dice)
            else:
                score = 0
        elif category == "Four of a Kind":
            if 4 in dice_counts:
                score = sum(self.dice)
            else:
                score = 0
        elif category == "Full House":
            if 3 in dice_counts and 2 in dice_counts:
                score = 25
            else:
                score = 0
        elif category == "Small Straight":
            if 1 in dice_counts[1:5] or 1 in dice_counts[2:6]:
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
    container.write("Dice Values:")
    dice_values = game.get_dice()

    # Create a list of dictionaries to represent the data for the table
    table_data = [{"Value": value} for i, value in enumerate(dice_values)]

    # Display the table using st.table()
    container.table(table_data)

def clear_multi():
    st.session_state.multiselect = []
    return

def display_score_summary(game, container):
    container.subheader("Score Summary")
    scores = game.get_scores()

    # Create a list of dictionaries to represent the data for the table
    table_data = []
    for category, score in scores.items():
        if score is None:
            score = ' - '
        if game.max_scores[category] is None:
            max_score = 'SUM'
        else:
            max_score = game.max_scores[category]

        table_data.append({"Category": category, "Score": score, "Max Score": max_score})

    # Display the table using st.table()
    container.table(table_data)

    st.sidebar.write("**Total Score:**", game.get_total_score())

def main():
    st.set_page_config(
        page_title="Ivory",
        page_icon="🎲",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    #image = Image.open('ivory_logo.jpeg')
    #st.sidebar.image(image)
    st.sidebar.title("🎲 Ivory",help='Dice game. Have fun!')

    if 'game' not in st.session_state:
        st.session_state.game = YahtzeeGame()

    game = st.session_state.game

    selected_dice = st.sidebar.multiselect('Select Dice to Reroll:', options=[f'{i}' for i in range(5)],default=None,help='You can select specific dice to reroll. Use the index of the dice to choose.',key='multiselect')
    game.selected_indices = list(map(int, selected_dice))

    if st.sidebar.button("Roll Dice",use_container_width=True):
        game.roll_dice()
    
    col1, col2 = st.columns(2)

    col1.header('Dice')
    container = col1.container()
    if game.get_rolls_left() == 4:
        col1.warning('Click "Roll Dice" to start playing.')

    with st.form("my_form",clear_on_submit=True):
        with st.sidebar:
            st.sidebar.subheader("Select a category:")
            selected_category = st.sidebar.selectbox("Category", ["Select Category"] + list(game.get_scores().keys()),)
            
            submitted = st.form_submit_button("Submit", on_click=clear_multi)
            if submitted:
                if selected_category == 'Select Category':
                    st.sidebar.warning('Please choose a category!')
                    display_dice(game)
                    st.stop()
                elif game.get_scores()[selected_category] != None:
                    st.warning('Please choose a different category!')
                    display_dice(game)
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

if __name__ == "__main__":
    main()