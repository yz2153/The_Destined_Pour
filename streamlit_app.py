import pandas as pd
import random
from itertools import combinations
import streamlit as st

# 設定頁面的標題與副標題(模式選擇)
st.title(":cup_with_straw: The Destined Pour")
# st.header("Select the generator mode you want!")
st.markdown("""
<h1 style='font-size: 28px; font-weight: 600; margin-bottom: 16px;'>
    Select the generator mode you want!
</h1>
""", unsafe_allow_html=True)

# 初始化 Part1

# st.session_state的用途是紀錄發生過的事件，因為streamlit預設在每次按下新的互動之後，會洗去過去的事件的紀錄
# 因此在遇到有連貫性的事件時，我們需要用st.session_state紀錄並更新狀態 

# 重置三種關於模式客製化的變數和st.session_state # 預設為不客製化
if 'calories_customized' not in st.session_state:
    option_calories = 'NO' 
    st.session_state['calories_customized'] = 'NO'
if 'price_customized' not in st.session_state:
    option_price = 'NO'
    st.session_state['price_customized'] = 'NO'
if 'ingredient_customized' not in st.session_state:
    option_ingredient = 'NO'
    st.session_state['ingredient_customized'] = 'NO'

# 重置calories相關的變數和st.session_state (slider/type)
calorie_target = "無" # -> 相當於沒有限制，由生成器隨機
if "calories_value" not in st.session_state:
    st.session_state['calories_value'] = 500 # 如果使用者想客製化這個項目，default是這個值


# 重置price相關的變數和st.session_state (slider/type)
price_target = "無" # -> 相當於沒有限制，由生成器隨機 
if "price_value" not in st.session_state:
    st.session_state['price_value'] = 70 # 如果使用者想客製化這個項目，default是這個值

# 重置關於口味與配料的st.session_state
selected_type = ["Topping", "Taste", "Texture"] # 如果使用者想客製化這個項目，default是全選
if 'selected_type' not in st.session_state: # 重置segmented_control
    st.session_state['selected_type'] = ["Topping", "Taste", "Texture"] # 如果使用者想客製化這個項目，default是全選
whether_to_add_topping = ":rainbow[YES]" # 如果使用者想客製化這個項目，default是要加入topping
if 'add_topping' not in st.session_state:
    st.session_state['add_topping'] = ":rainbow[YES]" # 如果使用者想客製化這個項目，default是要加入topping

# if 'selected_topping' not in st.session_state:
#     st.session_state['selected_topping'] = ["焙烏龍茶凍 Oolong Tea Jelly"]
if 'topping_number_max' not in st.session_state:
    st.session_state['topping_number_max'] = 1
if 'random_topping_number' not in st.session_state:
    st.session_state['random_topping_number'] = "無" # -> 相當於沒有限制，由生成器隨機 
topping_set = [] # 目前取消客製化加入指定topping的功能，因此將此變數設為empty list

if 'selected_taste' not in st.session_state:
    st.session_state['selected_taste'] = [] # default為empty list    
if 'random_taste' not in st.session_state: 
    st.session_state['random_taste'] = "無" # -> 相當於沒有限制，由生成器隨機 
if 'selected_taste_display' not in st.session_state: 
    st.session_state['selected_taste_display'] = [] # default為empty list

if 'selected_texture' not in st.session_state:
    st.session_state['selected_texture'] = [] # default為empty list
if 'selected_texture_display' not in st.session_state: 
    st.session_state['selected_texture_display'] = [] # default為empty list
if 'random_texture' not in st.session_state: 
    st.session_state['random_texture'] = "不限" # -> 相當於沒有限制，由生成器隨機；"無"代表的是希望飲料的texture是"無"屬性的

invalid_texture = "" # default為""，表示沒有按過檢查button，後續再做判斷
if 'invalid_texture' not in st.session_state:
    st.session_state['invalid_texture'] = "" # default為""，表示沒有按過檢查button

full_random = False # default為 False，後續再做判斷
if 'full_random' not in st.session_state:
    st.session_state['full_random'] = False

submitted_check_status = False # default為沒有按下按鈕 (full random的狀況另外處理)
if 'submitted_check_status' not in st.session_state: 
    st.session_state['submitted_check_status'] = False # default為沒有按下按鈕 (full random的狀況另外處理)

