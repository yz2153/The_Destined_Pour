import pandas as pd
import random
from itertools import combinations
import streamlit as st


# 設定頁面的標題與副標題(模式選擇)
st.title(":cup_with_straw: The Destined Pour")
st.header("Select the generator mode you want!")

# 初始化 Part1
 
# 重置三種關於模式的限制的st.session_state
if 'calories_customized' not in st.session_state:
    st.session_state['calories_customized'] = 'NO'
if 'price_customized' not in st.session_state:
    st.session_state['price_customized'] = 'NO'
if 'ingredient_customized' not in st.session_state:
    st.session_state['ingredient_customized'] = 'NO'

# 重置calories相關的st.session_state (slider/type)
if "calories_value" not in st.session_state:
    st.session_state['calories_value'] = 500
calorie_target = 500

# 重置price相關的st.session_state (slider/type)
if "price_value" not in st.session_state:
    st.session_state['price_value'] = 70
price_target = 70

# 重置關於口味與配料的st.session_state
if 'selected_type' not in st.session_state: # 重置segmented_control
    st.session_state['selected_type'] = ["Topping", "Taste", "Texture"]
if 'add_topping' not in st.session_state:
    st.session_state['add_topping'] = ":rainbow[YES]"

# if 'selected_topping' not in st.session_state:
#     st.session_state['selected_topping'] = ["焙烏龍茶凍 Oolong Tea Jelly"]
if 'topping_number_max' not in st.session_state:
    st.session_state['topping_number_max'] = 1

if 'selected_taste' not in st.session_state:
    st.session_state['selected_taste'] = []   
if 'random_taste' not in st.session_state: 
    st.session_state['random_taste'] = ""
if 'selected_taste_display' not in st.session_state: 
    st.session_state['selected_taste_display'] = []

if 'selected_texture' not in st.session_state:
    st.session_state['selected_texture'] = [] 
if 'selected_texture_display' not in st.session_state: 
    st.session_state['selected_texture_display'] = []
if 'random_texture' not in st.session_state: 
    st.session_state['random_texture'] = ""

if 'check_reminder_status' not in st.session_state: 
    st.session_state['check_reminder_status'] = ""


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


# 顯示目前選擇的模式
if option_calories == 'NO' and option_price == 'NO' and option_ingredient == 'NO':
    st.markdown("✔️ You selected: :violet-badge[Random generator]")
else: 
    st.markdown("✔️ You selected: " + badge_calories + badge_price + badge_ingredient)

st.divider()

# --- option_calories 的區塊 ---
def update_from_calories_slider():
    st.session_state["calories_value"] = st.session_state["calories_slider_value"]
def update_from_calories_number():
    st.session_state["calories_value"] = st.session_state["calories_number_value"]

if option_calories == "NO":
    calorie_target = random.randint(0, 2000)

if option_calories != "NO":
    st.markdown("<p style='font-size:20px; color:DarkMagenta; font-weight:bold;'>1️⃣ Setting Target Calories for Your Drink</p>", unsafe_allow_html=True)
    
    col_calories_slider, col_calories_numberinput = st.columns([6, 1])

    with col_calories_slider:
        st.slider(
            "calories_slider",
            min_value=0,
            max_value=2000,
            key="calories_slider_value",
            value=st.session_state["calories_value"],
            on_change=update_from_calories_slider,
            label_visibility = "collapsed", 
        )

    with col_calories_numberinput:
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

    st.divider()
# --- option_calories 的區塊 ---

# --- option_price 的區塊 ---
def update_from_price_slider():
    st.session_state["price_value"] = st.session_state["price_slider_value"]
def update_from_price_number():
    st.session_state["price_value"] = st.session_state["price_number_value"]

if option_price == 'NO':
    price_target = random.randint(0,1000)

if option_price != 'NO':
    st.markdown("<p style='font-size:20px; color:DarkMagenta; font-weight:bold;'>2️⃣ Setting Your Budget</p>", unsafe_allow_html=True)
    
    col_price_slider, col_price_numberinput = st.columns([6, 1])
    
    with col_price_slider:
        st.slider(
            "price_slider",
            min_value=0,
            max_value=1000,
            key="price_slider_value",
            value=st.session_state["price_value"],
            on_change=update_from_price_slider,
            label_visibility = "collapsed", 
        )

    with col_price_numberinput:
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

    st.divider()
# --- option_price 的區塊 ---

# --- option_ingredient 的區塊 ---
def update_customization_selection(): # 設定更新selected_type的session_state
    st.sessionstate['selected_type'] = st.session_state['customized_selection']
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

def update_check_button():
    st.session_state['check_combination_status'] = True

