import pandas as pd
import random
from itertools import combinations
import streamlit as st

# Setting the page title and subtitle (mode selection)
st.title(":cup_with_straw: The Destined Pour")
# st.header("Select the generator mode you want!")
st.markdown("""
<h1 style='font-size: 28px; font-weight: 600; margin-bottom: 16px;'>
    Select the generator mode you want!
</h1>
""", unsafe_allow_html=True)

# "Initialization" Part1

# st.session_state is used to remember what has happened, for Streamlit resets states when there is new interaction
# So, we need to use st.session_state to keep and update status throughout consecutive events.

# Resetting three variables and st.session_state about mode customization. # Default: "no customization"
if 'calories_customized' not in st.session_state:
    option_calories = 'NO'
    st.session_state['calories_customized'] = 'NO'
if 'price_customized' not in st.session_state:
    option_price = 'NO'
    st.session_state['price_customized'] = 'NO'
if 'ingredient_customized' not in st.session_state:
    option_ingredient = 'NO'
    st.session_state['ingredient_customized'] = 'NO'

# Resetting variable and st.session_state about calories (slider/type)
calorie_target = "無" # -> Means no limit, will be random
if "calories_value" not in st.session_state:
    st.session_state['calories_value'] = 500 # Default value if customized


# Resetting variable and st.session_state about prices (slider/type)
price_target = "無" # -> Means no limit, will be random
if "price_value" not in st.session_state:
    st.session_state['price_value'] = 70 # Default value if customized

# Resetting st.session_state for tastes and toppings
selected_type = ["Topping", "Taste", "Texture"] # Default: "all selected"
if 'selected_type' not in st.session_state: # Resetting segmented_control
    st.session_state['selected_type'] = ["Topping", "Taste", "Texture"] # Default: "all selected"
whether_to_add_topping = ":rainbow[YES]" # Default: "YES" for topping
if 'add_topping' not in st.session_state:
    st.session_state['add_topping'] = ":rainbow[YES]" # Default: "YES" for topping

# if 'selected_topping' not in st.session_state:
#     st.session_state['selected_topping'] = ["焙烏龍茶凍 Oolong Tea Jelly"]
if 'topping_number_max' not in st.session_state:
    st.session_state['topping_number_max'] = 1
if 'random_topping_number' not in st.session_state:
    st.session_state['random_topping_number'] = "無" # -> Means no limit, will be random
topping_set = [] # Feature for customizing toppings is removed for now, so this is an empty list.

if 'selected_taste' not in st.session_state:
    st.session_state['selected_taste'] = [] # Default: "empty list"
if 'random_taste' not in st.session_state:
    st.session_state['random_taste'] = "無" # -> Means no limit, will be random
if 'selected_taste_display' not in st.session_state:
    st.session_state['selected_taste_display'] = [] # Default: "empty list"

if 'selected_texture' not in st.session_state:
    st.session_state['selected_texture'] = [] # Default: "empty list"
if 'selected_texture_display' not in st.session_state:
    st.session_state['selected_texture_display'] = [] # Default: "empty list"
if 'random_texture' not in st.session_state:
    st.session_state['random_texture'] = "不限" # -> "不限(Unlimited)"  means no limit, will be random; while "無(None)" means the desired texture is none.

invalid_texture = "" # Default is "", meaning the check button has not been clicked yet, will be determined later.
if 'invalid_texture' not in st.session_state:
    st.session_state['invalid_texture'] = "" # Default is "", meaning the check button has not been clicked yet

full_random = False # Default is False, will be determined later
if 'full_random' not in st.session_state:
    st.session_state['full_random'] = False

submitted_check_status = False # Default is button not clicked (but "full random" is dealed with seperately)
if 'submitted_check_status' not in st.session_state:
    st.session_state['submitted_check_status'] = False # Default is button not clicked ("full random" is dealed with seperately)

check_reminder_status = "NO"
if 'check_reminder_status' not in st.session_state:
    st.session_state['check_reminder_status'] = "NO" # Default is "", meaning the check button has not been clicked yet (the passed ones will be marked "success")

generator_section = False
if 'generator_section' not in st.session_state:
    st.session_state['generator_section'] = False

# Defining the switch function to customize calories
def calories_on_change():
    st.session_state['calories_customized'] = st.session_state["calories_temp"]
    return None

# Setting the options for the calories mode
option_calories = st.radio(
    ":one: Do you want to customize the “calories” of your drinks?",
    [":rainbow[YES]", "NO",],
    key="calories_temp",
    index=1,
    on_change=calories_on_change,
    horizontal=True,
)

# Defining the switch function to customize prices
def price_on_change():
    st.session_state['price_customized'] = st.session_state["price_temp"]
    return None

# Setting the options for the price mode
option_price = st.radio(
    ":two: Do you want to customize the “price” of your drinks?",
    [":rainbow[YES]", "NO",],
    key="price_temp",
    index=1,
    on_change=price_on_change,
    horizontal=True,
)

# Defining the switch function to customize ingredients
def ingredient_on_change():
    st.session_state['ingredient_customized'] = st.session_state["ingredient_temp"]
    return None

# Setting the options for the ingredient mode
option_ingredient = st.radio(
    ":three: Do you want to customize the “ingredient” of your drinks?",
    [":rainbow[YES]", "NO",],
    key="ingredient_temp",
    index=1,
    on_change=ingredient_on_change,
    horizontal=True,
)

# Setting the badges representing the 3 customization modes
if st.session_state['calories_customized'] != 'NO':
    badge_calories = ':orange-badge[Calories]'
else:
        badge_calories = ''

if st.session_state['price_customized'] != 'NO':
    badge_price = ':green-badge[Price]'
else:
        badge_price = ''

if st.session_state['ingredient_customized'] != 'NO':
    badge_ingredient = ':blue-badge[Ingredient]'
else:
        badge_ingredient = ''


# Using markdown and badge to display the mode selected
if st.session_state['calories_customized'] == 'NO' and st.session_state['price_customized'] == 'NO' and st.session_state['ingredient_customized'] == 'NO':
    st.markdown("✔️ You selected: :violet-badge[Random generator]")
    full_random = True
    st.session_state['full_random'] = full_random