check_reminder_status = "NO"
if 'check_reminder_status' not in st.session_state: 
    st.session_state['check_reminder_status'] = "NO" # default為""，代表沒有按過按鈕 (通過的代號名稱會有sucess字樣)

generator_section = False
if 'generator_section' not in st.session_state:
    st.session_state['generator_section'] = False

# def用來處理calories功能的開關的function
def calories_on_change(): 
    st.session_state['calories_customized'] = st.session_state["calories_temp"]
    return None

# 設定calories mode的選擇區
option_calories = st.radio(
    ":one: Do you want to customize the “calories” of your drinks?",
    [":rainbow[YES]", "NO",],
    key="calories_temp",
    index=1,
    on_change=calories_on_change,
    horizontal=True,
)

# def用來處理price功能的開關的function
def price_on_change():
    st.session_state['price_customized'] = st.session_state["price_temp"]
    return None

# 設定price mode的選擇區
option_price = st.radio(
    ":two: Do you want to customize the “price” of your drinks?",
    [":rainbow[YES]", "NO",], 
    key="price_temp",   
    index=1,
    on_change=price_on_change,
    horizontal=True,
)

# def用來處理ingredient功能的開關的function
def ingredient_on_change():
    st.session_state['ingredient_customized'] = st.session_state["ingredient_temp"]
    return None

# 設定ingredient mode的選擇區
option_ingredient = st.radio(
    ":three: Do you want to customize the “ingredient” of your drinks?",
    [":rainbow[YES]", "NO",],  
    key="ingredient_temp",  
    index=1,
    on_change=ingredient_on_change,
    horizontal=True,
)

# 設定三種客製化模式的代表badge
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


# 以markdown搭配badge顯示目前選擇的模式
if st.session_state['calories_customized'] == 'NO' and st.session_state['price_customized'] == 'NO' and st.session_state['ingredient_customized'] == 'NO':
    st.markdown("✔️ You selected: :violet-badge[Random generator]")
    full_random = True
    st.session_state['full_random'] = full_random
else: 
    st.markdown("✔️ You selected: " + badge_calories + badge_price + badge_ingredient)
    full_random = False
    st.session_state['full_random'] = full_random

# --- option_calories 的區塊 ---
# calories_value代表的是最終數值，calories_slider_value與calories_number_value代表的是從不同種輸入模式輸入的數值
# 設定以下兩個functions，用來同步兩種輸入方式的顯示數值
def update_from_calories_slider():
    st.session_state["calories_value"] = st.session_state["calories_slider_value"]
def update_from_calories_number():
    st.session_state["calories_value"] = st.session_state["calories_number_value"]

if option_calories == "NO": # 假如使用者不客製化飲料的熱量 -> 將calorie_target設定為"無"(代表沒有限制)
    calorie_target = "無"

if option_calories != "NO":
    st.divider()
    st.markdown("<p style='font-size:20px; color:DarkMagenta; font-weight:bold;'>1️⃣ Setting Target Calories for Your Drink</p>", unsafe_allow_html=True)
    
    col_calories_slider, col_calories_numberinput = st.columns([6, 1]) # 設定一組columns，左寬右窄，左邊放slider，右邊放number_input

    with col_calories_slider: # 設定左邊的column
        st.slider(
            "calories_slider",
            min_value=0,
            max_value=2000,
            key="calories_slider_value",
            value=st.session_state["calories_value"],
            on_change=update_from_calories_slider,
            label_visibility = "collapsed", 
        )

    with col_calories_numberinput: # 設定右邊的column
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

# --- option_calories 的區塊 ---

# --- option_price 的區塊 ---
# price_value代表的是最終數值，price_slider_value與price_number_value代表的是從不同種輸入模式輸入的數值
# 設定以下兩個functions，用來同步兩種輸入方式的顯示數值
def update_from_price_slider():
    st.session_state["price_value"] = st.session_state["price_slider_value"]
def update_from_price_number():
    st.session_state["price_value"] = st.session_state["price_number_value"]