# 各項目的選項 ["Topping", "Taste", "Texture"]
# topping = ["檸檬 Lemon", "香橙 Orange", "甘蔗 Sugar cane", "春梅 Green Plum", "柚子 Yuzu/Pomelo", "珍珠 Golden Bubble/Pearl", "焙烏龍茶凍 Oolong Tea Jelly"]
taste = ["清爽回甘 Refreshing & Sweet Tea Flavor", "醇濃茶香 Mellow Tea Flavor", "酸 Sour", "甜 Sweet", "酸甜 Sweet & Sour", "奶香 Milky Flavor",]
texture = ["果粒 Fruitiness", "濃厚 Thick", "嚼感 Chewiness",]

if option_ingredient == 'NO':
    random_topping_number = random.randint(0, 5)
    random_taste = str(random.sample(taste, 1))
    random_texture = str(random.sample(texture, 1))
    invalid_textureb = False
    check_reminder_status = "success_3" # -> 視為全選的狀況 

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
    if "Topping Number" not in selected_type:
        random_topping_number = random.randint(0, 5)
    if "Taste" not in selected_type:
        random_taste = str(random.sample(taste, 1))
    if "Texture" not in selected_type:
        random_texture =str( random.sample(texture, 1))
        invalid_textureb = False
        check_reminder_status = "success_3" # -> 視為全選的狀況 

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
        
        st.markdown("➡️ The number of toppings on your drink is " + random_topping_number + ".")


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
            label_visibility = "collapsed", 
            )
    
    # 定義隨機+檢查函式：選項前後不搭的話，跳warning 
    # 如果不加配料的話，random_topping_number==0，所以直接使用random_topping_number (而不是是否加配料的bool)
    def random_texture_and_check(random_topping_number, selected_texture):
        # 要判斷使用者是否不加topping 卻選擇了果粒或嚼感texture
        # 如果使用者做了矛盾的選擇，後續要跳出提醒
        # 衝突檢查通過的話，random出一個texture，並設定好selected_texture_display
        # 衝突檢查不通過的話，random_texture = ""，selected_texture_display = ""
        random_texture = ""
        invalid_texture = False
        selected_texture_display = ""
        check_reminder_status = ""

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
    
        return random_texture, invalid_texture, selected_texture_display, check_reminder_status
        
    with st.form('check_and_reminder_form', clear_on_submit=False, border=True,):
        col_check_button, col_check_reminder = st.columns([1, 2])

        with col_check_button:
            submitted_check = st.form_submit_button("🔍 Check! ")

            # 顯示在button下方
            st.markdown("<p style='margin-top: 0px; margin-bottom: 0px; font-size:12px; color:DarkGray; font-weight:bold;'>◇ Please make sure your customized combination is valid before generating. </p>", unsafe_allow_html=True)    
        
        if submitted_check:
            random_texture, invalid_texture, selected_texture_display, check_reminder_status = random_texture_and_check(random_topping_number, selected_texture)
            st.session_state['random_texture'] = random_texture
            st.session_state['selected_texture_display'] = selected_texture_display
            st.session_state['invalid_texture'] = invalid_texture
            st.session_state['check_reminder_status'] = check_reminder_status

        with col_check_reminder:
            if st.session_state['check_reminder_status']=="": # 還沒有按過check的時候顯示的字樣
                st.markdown("👈 Please click the check button after the selection is complete.")
            if st.session_state['check_reminder_status'] in ["success_0", "success_12", "success_3", ]: # 如果texture檢查通過，則顯示這則訊息
                st.markdown("🆗 Pass! This combination can be used. ")
            if st.session_state['check_reminder_status']=="warning": # 如果檢查不通過，則跳出warning
                st.markdown("🚨 Please ensure that your selection is valid. ")
        
    with st.container():
        if st.session_state['check_reminder_status'] != "":
            st.markdown(
                """
                <div style="margin-top: 0px; margin-bottom: 0px; border-left: 0.3rem solid #b19cd9; padding: 1rem; background-color: #f5f0ff; border-radius: 0.5rem; ">
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
            
        if st.session_state['check_reminder_status']=="success_0":
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
        
        if st.session_state['check_reminder_status']=="success_12":
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

        if st.session_state['check_reminder_status']=="success_3":
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
    st.divider()               

# 一些會用到的emoji： 🎲 ✅ ✔️ ⚠️ 🚨 👈 💸 🔥 🌟 ✨ 🔄 ➡️ 🆗 

# ----- [start] 接入功能code的必要轉換 -----
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
# texture 改名 ('無'不用改名)
texture_name_generator = ['果粒', '濃厚', '嚼感']
texture_name_dict = dict(zip(texture, texture_name_generator))
if texture_preference in texture_name_dict:
    texture_preference = texture_name_dict[texture_preference]

# ----- [end] 接入功能code的必要轉換 -----

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

if price_target == '無':
    price_target = 2147483647
if topping_num == '無':
    topping_num = 2147483647
if calorie_target == '無':
    calorie_target = 2147483647

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
if 'add_to_fav' not in st.session_state:
    st.session_state['add_to_fav'] = False
if 'drink_combination' not in st.session_state:
    st.session_state['drink_combination'] = dict()

if st.session_state['check_reminder_status'] in ["success_0", "success_12", "success_3"]: # 前面檢查通過之後 才能讓使用者使用generator
    with st.container():
        st.markdown("<p style='margin-bottom: 0px; font-size:16px; color:DarkSlateBlue; font-weight:bold;'>下方皆為舊版code 正在改版</p>", unsafe_allow_html=True)
        st.markdown("""
        <h1 style='font-size: 24px; font-weight: 600; margin-bottom: 16px;'>
            Random generator
        </h1>
        """, unsafe_allow_html=True)
        # st.header("Random generator")
        
        with st.form('generator_form', clear_on_submit=False, border=False,):
            submitted_generator = st.form_submit_button("🎲 Roll the dice! ") 

            if submitted_generator:
                # ----- [start] Code completed by withdrawn member Mr. Chan -----
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
                                    or texture_preference=='無')
                                    ): drink_conbination.append({
                                        'Drink': drink['Name'],
                                        'Size' : '中杯',
                                        'Topping': topping_names,
                                        'Side': '無',
                                        'Total Calories': total_calories,
                                        'Total Price': total_price
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
                                texture_preference == '無')
                            ): drink_conbination.append({
                                    'Drink': drink['Name'],
                                    'Size' : '中杯',
                                    'Topping': topping_names,
                                    'Side': side['Name'],
                                    'Total Calories': total_calories,
                                    'Total Price': total_price
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
                                    texture_preference == '無')
                                ): drink_conbination.append({
                                        'Drink': drink['Name'],
                                        'Size' : '大杯',
                                        'Topping': topping_names,
                                        'Side': '無',
                                        'Total Calories': total_calories,
                                        'Total Price': total_price
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
                                    texture_preference == '無')
                                ): drink_conbination.append({
                                        'Drink': drink['Name'],
                                        'Size' : '大杯',
                                        'Topping': topping_names,
                                        'Side': side['Name'],
                                        'Total Calories': total_calories,
                                        'Total Price': total_price
                                    })

                # ----- [end] Code completed by withdrawn member Mr. Chan -----
                
                st.write("drink_conbination = " + drink_conbination)

                chosen_drink_combination = random.choice(drink_conbination)
                st.session_state['drink_combination'] = chosen_drink_combination
                chosen_drink_combination_topping = ''
                chosen_drink_price = chosen_drink_combination['Total Price']
                chosen_drink_calories = chosen_drink_combination['Total Calories']

                for i in range((len(chosen_drink_combination['Topping'])-1)):
                    chosen_drink_combination_topping = chosen_drink_combination_topping + str(chosen_drink_combination['Topping'][i]) + ', '
                chosen_drink_combination_topping = chosen_drink_combination_topping + str(chosen_drink_combination['Topping'][-1])

                drink_combination_display = dict()
                drink_combination_display = {
                    'Random Items': 'Content', 
                    'Drink': chosen_drink_combination['Drink'],
                    'Size': chosen_drink_combination['Size'], 
                    'Topping': chosen_drink_combination_topping, 
                    'Side': chosen_drink_combination['Side'],
                }

                df_drink_combination_display = pd.DataFrame(drink_combination_display, index=[0])
                df_drink_combination_display_T = df_drink_combination_display.T
                # print("Your destined pour:")
                # print(chosen_drink_combination)
            # else:
                # print("No valid combinations found.")

                st.markdown(f"""
                <div style='font-size:20px; font-weight:bold;'>
                Formula_of_the_drink
                </div>
                """, unsafe_allow_html=True) # [store_name] 暫時取消

                st.dataframe(
                    df_drink_combination_display_T, 
                    # hide_index=True,
                )

                # ------
                st.markdown(
                ":green-badge[:material/check: Success]"
                )
                
                col_price, col_calories = st.columns(2) # 這邊的內容可以考慮改用st.metric呈現

                with col_price:
                    # 這邊之後要加上產出飲料的價位
                    st.markdown(f"""
                    <p style='margin-bottom: 2px; font-size:16px;'> 💸 Price </p>
                    <p style='margin-bottom: 2px; font-size:24px; font-weight:bold;'> {chosen_drink_price} </p>
                    """, unsafe_allow_html=True
                    )

                with col_calories:
                    # 這邊之後要加上產出飲料的熱量
                    st.markdown(f"""
                    <p style='margin-bottom: 2px; font-size:16px;'> 🔥 Calories </p>
                    <p style='margin-bottom: 2px; font-size:24px; font-weight:bold;'> {chosen_drink_calories} </p>
                    """, unsafe_allow_html=True
                    )