else:
    st.markdown("✔️ You selected: " + badge_calories + badge_price + badge_ingredient)
    full_random = False
    st.session_state['full_random'] = full_random

# --- option_calories (start) ---
# calories_value is the final value, while calories_slider_value and calories_number_value represent values coming from different input modes.
# The 2 functions below are to synchronize values from the 2 input methods
def update_from_calories_slider():
    st.session_state["calories_value"] = st.session_state["calories_slider_value"]
def update_from_calories_number():
    st.session_state["calories_value"] = st.session_state["calories_number_value"]

if option_calories == "NO": # If choose not to customize calories -> Set calorie_target to "無"(Unlimited)
    calorie_target = "無"

if option_calories != "NO":
    st.divider()
    st.markdown("<p style='font-size:20px; color:DarkMagenta; font-weight:bold;'>1️⃣ Setting Target Calories for Your Drink</p>", unsafe_allow_html=True)

    col_calories_slider, col_calories_numberinput = st.columns([6, 1]) # A set of columns, the wide one on the left is for the slider, the narrow one on the right is for number_input.

    with col_calories_slider: # Setting the left column
        st.slider(
            "calories_slider",
            min_value=0,
            max_value=2000,
            key="calories_slider_value",
            value=st.session_state["calories_value"],
            on_change=update_from_calories_slider,
            label_visibility = "collapsed",
        )

    with col_calories_numberinput: # Setting the right column
        st.number_input(
            "calories_numberinput",
            min_value=0,
            max_value=2000,
            key="calories_number_value",
            value=st.session_state["calories_value"],
            on_change=update_from_calories_number,
            label_visibility = "collapsed",
        )

    calorie_target = st.session_state["calories_value"]
    st.markdown(f"""
    Your target calorie count for your drink is <span style='color: SlateBlue; font-weight: bold;'>{calorie_target}</span> calories.
    """, unsafe_allow_html=True)

# --- option_calories (end) ---

# --- option_price (start) ---
# price_value is the final value, whil eprice_slider_value and price_number_value represent values coming from different input modes.
# The 2 functions below are to synchronize values from the 2 input methods
def update_from_price_slider():
    st.session_state["price_value"] = st.session_state["price_slider_value"]
def update_from_price_number():
    st.session_state["price_value"] = st.session_state["price_number_value"]

if option_price == 'NO': # If choose not to customize price -> Set price_target to "無"(Unlimited)
    price_target = "無"

if option_price != 'NO':
    st.divider()
    st.markdown("<p style='font-size:20px; color:DarkMagenta; font-weight:bold;'>2️⃣ Setting Your Budget</p>", unsafe_allow_html=True)

    col_price_slider, col_price_numberinput = st.columns([6, 1]) # A set of columns, the wide one on the left is for the slider, the narrow one on the right is for number_input.

    with col_price_slider: # Setting the left column
        st.slider(
            "price_slider",
            min_value=0,
            max_value=1000,
            key="price_slider_value",
            value=st.session_state["price_value"],
            on_change=update_from_price_slider,
            label_visibility = "collapsed",
        )

    with col_price_numberinput: # Setting the right column
        st.number_input(
            "price_numberinput",
            min_value=0,
            max_value=1000,
            key="price_number_value",
            value=st.session_state["price_value"],
            on_change=update_from_price_number,
            label_visibility = "collapsed",
        )

    price_target = st.session_state["price_value"]
    st.markdown(f"""
    Your budget is <span style='color: SlateBlue; font-weight: bold;'>{price_target}</span> dollars.
    """, unsafe_allow_html=True)

# --- option_price (end) ---

# --- option_ingredient (start) ---
def update_customization_selection(): # Setting the session_state to update selected_type
    st.session_state['selected_type'] = st.session_state['customized_selection']
def update_whether_to_add_topping():
    st.session_state['whether_to_add_topping'] = st.session_state['add_topping']

# def update_topping_selection(): # Setting the session_state to update topping
#     st.session_state.selected_topping = st.session_state.temp_topping_selection
def update_topping_number_max(): # Setting the session_state to update topping
    st.session_state['topping_number_max'] = st.session_state['temp_topping_number_max']

def update_taste_selection(): # Setting the session_state to update taste
    st.session_state['selected_taste'] = st.session_state['temp_taste_selection']
def update_texture_selection(): # Setting the session_state to update texture
    st.session_state['selected_texture'] = st.session_state['temp_texture_selection']

# The customizable ingredients are ["Topping", "Taste", "Texture"]
# topping = ["檸檬 Lemon", "香橙 Orange", "甘蔗 Sugar cane", "春梅 Green Plum", "柚子 Yuzu/Pomelo", "珍珠 Golden Bubble/Pearl", "焙烏龍茶凍 Oolong Tea Jelly"]
taste = ["清爽回甘 Refreshing & Sweet Tea Flavor", "醇濃茶香 Mellow Tea Flavor", "酸 Sour", "甜 Sweet", "酸甜 Sweet & Sour", "奶香 Milky Flavor",]
texture = ["果粒 Fruitiness", "濃厚 Thick", "嚼感 Chewiness",]

if option_ingredient == 'NO':
    random_topping_number = "無"
    st.session_state['random_topping_number'] = random_topping_number
    random_taste = "無"
    st.session_state['random_taste'] = random_taste
    random_texture = "不限"
    st.session_state['random_texture'] = random_texture
    invalid_texture = False
    st.session_state['invalid_texture'] = invalid_texture
    submitted_check_status = False
    st.session_state['submitted_check_status'] = submitted_check_status
    check_reminder_status = "success_3" # -> Treated as if all textures are selected
    st.session_state['check_reminder_status'] = check_reminder_status

# Choosing the type of ingredients to customize ["Topping", "Taste", "Texture"]
if option_ingredient != 'NO':
    with st.container(border=False,):
        # Title
        st.markdown("<p style='margin-bottom: 0px; font-size:20px; color:DarkMagenta; font-weight:bold;'>3️⃣ Customize Your Ingredients</p>", unsafe_allow_html=True)
        # Subtitle
        st.markdown("<p style='margin-bottom: 0px; font-size:16px; color:DarkMagenta; font-weight:bold;'>Select the type you want to customize.</p>", unsafe_allow_html=True)

    # Setting the segmented_control for selecting the type of ingredient to customize (Default: all of the above)
        type_customization = ["Topping Number", "Taste", "Texture"]
        selected_type = st.segmented_control(
            "Select the type you want to customize",
            type_customization,
            default=["Topping Number", "Taste", "Texture"],
            selection_mode="multi",
            key="customized_selection",
            on_change=update_customization_selection,
            label_visibility = "collapsed",
        )