if option_price == 'NO': # 假如使用者不客製化飲料的價錢 -> 將price_target設定為"無"(代表沒有限制)
    price_target = "無"

if option_price != 'NO':
    st.divider()
    st.markdown("<p style='font-size:20px; color:DarkMagenta; font-weight:bold;'>2️⃣ Setting Your Budget</p>", unsafe_allow_html=True)
    
    col_price_slider, col_price_numberinput = st.columns([6, 1]) # 設定一組columns，左寬右窄，左邊放slider，右邊放number_input
    
    with col_price_slider: # 設定左邊的column
        st.slider(
            "price_slider",
            min_value=0,
            max_value=1000,
            key="price_slider_value",
            value=st.session_state["price_value"],
            on_change=update_from_price_slider,
            label_visibility = "collapsed", 
        )

    with col_price_numberinput: # 設定右邊的column
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

# --- option_price 的區塊 ---

# --- option_ingredient 的區塊 ---
def update_customization_selection(): # 設定更新selected_type的session_state
    st.session_state['selected_type'] = st.session_state['customized_selection']
def update_whether_to_add_topping():
    st.session_state['whether_to_add_topping'] = st.session_state['add_topping']

# def update_topping_selection(): # 設定更新topping的session_state
#     st.session_state.selected_topping = st.session_state.temp_topping_selection
def update_topping_number_max(): # 設定更新topping的session_state
    st.session_state['topping_number_max'] = st.session_state['temp_topping_number_max']

def update_taste_selection(): # 設定更新taste的session_state
    st.session_state['selected_taste'] = st.session_state['temp_taste_selection']
def update_texture_selection(): # 設定更新texture的session_state
    st.session_state['selected_texture'] = st.session_state['temp_texture_selection']

# Ingredient中可以客製化的項目 ["Topping", "Taste", "Texture"]
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
    check_reminder_status = "success_3" # -> 視為texture全選的狀況 
    st.session_state['check_reminder_status'] = check_reminder_status

# 選擇要客製化的Ingredient項目 ["Topping", "Taste", "Texture"]
if option_ingredient != 'NO': 
    with st.container(border=False,):
        # 區域大標題
        st.markdown("<p style='margin-bottom: 0px; font-size:20px; color:DarkMagenta; font-weight:bold;'>3️⃣ Customize Your Ingredients</p>", unsafe_allow_html=True)    
        # 標題
        st.markdown("<p style='margin-bottom: 0px; font-size:16px; color:DarkMagenta; font-weight:bold;'>Select the type you want to customize.</p>", unsafe_allow_html=True)
    
    # 設定 選擇客製化ingredients的segmented_control (預設在session state是全選)
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
        check_reminder_status = "success_3" # 視為texture全選的狀況 
        st.session_state['check_reminder_status'] = check_reminder_status

# 加料 Topping
if option_ingredient != 'NO' and "Topping Number" in selected_type:
    with st.container(border=True,):
        st.markdown("<p style='margin-bottom: 0px; font-size:16px; color:DarkSlateBlue; font-weight:bold;'> ① Customize Your Topping</p>", unsafe_allow_html=True)
        
        # 選擇是否要加料 (False -> topping_number_max = 0)
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

        if whether_to_add_topping!="NO": # 如果使用者想要加topping
            # 選擇要添加的topping數量上限 (後面還要跟選擇出來的topping範圍判斷一次)
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


# 風味 taste         
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
        
        # display 所有使用者選擇的項目，實際上隨機從中選出一個給generator
        random_taste = ""
        selected_taste_display = ""

        if len(selected_taste)>0:
            random_taste = random.choice(selected_taste) # 從使用者選擇的一或多個項目中選出一個
            st.session_state['random_taste'] = random_taste

            for i in range((len(selected_taste)-1)): # 設定顯示在頁面上的選項
                selected_taste_display = selected_taste_display + str(selected_taste[i]) + ', '
            selected_taste_display = selected_taste_display + str(selected_taste[-1])
            
            st.session_state['selected_taste_display'] = selected_taste_display
            st.markdown("➡️ Your selected taste: " + selected_taste_display + ".")
        else: # 沒選視同全選 -> 直接從所有選項中隨機
            random_taste = random.choice(taste) 
            selected_taste_display = ""

            st.session_state['random_taste'] = random_taste
            st.session_state['selected_taste_display'] = selected_taste_display
            st.markdown("➡️ You'll get random taste of drinks!")

# 口感 Texture
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
    
    # 定義隨機 + 檢查函式：選項前後不搭的話，跳warning 
    # 如果不加配料的話，random_topping_number==0，所以直接使用random_topping_number (而不是是否加配料的bool)
    def random_texture_and_check(random_topping_number, selected_texture):
        # 要判斷使用者是否不加topping 卻選擇了果粒或嚼感texture
        # 如果使用者做了矛盾的選擇，後續要跳出提醒
        # 衝突檢查通過的話，random出一個texture，並設定好selected_texture_display
        # 衝突檢查不通過的話，random_texture = ""，selected_texture_display = ""
        random_texture = ""
        invalid_texture = False
        selected_texture_display = ""
        check_reminder_status = "NO"

        if random_topping_number==0 and selected_texture in ["果粒 Fruitiness", "嚼感 Chewiness"]:
            invalid_texture = True
            check_reminder_status = "warning"
            # 將texture相關的值都設為"warning" 以利debug
            random_texture = "warning"
            selected_texture_display = "warning"
        else:
            invalid_texture = False
        
        if invalid_texture==False: # 衝突檢查通過
            if len(selected_texture)==0: # 沒有選擇texture -> 飲料的texture屬性要是空的
                random_texture = '無'
                selected_texture_display = '無' # -> Your drink will not have a specific texture property.
                check_reminder_status = "success_0"
            
            if len(selected_texture) > 0:
                random_texture = random.choice(selected_texture) # 從使用者選擇的一或多個項目中選出一個
                
                for i in range((len(selected_texture)-1)): # 設定顯示在頁面上的選項
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

            # 顯示在button下方
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
            if st.session_state['check_reminder_status']=="NO": # 還沒有按過check的時候顯示的字樣
                st.markdown("👈 Please click the check button after the selection is complete.")
            if st.session_state['check_reminder_status'] in ["success_0", "success_12", "success_3", ]: # 如果texture檢查通過，則顯示這則訊息
                st.markdown("🆗 Pass! This combination can be used. ")
            if st.session_state['check_reminder_status']=="warning": # 如果檢查不通過，則跳出warning
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


# 一些會用到的emoji： 🎲 ✅ ✔️ ⚠️ 🚨 👈 💸 🔥 🌟 ✨ 🔄 ➡️ 🆗 
# ----- [start] 接入generator前的設定與轉換 -----
# 要輸入generator的：

# [OK] price_target要放前面使用者輸入的price值或是隨機的值
# [OK] calorie_target要放前面使用者輸入的calorie值或是隨機的值 

# [OK] random_topping_number要放前面使用者輸入的topping數量或是隨機的數量
# 如果不加配料的話，random_topping_number==0 (random_topping_number==""代表未設定 -> 正常來說會random一個結果)

# [OK] taste是 random_taste (1個) (不選視同全選 所以永遠都是一個) 
# [OK] texture是 random_texture (1個) (不選跟全選不同 不選是"無"，全選要random，""代表未設定 -> 正常來說會random一個結果)) 

mode = "no" # 目前預設為no -> 功能code有寫出來 但UI來不及做完
topping_num = random_topping_number

taste_preference = st.session_state['random_taste'] # 已完成名稱配對
# taste 改名 ('無'不用改名)
taste_name_generator = ['甘', '苦', '酸', '甜', '酸甜', '奶味']
taste_name_dict = dict(zip(taste, taste_name_generator))
if taste_preference in taste_name_dict:
    taste_preference = taste_name_dict[taste_preference]

texture_preference = st.session_state['random_texture'] # 已完成名稱配對
# texture 改名 ('無'或'不限'不用改名)
texture_name_generator = ['果粒', '濃厚', '嚼感']
texture_name_dict = dict(zip(texture, texture_name_generator))
if texture_preference in texture_name_dict:
    texture_preference = texture_name_dict[texture_preference]

# ----- [end] 接入generator前的設定與轉換 -----

# ----- [start] Code completed by withdrawn member Mr. Chan -----