if option_ingredient != 'NO':
    st.divider()
    if "Topping Number" not in selected_type:
        random_topping_number = "無"
        st.session_state['random_topping_number'] = random_topping_number
    if "Taste" not in selected_type:
        random_taste = "無"
        st.session_state['random_taste'] = random_taste
    if "Texture" not in selected_type:
        random_texture = "不限"
        st.session_state['random_texture'] = random_texture
        invalid_texture = False
        st.session_state['invalid_texture'] = invalid_texture
        submitted_check_status = False
        st.session_state['submitted_check_status'] = submitted_check_status
        check_reminder_status = "success_3" # Treated as if all textures are selected
        st.session_state['check_reminder_status'] = check_reminder_status

# Topping
if option_ingredient != 'NO' and "Topping Number" in selected_type:
    with st.container(border=True,):
        st.markdown("<p style='margin-bottom: 0px; font-size:16px; color:DarkSlateBlue; font-weight:bold;'> ① Customize Your Topping</p>", unsafe_allow_html=True)

        # Choosing whether to add toppings (False -> topping_number_max = 0)
        st.markdown("<p margin-bottom: 0px; style='font-size:14px; color:DarkSlateBlue; font-weight:bold;'>Select whether you want to add topping to your drink or not.</p>", unsafe_allow_html=True)
        whether_to_add_topping = st.radio(
            "Select whether you want to add topping to your drink or not.",
            [":rainbow[YES]", "NO",],
            index=0,
            key="add_topping",
            on_change=update_whether_to_add_topping,
            horizontal=True,
            label_visibility="collapsed",
        )

        if whether_to_add_topping=='NO':
            topping_number_max = 0
            random_topping_number = 0

        if whether_to_add_topping!="NO": # In the case the user choose to add toppings
            # Setting the upper limit to the number of toppings added (to be confirmed later, according to the range of toppings selected)
            st.markdown("<p style='margin-bottom: 0px; font-size:14px; color:DarkSlateBlue; font-weight:bold;'>Select the maximum number of topping you want (number between 1-5). </p>", unsafe_allow_html=True)
            st.markdown("<p style='margin-bottom: 4px; font-size:12px; color:DarkGray; font-weight:bold;'>◇ We will select a number from 1 to the number you have set as the number of toppings to add.</p>", unsafe_allow_html=True)

            topping_number_max = st.number_input(
                "Select the maximum number of topping you want",
                min_value=1,
                max_value=5,
                key="temp_topping_number_max",
                value=1,
                on_change=update_topping_number_max,
                label_visibility = "collapsed",
            )
            random_topping_number = random.randint(1,int(topping_number_max))

        st.markdown("➡️ The number of toppings on your drink is " + str(random_topping_number) + ".")


# Taste
if option_ingredient != 'NO' and "Taste" in selected_type:
    with st.container(border=True,):
        st.markdown("<p style='margin-bottom: 0px; font-size:16px; color:DarkSlateBlue; font-weight:bold;'> ② Select the taste of the drink you prefer</p>", unsafe_allow_html=True)
        st.markdown("<p style='margin-bottom: 0px; font-size:12px; color:DarkGray; font-weight:bold;'>◇ If no option is selected, it is considered a full selection. </p>", unsafe_allow_html=True)
        st.markdown("<p style='margin-bottom: 4px; font-size:12px; color:DarkGray; font-weight:bold;'>◇ We will randomly select a taste of your selection to be used as a reference for the generator. </p>", unsafe_allow_html=True)

        selected_taste = st.pills(
            "Select the taste of the drink you prefer",
            taste,
            selection_mode="multi",
            key="temp_taste_selection",
            on_change=update_taste_selection,
            label_visibility = "collapsed",
            )

        # Displaying all items selected by user, while only choosing one randomly to feed to the generator
        random_taste = ""
        selected_taste_display = ""

        if len(selected_taste)>0:
            random_taste = random.choice(selected_taste) # Choosing one item from the item(s) selected by user
            st.session_state['random_taste'] = random_taste

            for i in range((len(selected_taste)-1)): # Setting the options to display on the page
                selected_taste_display = selected_taste_display + str(selected_taste[i]) + ', '
            selected_taste_display = selected_taste_display + str(selected_taste[-1])

            st.session_state['selected_taste_display'] = selected_taste_display
            st.markdown("➡️ Your selected taste: " + selected_taste_display + ".")
        else: # non-selected is viewed as all-selected -> will randomize out of all options
            random_taste = random.choice(taste)
            selected_taste_display = ""

            st.session_state['random_taste'] = random_taste
            st.session_state['selected_taste_display'] = selected_taste_display
            st.markdown("➡️ You'll get random taste of drinks!")