# --- [start] 此部分的code尚未做好對應的UI，因此轉為註解 ---
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

# --- [end] 此部分的code尚未做好對應的UI，因此轉為註解 ---

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


topping_set = [] # 因設計難度較高，暫不設計可以讓使用者自訂topping種類的功能，所以設定為empty list
df_filtered = df_topping[~df_topping['Name'].isin(topping_set)].reset_index(drop=True)

initial_toppings = df_topping[df_topping['Name'].isin(topping_set)]
topping_calories_initial_med = sum(int(row['Cal_med']) for _, row in initial_toppings.iterrows())
topping_price_initial_med = sum(int(row['Price_med']) for _, row in initial_toppings.iterrows())
topping_calories_initial_big = sum(int(row['Cal_big']) for _, row in initial_toppings.iterrows())
topping_price_initial_big = sum(int(row['Price_big']) for _, row in initial_toppings.iterrows())

# ----- [end] Code completed by withdrawn member Mr. Chan -----

# 初始化 Part2
if 'dice_rolled' not in st.session_state:
    st.session_state['dice_rolled'] = False
if 'drink_combination' not in st.session_state:
    st.session_state['drink_combination'] = dict()
# if 'add_to_fav' not in st.session_state:
#     st.session_state['add_to_fav'] = False

generator_section = False
st.session_state['generator_section'] = generator_section
if check_reminder_status == "NO": # 獨立處理按過YES，再按NO的話，st.session_state['check_reminder_status']沒有跟check_reminder_status同步的狀況
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

# --- [start] generator_section的debug code ---
# st.write('full_random = ', full_random)
# st.write('submitted_check_status = ', submitted_check_status)
# st.write('check_reminder_status = ', check_reminder_status)
# st.write('generator_section = ', generator_section)
# st.write(st.session_state['generator_section'])

# st.write('full_random = ', st.session_state['full_random'])
# st.write('check_reminder_status = ', st.session_state['check_reminder_status'])
# st.write('type(check_reminder_status) = ', type(st.session_state['check_reminder_status']))

# --- [end] generator_section的debug code ---