# Texture
if option_ingredient != 'NO' and "Texture" in selected_type:
    # submitted_check_status = False
    # st.session_state['submitted_check_status'] = False
    # check_reminder_status = ""
    # st.session_state['check_reminder_status'] = check_reminder_status

    with st.container(border=True,):
        st.markdown("<p style='margin-bottom: 0px; font-size:16px; color:DarkSlateBlue; font-weight:bold;'> ③ Select the texture of the drink you prefer</p>", unsafe_allow_html=True)
        st.markdown("<p style='margin-bottom: 0px; font-size:12px; color:DarkGray; font-weight:bold;'>◇ We will randomly select a texture of your selection to be used as a reference for the generator.</p>", unsafe_allow_html=True)
        st.markdown("<p style='margin-bottom: 0px; font-size:12px; color:DarkGray; font-weight:bold;'>◇ If you want to get random texture drinks, turn off texture customization above or select the option entirely.</p>", unsafe_allow_html=True)
        st.markdown("<p style='margin-bottom: 4px; font-size:12px; color:DarkGray; font-weight:bold;'>◇ If you don't choose any of them, you'll get a drink with no specific texture property.</p>", unsafe_allow_html=True)

        selected_texture= st.pills(
            "Select the texture of the drink you prefer",
            texture,
            selection_mode="multi",
            key="temp_texture_selection",
            on_change=update_texture_selection,
            label_visibility = "collapsed",
            )

    # Defining "random_texture_and_check": pop out a warning message when selected options contradict each other
    # When choosing not to add toppings, random_topping_number==0, so we can simply use random_topping_number (instead of bool of whether to add toppings)
    def random_texture_and_check(random_topping_number, selected_texture):
        # Checking whether user selected "no toppings" while selecting "Fruitiness" or "Chewiness" texture
        # Pop out a reminder later, if user made contradicting choices
        # When the check is passed, a texture is randomly chosen, and the selected_texture_display is set
        # When the check is not passed, random_texture = "", selected_texture_display = ""
        random_texture = ""
        invalid_texture = False
        selected_texture_display = ""
        check_reminder_status = "NO"

        if random_topping_number==0 and selected_texture in ["果粒 Fruitiness", "嚼感 Chewiness"]:
            invalid_texture = True
            check_reminder_status = "warning"
            # Setting all values related to texture as "warning" for the convenience of debugging
            random_texture = "warning"
            selected_texture_display = "warning"
        else:
            invalid_texture = False

        if invalid_texture==False: # The check is passed
            if len(selected_texture)==0: # No texture is selected -> The drink's texture property must be empty
                random_texture = '無'
                selected_texture_display = '無' # -> Your drink will not have a specific texture property.
                check_reminder_status = "success_0"

            if len(selected_texture) > 0:
                random_texture = random.choice(selected_texture) # Choosing one item from the item(s) selected by user

                for i in range((len(selected_texture)-1)): # Setting the options to display on the page
                    selected_texture_display = selected_texture_display + str(selected_texture[i]) + ', '
                selected_texture_display = selected_texture_display + str(selected_texture[-1])

                if len(selected_texture) < 3:
                    check_reminder_status = "success_12"
                if len(selected_texture) == 3:
                    check_reminder_status = "success_3"
                    random_texture = '不限'

        return random_texture, invalid_texture, selected_texture_display, check_reminder_status

    with st.form('check_and_reminder_form', clear_on_submit=False, border=True,):
        col_check_button, col_check_reminder = st.columns([1, 2])

        with col_check_button:
            submitted_check = st.form_submit_button("🔍 Check! ")

            # To display below the button
            st.markdown("<p style='margin-top: 0px; margin-bottom: 0px; font-size:12px; color:DarkGray; font-weight:bold;'>◇ Please make sure your customized combination is valid before generating. </p>", unsafe_allow_html=True)

        if submitted_check:
            submitted_check_status = True
            st.session_state['submitted_check_status'] = submitted_check_status

        if st.session_state['submitted_check_status'] == True:
            random_texture, invalid_texture, selected_texture_display, check_reminder_status = random_texture_and_check(random_topping_number, selected_texture)
            st.session_state['random_texture'] = random_texture
            st.session_state['selected_texture_display'] = selected_texture_display
            st.session_state['invalid_texture'] = invalid_texture
            st.session_state['check_reminder_status'] = check_reminder_status

        with col_check_reminder:
            if st.session_state['check_reminder_status']=="NO": # Displayed before the check button is clicked
                st.markdown("👈 Please click the check button after the selection is complete.")
            if st.session_state['check_reminder_status'] in ["success_0", "success_12", "success_3", ]: # Displayed if the texture check is passed
                st.markdown("🆗 Pass! This combination can be used. ")
            if st.session_state['check_reminder_status']=="warning": # The warning displayed if the texture check is not passed
                st.markdown("🚨 Please ensure that your selection is valid. ")

    with st.container():
        if st.session_state['check_reminder_status'] != "NO" and st.session_state['submitted_check_status'] == True:
            st.markdown(
                """
                <div style="margin-top: 0px; margin-bottom: 4px; border-left: 0.3rem solid #b19cd9; padding: 1rem; background-color: #f5f0ff; border-radius: 0.5rem; ">
                    <strong>✨ Note:</strong><br><br>
                    ◇ If you reselect the customized combination you want, press the “Check” button again before generating your drink.
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.session_state['check_reminder_status'] == "warning":
            st.markdown(
                """
                <div style="border-left: 0.3rem solid orange; padding: 1rem; background-color: #fff7e6; border-radius: 0.5rem;">
                    <strong>⚠️ Warning: </strong><br><br>
                    If you want to specify the texture of your drink as “果粒 Fruitiness” or “嚼感 Chewiness”:<br><br>

                    <u>You need to:</u><br>
                    ◇ In the <span style='color:DarkSlateBlue;'>① Customize Your Topping section</span>, <b>open</b> the option called <span style='color:DarkSlateBlue;'>“Topping number”</span>.<br>
                    ◇ Select <b>“YES”</b> in the <span style='color:DarkSlateBlue;'>“Add topping or not”</span> section.
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.session_state['check_reminder_status']=="success_0" and st.session_state['submitted_check_status'] == True:
            st.markdown(
                f"""
                <div style="border-left: 0.3rem solid green; padding: 1rem; background-color: #e6ffe6; border-radius: 0.5rem;">
                    <strong>✅ Success:</strong><br><br>
                    ➡️ You'll get a drink with no specific texture property.<br><br>
                    ◇ Everything looks good. Proceed to generate your drink!
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.session_state['check_reminder_status']=="success_12" and st.session_state['submitted_check_status'] == True:
            selected_texture_display = st.session_state['selected_texture_display']
            st.markdown(
                f"""
                <div style="border-left: 0.3rem solid green; padding: 1rem; background-color: #e6ffe6; border-radius: 0.5rem;">
                    <strong>✅ Success:</strong><br><br>
                    ➡️ Your selected texture: <b>{selected_texture_display}</b>.<br><br>
                    ◇ Everything looks good. Proceed to generate your drink!
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.session_state['check_reminder_status']=="success_3" and st.session_state['submitted_check_status'] == True:
            st.markdown(
                f"""
                <div style="border-left: 0.3rem solid green; padding: 1rem; background-color: #e6ffe6; border-radius: 0.5rem;">
                    <strong>✅ Success:</strong><br><br>
                    ➡️ You'll get random texture of drinks!<br><br>
                    ◇ Everything looks good. Proceed to generate your drink!
                </div>
                """,
                unsafe_allow_html=True
            )

# ----- [start] Settings and conversion before entering the generator -----
# Values to be passed into the generator:

# [OK] price_target should be the user's input price or a random value
# [OK] calorie_target should be the user's input calorie or a random value

# [OK] random_topping_number should be the number of toppings input by the user or a random number
# When choosing not to add toppings, random_topping_number==0 (random_topping_number=="" means not set yet -> normally, the result will be randomized)

# [OK] taste是 random_taste (1 item) (non-selected counts as all-selected, so it's always 1)
# [OK] texture是 random_texture (1 item) (non-selected means "none" while all-selected means random; "" means not set yet -> normally, the result will be randomized)

mode = "no" # Currently set as no -> the function code is written, but we haven't finished the UI
topping_num = random_topping_number

taste_preference = st.session_state['random_taste'] # Name mapping is completed
# Renaming taste ('無(None)' does not need renaming)
taste_name_generator = ['甘', '苦', '酸', '甜', '酸甜', '奶味']
taste_name_dict = dict(zip(taste, taste_name_generator))
if taste_preference in taste_name_dict:
    taste_preference = taste_name_dict[taste_preference]

texture_preference = st.session_state['random_texture'] # Name mapping is completed
# Renaming texture ('無(None)' or '不限(Unlimited)' does not need renaming)
texture_name_generator = ['果粒', '濃厚', '嚼感']
texture_name_dict = dict(zip(texture, texture_name_generator))
if texture_preference in texture_name_dict:
    texture_preference = texture_name_dict[texture_preference]

# ----- [end] Settings and conversion before entering the generator -----

# ----- [start] Code completed by withdrawn member Mr. Chan -----

# --- [start] This part of the code does not have a matching UI yet, so it's commented out ---
# valid_sex = ['男', '女']
# mode = get_text_input("Do you want customized mode (yes/no)?", valid_mode)

# if mode == 'yes':
#     sex = get_text_input("Enter your sex (男/女):", valid_sex)
#     age = get_int_input("Enter your age (0~200): ", 0, 200)
#     height = get_int_input("Enter your height in cm: ", 0, 250)
#     weight = get_int_input("Enter your weight in kg: ", 0, 250)
#     if sex == '男':
#       daily_calorie_requirement_customized = (66+13.7*weight+5*height-6.8*age)*0.2
#     else:
#       daily_calorie_requirement_customized = (655+9.6*weight+1.8*height-4.7*age)*0.2

# --- [end] This part of the code does not have a matching UI yet, so it's commented out ---

file_open = open("drink.txt", "r")
some_text = file_open.readlines()
elements = {}

for i in range(len(some_text)):
    elements[i] = some_text[i].split()

df = pd.DataFrame.from_dict(elements, orient='index')
df.columns = ['Name', 'Price_med', 'Price_big', 'Type', 'Taste', 'Texture', 'Cal_med', 'Cal_big']

df_drink = df[df['Type'] == '飲料']
df_drink = df_drink.reset_index(drop=True)

df_topping = df[df['Type'] == '加料']
df_topping = df_topping.reset_index(drop=True)

df_side = df[df['Type'] == '副飲']
df_side = df_side.reset_index(drop=True)

if calorie_target == '無':
    calorie_target = 2147483647
if price_target == '無':
    price_target = 2147483647
if topping_num == '無':
    topping_num = 2147483647


topping_set = [] # Due to designing difficulties, the topping customization feature is canceled for now, so it is set as empty list
df_filtered = df_topping[~df_topping['Name'].isin(topping_set)].reset_index(drop=True)

initial_toppings = df_topping[df_topping['Name'].isin(topping_set)]
topping_calories_initial_med = sum(int(row['Cal_med']) for _, row in initial_toppings.iterrows())
topping_price_initial_med = sum(int(row['Price_med']) for _, row in initial_toppings.iterrows())
topping_calories_initial_big = sum(int(row['Cal_big']) for _, row in initial_toppings.iterrows())
topping_price_initial_big = sum(int(row['Price_big']) for _, row in initial_toppings.iterrows())

# ----- [end] Code completed by withdrawn member Mr. Chan -----

# "Initialization" Part2
if 'dice_rolled' not in st.session_state:
    st.session_state['dice_rolled'] = False
if 'drink_combination' not in st.session_state:
    st.session_state['drink_combination'] = dict()
# if 'add_to_fav' not in st.session_state:
#     st.session_state['add_to_fav'] = False

generator_section = False
st.session_state['generator_section'] = generator_section
if check_reminder_status == "NO": # Special case: if YES was clicked and then switched to NO, st.session_state['check_reminder_status'] might not sync with check_reminder_status.
    st.session_state['check_reminder_status'] = check_reminder_status

if st.session_state['full_random']:
    generator_section = True
    st.session_state['generator_section'] = generator_section
elif st.session_state['check_reminder_status'] in ["success_0", "success_12", "success_3"]:
    generator_section = True
    st.session_state['generator_section'] = generator_section
elif st.session_state['check_reminder_status'] == "NO":
    generator_section = False
    st.session_state['generator_section'] = generator_section
elif st.session_state['check_reminder_status'] == "warning":
    generator_section = False
    st.session_state['generator_section'] = generator_section
else:
    generator_section = False
    st.session_state['generator_section'] = generator_section

# --- [start] Debug code for generator_section---
# st.write('full_random = ', full_random)
# st.write('submitted_check_status = ', submitted_check_status)
# st.write('check_reminder_status = ', check_reminder_status)
# st.write('generator_section = ', generator_section)
# st.write(st.session_state['generator_section'])

# st.write('full_random = ', st.session_state['full_random'])
# st.write('check_reminder_status = ', st.session_state['check_reminder_status'])
# st.write('type(check_reminder_status) = ', type(st.session_state['check_reminder_status']))

# --- [end] Debug code for generator_section---

# Generator access is allowed only when full_random == True or when invalid_texture check has been passed
generator_section = st.session_state['generator_section']
if generator_section == True:
    st.divider()
    with st.container():
        # st.markdown("<p style='margin-bottom: 0px; font-size:16px; color:DarkSlateBlue; font-weight:bold;'>下方皆為舊版code 正在改版</p>", unsafe_allow_html=True)
        st.markdown("""
        <h1 style='font-size: 28px; font-weight: 600; margin-bottom: 16px;'>
            Random generator
        </h1>
        """, unsafe_allow_html=True)

        # Defining the get_difference function for later use
        def get_difference(value, target):
            if target == 2147483647: # If target is not set, target == 2147483647
                return 0 # When target is not set, no need to calculate the difference
            else:
                return abs(value - int(target))

        # Setting the generating function as needed
        with st.form('generator_form', clear_on_submit=False, border=False,):
            submitted_generator = st.form_submit_button("🎲 Create your own destined pour! ")
            # 🎲 Roll the dice!

            if submitted_generator: # If the button is clicked, start generating
                # ----- [start] Code completed by withdrawn member Mr. Chan -----
                # Calculation for the combination is added on the basis of code written by Mr. Chan
                drink_conbination = []
                df_filtered = df_topping[~df_topping['Name'].isin(topping_set)].reset_index(drop=True)
                for i in range(len(df_drink)):
                    for j in range(len(df_side)+1):
                        for k in range(0, min(topping_num + 1 - len(topping_set), len(df_filtered) + 1)):
                            for combo in combinations(range(len(df_filtered)), k):
                                topping_calories = topping_calories_initial_med + sum(int(df_filtered.iloc[t]['Cal_med']) for t in combo)
                                topping_price = topping_price_initial_med + sum(int(df_filtered.iloc[t]['Price_med']) for t in combo)
                                topping_names = topping_set + [df_filtered.iloc[t]['Name'] for t in combo]
                                drink = df_drink.iloc[i]
                                side = df_side.iloc[j-1]

                                if (j == 0):
                                    total_calories = int(drink['Cal_med']) + topping_calories
                                    total_price = int(drink['Price_med']) + topping_price
                                    if (
                                    total_calories <= calorie_target and
                                    total_price <= price_target and
                                    (drink['Taste'] == taste_preference or
                                    (any(str(df_topping.iloc[t]['Taste']).strip() == taste_preference for t in combo)) or
                                    taste_preference == '無') and
                                    (drink['Texture'] == texture_preference or
                                    (any(str(df_topping.iloc[t]['Texture']).strip() == texture_preference for t in combo))
                                    or texture_preference=='不限')
                                    ):
                                        calorie_difference = get_difference(total_calories, calorie_target)
                                        price_difference = get_difference(total_price, price_target)
                                        difference_between_goals_and_results = calorie_difference + price_difference

                                        drink_conbination.append({
                                        'Drink': drink['Name'],
                                        'Size' : '中杯',
                                        'Topping': topping_names,
                                        'Side': '無',
                                        'Total Calories': total_calories,
                                        'Total Price': total_price,
                                        'Calorie Difference': calorie_difference,
                                        'Price Difference': price_difference,
                                        'Difference Score': difference_between_goals_and_results,
                                    })
                            else:
                                total_calories = int(drink['Cal_med']) + topping_calories + int(side['Cal_med'])
                                total_price = int(drink['Price_med']) + topping_price + int(side['Price_med'])
                            if (
                                total_calories <= calorie_target and
                                total_price <= price_target and
                                (drink['Taste'] == taste_preference or
                                (any(str(df_topping.iloc[t]['Taste']).strip() == taste_preference for t in combo)) or
                                side['Taste'] == taste_preference or
                                taste_preference == '無') and
                                (drink['Texture'] == texture_preference or
                                (any(str(df_topping.iloc[t]['Texture']).strip() == texture_preference for t in combo)) or
                                side['Texture'] == texture_preference or
                                texture_preference == '不限')
                            ):
                                calorie_difference = get_difference(total_calories, calorie_target)
                                price_difference = get_difference(total_price, price_target)
                                difference_between_goals_and_results = calorie_difference + price_difference

                                drink_conbination.append({
                                    'Drink': drink['Name'],
                                    'Size' : '中杯',
                                    'Topping': topping_names,
                                    'Side': side['Name'],
                                    'Total Calories': total_calories,
                                    'Total Price': total_price,
                                    'Calorie Difference': calorie_difference,
                                    'Price Difference': price_difference,
                                    'Difference Score': difference_between_goals_and_results,
                                })

                for i in range(len(df_drink)):
                    for j in range(len(df_side)+1):
                        for k in range(0, min(topping_num + 1 - len(topping_set), len(df_filtered) + 1)):
                            for combo in combinations(range(len(df_filtered)), k):
                                topping_calories = topping_calories_initial_big + sum(int(df_filtered.iloc[t]['Cal_big']) for t in combo)
                                topping_price = topping_price_initial_big + sum(int(df_filtered.iloc[t]['Price_big']) for t in combo)
                                topping_names = topping_set + [df_filtered.iloc[t]['Name'] for t in combo]
                                drink = df_drink.iloc[i]
                                side = df_side.iloc[j-1]
                                if (j == 0):
                                    total_calories = int(drink['Cal_big']) + topping_calories
                                    total_price = int(drink['Price_big']) + topping_price
                                    if (
                                    total_calories <= calorie_target and
                                    total_price <= price_target and
                                    (drink['Taste'] == taste_preference or
                                    (any(str(df_topping.iloc[t]['Taste']).strip() == taste_preference for t in combo)) or
                                    taste_preference == '無') and
                                    (drink['Texture'] == texture_preference or
                                    (any(str(df_topping.iloc[t]['Texture']).strip() == texture_preference for t in combo)) or
                                    texture_preference == '不限')
                                ):
                                        calorie_difference = get_difference(total_calories, calorie_target)
                                        price_difference = get_difference(total_price, price_target)
                                        difference_between_goals_and_results = calorie_difference + price_difference

                                        drink_conbination.append({
                                        'Drink': drink['Name'],
                                        'Size' : '大杯',
                                        'Topping': topping_names,
                                        'Side': '無',
                                        'Total Calories': total_calories,
                                        'Total Price': total_price,
                                        'Calorie Difference': calorie_difference,
                                        'Price Difference': price_difference,
                                        'Difference Score': difference_between_goals_and_results,
                                    })
                        else:
                            total_calories = int(drink['Cal_big']) + topping_calories + int(side['Cal_big'])
                            total_price = int(drink['Price_big']) + topping_price + int(side['Price_big'])
                        if (
                            total_calories <= calorie_target and
                            total_price <= price_target and
                            (drink['Taste'] == taste_preference or
                            (any(str(df_topping.iloc[t]['Taste']).strip() == taste_preference for t in combo)) or
                            side['Taste'] == taste_preference or
                            taste_preference == '無') and
                            (drink['Texture'] == texture_preference or
                            (any(str(df_topping.iloc[t]['Texture']).strip() == texture_preference for t in combo)) or
                            side['Texture'] == texture_preference or
                            texture_preference == '不限')
                        ):
                            calorie_difference = get_difference(total_calories, calorie_target)
                            price_difference = get_difference(total_price, price_target)
                            difference_between_goals_and_results = calorie_difference + price_difference

                            drink_conbination.append({
                                'Drink': drink['Name'],
                                'Size' : '大杯',
                                'Topping': topping_names,
                                'Side': side['Name'],
                                'Total Calories': total_calories,
                                'Total Price': total_price,
                                'Calorie Difference': calorie_difference,
                                'Price Difference': price_difference,
                                'Difference Score': difference_between_goals_and_results,
                            })

                # ----- [end] Code completed by withdrawn member Mr. Chan -----

                # st.write(drink_conbination) # To check whether the generator worked -> must be commented out when finished

                # Put the combinations that fit the conditions into the dataframe of pandas
                df_drink_combination = pd.DataFrame(drink_conbination)

                if drink_conbination == []: # Display "Warning" if no combination is generated
                    st.markdown(
                        """
                        <div style="border-left: 0.3rem solid orange; padding: 1rem; background-color: #fff7e6; border-radius: 0.5rem;">
                            <strong>⚠️ Warning: </strong><br><br>
                            ◇ No valid combinations found.<br>
                            ◇ If the valid combination is not generated, you can try to create it again, it is possible that the currently used parameters did not generate the result successfully.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                if drink_conbination != []: # If results are generated normally -> Display the results
                    # Sort them from lowest to highest according to Difference Score
                    df_drink_combination_sorted = df_drink_combination.sort_values('Difference Score', ascending=True).reset_index(drop=True)
                    # Calculate the Difference Score between each combination and Combination 0
                    df_drink_combination_sorted['Difference Score from Combination 0'] = df_drink_combination_sorted['Difference Score'] - df_drink_combination_sorted.iloc[0]['Difference Score']

                    chosen_drink_combination = dict() # Set chosen_drink_combination as empty dict
                    df_waiting_list = pd.DataFrame() # Set df_waiting_list as empty pd.dataframe
                    df_waiting_list2 = pd.DataFrame() # Set df_waiting_list2 as empty pd.dataframe

                    if len(df_drink_combination_sorted) == 1: # If there is only 1 combination that fits the conditions
                        # Convert the combination to dict, and put it into chosen_drink_combination
                        chosen_drink_combination = df_drink_combination_sorted.iloc[0].to_dict()

                    if len(df_drink_combination_sorted) > 1: #  If there are more than 1 combinations that fit the conditions
                        # diff1 means the value of Difference Score between the 2nd line and Combination 0
                        diff1 = df_drink_combination_sorted.iloc[1]['Difference Score from Combination 0']
                        if len(df_drink_combination_sorted) > 4: #  If there are at least 5 combinations that fit the conditions, calculate diff4
                            # diff4 means the value of Difference Score between the 5th line and Combination 0
                            diff4 = df_drink_combination_sorted.iloc[4]['Difference Score from Combination 0']

                        if diff1 > 30: # If the value of Difference Score between the 2nd line and Combination 0 > 30 -> Combination 0 is chosen_drink_combination
                            chosen_drink_combination = df_drink_combination_sorted.iloc[0].to_dict()

                        else:  # If diff1 <= 30
                            # First, find all combinations with difference scores < 31 from Combination 0
                            df_waiting_list = df_drink_combination_sorted[df_drink_combination_sorted['Difference Score from Combination 0'] < 31]
                            if df_waiting_list.shape[0] >= 5 and (diff4 == 0):
                                # If at least 5 combinations have the same scores, collect all combinations with difference scores < 1 to df_waiting_list2, then randomly select one out of them
                                df_waiting_list2 = df_drink_combination_sorted[df_drink_combination_sorted['Difference Score from Combination 0'] < 1]
                                candidates_length = len(df_waiting_list2)
                                random_candidate_loc = random.randint(0, candidates_length-1)
                                chosen_drink_combination = df_waiting_list2.iloc[random_candidate_loc].to_dict()
                                # top_candidates = df_waiting_list[df_waiting_list['Difference Score from Combination 0'] == 0]
                                # chosen_drink_combination = top_candidates.sample(1).iloc[0].to_dict()
                            elif df_waiting_list.shape[0] >= 5 and (diff4 > 0):
                                # If there are at least 5 combinations that fit the conditions, but diff4 != 0, then randomly select one out of the first 5 combinations
                                random_candidate_loc = random.randint(0, 4)
                                chosen_drink_combination = df_waiting_list.iloc[random_candidate_loc].to_dict()
                            else:
                                # If there are 2-4 combinations that fit the conditions, then randomly select one out of them
                                candidates_length = len(df_waiting_list)
                                random_candidate_loc = random.randint(0, candidates_length-1)
                                chosen_drink_combination = df_waiting_list.iloc[random_candidate_loc].to_dict()

                    st.session_state['drink_combination'] = chosen_drink_combination

                    # Rename the "drink" name of chosen_drink_combination to bilingual version
                    chosen_drink_drink_name = chosen_drink_combination['Drink']
                    converted_drink_name = ""
                    drink_name_generator = ["紅茶", "綠茶", "烏龍茶", "阿華田", "水"]
                    drink_name_display = ["紅茶 Black tea", "綠茶 Green tea", "烏龍茶 Oolong tea", "阿華田(可可) Ovaltine (Cocoa)", "水 Water"]
                    drink_name_dict = dict(zip(drink_name_generator, drink_name_display))
                    if chosen_drink_drink_name in drink_name_dict:
                        converted_drink_name = drink_name_dict[chosen_drink_drink_name]
                    chosen_drink_drink_name = converted_drink_name

                    # Rename the "size" name of chosen_drink_combination to bilingual version
                    chosen_drink_size = chosen_drink_combination['Size']
                    converted_size_name = ""
                    size_name_generator = ["中杯", "大杯"]
                    size_name_display = ["中杯 Medium", "大杯 Large"]
                    size_name_dict = dict(zip(size_name_generator, size_name_display))
                    if chosen_drink_size in size_name_dict:
                        converted_size_name = size_name_dict[chosen_drink_size]
                    chosen_drink_size = converted_size_name

                    # Rename the "side" name of chosen_drink_combination to bilingual version
                    chosen_drink_side = chosen_drink_combination['Side']
                    converted_side_name = ""
                    side_name_generator = ["優酪", "奶蓋", "奶精", "鮮奶"]
                    side_name_display = ["優酪 Yogurt", "奶蓋 Milk cap", "奶精 Creamer", "鮮奶 Fresh milk"]
                    side_name_dict = dict(zip(side_name_generator, side_name_display))
                    if chosen_drink_side in side_name_dict:
                        converted_side_name = side_name_dict[chosen_drink_side]
                    chosen_drink_side = converted_side_name

                    # Rename the "topping" name of chosen_drink_combination to bilingual version
                    chosen_drink_topping = chosen_drink_combination['Topping']
                    converted_topping_name = []
                    topping_name_generator = ['檸檬', '香橙', '甘蔗', '春梅', '柚子', '珍珠', '焙烏龍茶凍']
                    topping_name_display = ["檸檬 Lemon", "香橙 Orange", "甘蔗 Sugar cane", "春梅 Green Plum", "柚子 Yuzu/Pomelo", "珍珠 Golden Bubble/Pearl", "焙烏龍茶凍 Oolong Tea Jelly"]

                    topping_name_dict = dict(zip(topping_name_generator , topping_name_display))
                    for i in chosen_drink_topping:
                        if i in topping_name_dict: # Put the new names into converted_topping_name
                            converted_topping_name.append(topping_name_dict[i])
                        else:
                            converted_topping_name.append()
                    chosen_drink_topping = converted_topping_name # Convert the contents of chosen_drink_topping into that of converted_topping_name

                    # Setting the topping of chosen_drink_combination to display to user
                    chosen_drink_topping_display = ""
                    if len(chosen_drink_combination['Topping']) > 0:
                        for i in range((len(chosen_drink_combination['Topping'])-1)):
                            chosen_drink_topping_display = chosen_drink_topping_display + str(chosen_drink_topping[i]) + ', '
                        chosen_drink_topping_display = chosen_drink_topping_display + str(chosen_drink_topping[-1])
                    if len(chosen_drink_combination['Topping']) == 0:
                        chosen_drink_topping = 'None'

                    chosen_drink_price = chosen_drink_combination['Total Price']
                    chosen_drink_calories = chosen_drink_combination['Total Calories']

                    # Fill the generated combination into a dict
                    drink_combination_display = dict()
                    drink_combination_display = {
                        'Random Items': 'Content',
                        '飲料基底 Drink': chosen_drink_drink_name,
                        '飲料尺寸 Size': chosen_drink_size,
                        '特調配料 Side': chosen_drink_side,
                        '配料 Topping': chosen_drink_topping_display,
                    }

                    # Convert drink_combination_display into the form of pd.dataframe to save in df_drink_combination_display
                    df_drink_combination_display = pd.DataFrame(drink_combination_display, index=[0])
                    cols_display = ['飲料基底 Drink', '飲料尺寸 Size','特調配料 Side','配料 Topping']
                    df_drink_combination_display = df_drink_combination_display[cols_display]
                    # Transpose df_drink_combination_display to save in df_drink_combination_display_T
                    df_drink_combination_display_T = df_drink_combination_display.T

                    with st.container(border=True,):
                        col_destined_pour, col_generator_status = st.columns([6, 1])

                        with col_destined_pour:
                            # Change the title to gradient colored (settings inspired by chatgpt's example)
                            st.markdown(
                                """
                                <div style='
                                    margin-bottom: 4px;
                                    font-size: 24px;
                                    font-weight: bold;
                                    background: linear-gradient(90deg, #FF0000, #FF9900, #FFFF00, #33FF00, #00BFFF, #6A4C93);
                                    -webkit-background-clip: text;
                                    -webkit-text-fill-color: transparent;
                                    background-clip: text;
                                    text-fill-color: transparent;
                                    display: inline-block;
                                '>
                                    Your destined pour:
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with col_generator_status:
                            st.markdown(
                            ":green-badge[:material/check: Success]"
                            )

                        st.dataframe(df_drink_combination_display_T)
                        # ------

                        col_price, col_calories = st.columns(2) # The values can be displayed with st.metric

                        with col_price: # Price of the drink is displayed in this column
                            st.markdown(f"""
                            <p style='margin-bottom: 2px; font-size:16px;'> 💸 Price </p>
                            """, unsafe_allow_html=True
                            )
                            # <p style='margin-bottom: 2px; font-size:24px; font-weight:bold;'> {chosen_drink_price} </p>
                            st.metric(
                                "",
                                chosen_drink_price,
                                label_visibility="collapsed",
                            )

                        with col_calories: # Calorie of the drink is displayed in this column
                            st.markdown(f"""
                            <p style='margin-bottom: 2px; font-size:16px;'> 🔥 Calories </p>
                            """, unsafe_allow_html=True
                            )
                            # <p style='margin-bottom: 2px; font-size:24px; font-weight:bold;'> {chosen_drink_calories} </p>
                            st.metric(
                                "",
                                chosen_drink_calories,
                                label_visibility="collapsed",
                            )

                        st.markdown(
                            """
                            <div style="margin-top: 6px; margin-bottom: 4px; border-left: 0.3rem solid #b19cd9; padding: 1rem; background-color: #f5f0ff; border-radius: 0.5rem; ">
                                <strong>✨ Note:</strong><br><br>
                                ◇ If you want to recreate the destined pour, just click the “🎲 Create your own destined pour! ” button again.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