# full_random == True 或 前面invalid_texture檢查通過之後，才能讓使用者使用generator
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
        
        # def等下要使用的get_difference function
        def get_difference(value, target):
            if target == 2147483647: # 如果target是沒有指定的狀態，target == 2147483647
                return 0 # target沒有指定的狀況下，不用計算差值(difference)
            else:
                return abs(value - int(target))

        # 將generate功能設定為需要
        with st.form('generator_form', clear_on_submit=False, border=False,):
            submitted_generator = st.form_submit_button("🎲 Create your own destined pour! ") 
            # 🎲 Roll the dice!

            if submitted_generator: # 如果按下按鈕開始generate
                # ----- [start] Code completed by withdrawn member Mr. Chan -----
                # 基於Mr. Chan的code，額外追加了挑選combination的計算
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
                
                # st.write(drink_conbination) # 用來檢查generator是否worked -> 完成後須註解掉

                # 將符合初步篩選條件的組合放入pandas的dataframe中
                df_drink_combination = pd.DataFrame(drink_conbination)
                # 按 Difference Score 由小到大排序
                df_drink_combination_sorted = df_drink_combination.sort_values('Difference Score', ascending=True).reset_index(drop=True)
                # 計算每一組與第一組(第零列)的Difference Score的差值
                df_drink_combination_sorted['Difference Score from Combination 0'] = df_drink_combination_sorted['Difference Score'] - df_drink_combination_sorted.iloc[0]['Difference Score']

                if drink_conbination == []: # 如果生成不出組合，顯示warning
                    st.markdown(
                        """
                        <div style="border-left: 0.3rem solid orange; padding: 1rem; background-color: #fff7e6; border-radius: 0.5rem;">
                            <strong>⚠️ Warning: </strong><br><br>
                            No valid combinations found.
                        </div>ination_sorted.iloc[0].to_dict()
                        """,
                        unsafe_allow_html=True
                    )        

                if drink_conbination != []: # 如果有正常生成出結果 -> 顯示生成的結果
                    chosen_drink_combination = dict() # 將chosen_drink_combination設為empty dict
                    df_waiting_list = pd.DataFrame() # 將df_waiting_list設為empty pd.dataframe
                    df_waiting_list2 = pd.DataFrame() # 將df_waiting_list2設為empty pd.dataframe

                    if len(df_drink_combination_sorted) == 1: # 如果符合條件的組合恰有1組
                        # 將符合條件的組合轉換為dict，並放入chosen_drink_combination
                        chosen_drink_combination = df_drink_combination_sorted.iloc[0].to_dict() 

                    if len(df_drink_combination_sorted) > 1: # 如果符合條件的組合不只1組
                        # diff1是指第2列的資料的'Difference Score from Combination 0'對應的值
                        diff1 = df_drink_combination_sorted.iloc[1]['Difference Score from Combination 0']
                        if len(df_drink_combination_sorted) > 4: # 如果符合條件的組合至少有5組，計算diff4
                            # diff4是指第5列的資料的'Difference Score from Combination 0'對應的值
                            diff4 = df_drink_combination_sorted.iloc[4]['Difference Score from Combination 0']
                        
                        if diff1 > 30: # 如果第2組的'Difference Score from Combination 0'對應的值大於 30 -> 選擇第1組(第0列)的組合作為chosen_drink_combination
                            chosen_drink_combination = df_drink_combination_sorted.iloc[0].to_dict()
                            
                        else:  # 如果第2組的'Difference Score from Combination 0'對應的值(diff1)小於等於 30
                            # 先找出所有差值('Difference Score from Combination 0'對應的值)在 31 以下的組合
                            df_waiting_list = df_drink_combination_sorted[df_drink_combination_sorted['Difference Score from Combination 0'] < 31]
                            if df_waiting_list.shape[0] >= 5 and (diff4 == 0): 
                                # 如果有至少5組分數一樣，，將'Difference Score from Combination 0'對應的值 < 1 的組別收集到df_waiting_list2，並從這些組裡隨機挑1組
                                df_waiting_list2 = df_drink_combination_sorted[df_drink_combination_sorted['Difference Score from Combination 0'] < 1]
                                candidates_length = len(df_waiting_list2)
                                random_candidate_loc = random.randint(0, candidates_length-1)
                                chosen_drink_combination = df_waiting_list2.iloc[random_candidate_loc].to_dict()
                                # top_candidates = df_waiting_list[df_waiting_list['Difference Score from Combination 0'] == 0]
                                # chosen_drink_combination = top_candidates.sample(1).iloc[0].to_dict()
                            elif df_waiting_list.shape[0] >= 5 and (diff4 > 0):
                                # 如果條件的組別至少有五組，但diff4 != 0，則從前5組裡面隨機挑1組
                                random_candidate_loc = random.randint(0, 4)
                                chosen_drink_combination = df_waiting_list.iloc[random_candidate_loc].to_dict()
                            else:
                                # 如果符合條件的組別大於1組，小於5組，則從這些組別中隨機挑1組
                                candidates_length = len(df_waiting_list)
                                random_candidate_loc = random.randint(0, candidates_length-1)
                                chosen_drink_combination = df_waiting_list.iloc[random_candidate_loc].to_dict()

                    st.session_state['drink_combination'] = chosen_drink_combination
                    
                    # 將chosen_drink_combination的drink名稱改名為中英文雙語版本
                    chosen_drink_drink_name = chosen_drink_combination['Drink']
                    converted_drink_name = ""
                    drink_name_generator = ["紅茶", "綠茶", "烏龍茶", "阿華田", "水"]
                    drink_name_display = ["紅茶 Black tea", "綠茶 Green tea", "烏龍茶 Oolong tea", "阿華田(可可) Ovaltine (Cocoa)", "水 Water"]
                    drink_name_dict = dict(zip(drink_name_generator, drink_name_display))
                    if chosen_drink_drink_name in drink_name_dict:
                        converted_drink_name = drink_name_dict[chosen_drink_drink_name]
                    chosen_drink_drink_name = converted_drink_name

                    # 將chosen_drink_combination的size名稱改名為中英文雙語版本
                    chosen_drink_size = chosen_drink_combination['Size']
                    converted_size_name = ""
                    size_name_generator = ["中杯", "大杯"]
                    size_name_display = ["中杯 Medium", "大杯 Large"]
                    size_name_dict = dict(zip(size_name_generator, size_name_display))
                    if chosen_drink_size in size_name_dict:
                        converted_size_name = size_name_dict[chosen_drink_size]
                    chosen_drink_size = converted_size_name

                    # 將chosen_drink_combination的side名稱改名為中英文雙語版本
                    chosen_drink_side = chosen_drink_combination['Side']
                    converted_side_name = ""
                    side_name_generator = ["優酪", "奶蓋", "奶精", "鮮奶"]
                    side_name_display = ["優酪 Yogurt", "奶蓋 Milk cap", "奶精 Creamer", "鮮奶 Fresh milk"]
                    side_name_dict = dict(zip(side_name_generator, side_name_display))
                    if chosen_drink_side in side_name_dict:
                        converted_side_name = side_name_dict[chosen_drink_side]
                    chosen_drink_side = converted_side_name

                    # 將chosen_drink_combination的topping名稱改名為中英文雙語版本
                    chosen_drink_topping = chosen_drink_combination['Topping']
                    converted_topping_name = []
                    topping_name_generator = ['檸檬', '香橙', '甘蔗', '春梅', '柚子', '珍珠', '焙烏龍茶凍']  
                    topping_name_display = ["檸檬 Lemon", "香橙 Orange", "甘蔗 Sugar cane", "春梅 Green Plum", "柚子 Yuzu/Pomelo", "珍珠 Golden Bubble/Pearl", "焙烏龍茶凍 Oolong Tea Jelly"]      
                    
                    topping_name_dict = dict(zip(topping_name_generator , topping_name_display))
                    for i in chosen_drink_topping:
                        if i in topping_name_dict: # 將要置換的新名稱放入converted_topping_name
                            converted_topping_name.append(topping_name_dict[i])
                        else:
                            converted_topping_name.append()
                    chosen_drink_topping = converted_topping_name #將chosen_drink_topping的內容換成converted_topping_name的內容

                    # 設定要display給使用者看的chosen_drink_combination的topping
                    chosen_drink_topping_display = ""
                    if len(chosen_drink_combination['Topping']) > 0:
                        for i in range((len(chosen_drink_combination['Topping'])-1)):
                            chosen_drink_topping_display = chosen_drink_topping_display + str(chosen_drink_topping[i]) + ', '
                        chosen_drink_topping_display = chosen_drink_topping_display + str(chosen_drink_topping[-1])
                    if len(chosen_drink_combination['Topping']) == 0:
                        chosen_drink_topping = 'None'

                    chosen_drink_price = chosen_drink_combination['Total Price']
                    chosen_drink_calories = chosen_drink_combination['Total Calories']

                    # 將生成的飲料組合裝成一個dict
                    drink_combination_display = dict()
                    drink_combination_display = {
                        'Random Items': 'Content', 
                        '飲料基底 Drink': chosen_drink_drink_name,
                        '飲料尺寸 Size': chosen_drink_size, 
                        '特調配料 Side': chosen_drink_side,
                        '配料 Topping': chosen_drink_topping_display,                         
                    }

                    # 將drink_combination_display改以pd.dataframe的形式，儲存在df_drink_combination_display 
                    df_drink_combination_display = pd.DataFrame(drink_combination_display, index=[0])
                    cols_display = ['飲料基底 Drink', '飲料尺寸 Size','特調配料 Side','配料 Topping']
                    df_drink_combination_display = df_drink_combination_display[cols_display]
                    # 將df_drink_combination_display行列互換，儲存於df_drink_combination_display_T
                    df_drink_combination_display_T = df_drink_combination_display.T 

                    with st.container(border=True,):
                        col_destined_pour, col_generator_status = st.columns([6, 1])

                        with col_destined_pour:
                            # 將標題字樣設為彩色漸層(此設定是參考chatgpt給出的範例)
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

                        col_price, col_calories = st.columns(2) # 數值可改用st.metric呈現

                        with col_price: # 在這個column中顯示飲料的價位
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

                        with col_calories: # 在這個column中顯示飲料的熱量
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
                
