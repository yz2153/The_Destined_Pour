# import numpy as np
# import pandas as pd
import random
from itertools import combinations
import streamlit as st
 
# 設定頁面的標題與副標題(模式選擇)
st.title(":cup_with_straw: The Destined Pour")
st.header("Select the generator mode you want!")

# 重置三種關於模式的限制的st.session_state
if 'calories_customized' not in st.session_state:
    st.session_state['calories_customized'] = 'NO'
if 'price_customized' not in st.session_state:
    st.session_state['price_customized'] = 'NO'
if 'ingredient_customized' not in st.session_state:
    st.session_state['ingredient_customized'] = 'NO'

# 重置calories相關的st.session_state (slider/type)
if "calories_value" not in st.session_state:
    st.session_state['calories_value'] = 350
# 重置budget相關的st.session_state (slider/type)
if "budget_value" not in st.session_state:
    st.session_state['budget_value'] = 50

# 重置關於口味與配料的st.session_state
if 'selected_type' not in st.session_state: # 重置segmented_control
    st.session_state['selected_type'] = ["Topping", "Taste", "Texture"]
if 'add_topping' not in st.session_state:
    st.session_state['add_topping'] = True
if 'selected_topping' not in st.session_state:
    st.session_state['selected_topping'] = []
if 'selected_taste' not in st.session_state:
    st.session_state['selected_taste'] = []   
if 'selected_testure' not in st.session_state: # 這個的選擇還沒有完成
    st.session_state['selected_testure'] = [] 

# 重置用來放模式選擇結果的list
mode_badge_list = []

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
    

# ---
st.divider()
# ---

# --- option_calories 的區塊 ---
def update_from_calories_slider():
    st.session_state["calories_value"] = st.session_state["calories_slider_value"]
def update_from_calories_number():
    st.session_state["calories_value"] = st.session_state["calories_number_value"]


if option_calories != 'NO':
    st.markdown("<p style='font-size:20px; color:DarkMagenta; font-weight:bold;'>Setting Target Calories for Your Drink</p>", unsafe_allow_html=True)
    
    col_calories_slider, col_calories_numberinput = st.columns([6, 1])

    with col_calories_slider:
        st.slider(
            "",
            min_value=0,
            max_value=1000,
            key="calories_slider_value",
            value=st.session_state["calories_value"],
            on_change=update_from_calories_slider,
            label_visibility = "collapsed", 
        )

    with col_calories_numberinput:
        st.number_input(
            "",
            min_value=0,
            max_value=1000,
            key="calories_number_value",
            value=st.session_state["calories_value"],
            on_change=update_from_calories_number,
            label_visibility = "collapsed",
        )

    calories_text = st.session_state["calories_value"]
    st.markdown(f"""
    Your target calorie count for your drink is <span style='color: SlateBlue; font-weight: bold;'>{calories_text}</span> calories.
    """, unsafe_allow_html=True)

    st.divider()
# --- option_calories 的區塊 ---

# --- option_price 的區塊 ---
def update_from_price_slider():
    st.session_state["budget_value"] = st.session_state["price_slider_value"]

def update_from_price_number():
    st.session_state["budget_value"] = st.session_state["price_number_value"]


if option_price != 'NO':
    st.markdown("<p style='font-size:20px; color:DarkMagenta; font-weight:bold;'>Setting Your Budget</p>", unsafe_allow_html=True)
    
    col_price_slider, col_price_numberinput = st.columns([6, 1])

    
    with col_price_slider:
        st.slider(
            "",
            min_value=0,
            max_value=1000,
            key="price_slider_value",
            value=st.session_state["budget_value"],
            on_change=update_from_price_slider,
            label_visibility = "collapsed", 
        )

    with col_price_numberinput:
        st.number_input(
            "",
            min_value=0,
            max_value=1000,
            key="price_number_value",
            value=st.session_state["budget_value"],
            on_change=update_from_price_number,
            label_visibility = "collapsed",
        )

    budget_text = st.session_state["budget_value"]
    st.markdown(f"""
    Your budget is <span style='color: SlateBlue; font-weight: bold;'>{budget_text}</span> dollars.
    """, unsafe_allow_html=True)

    st.divider()
# --- option_price 的區塊 ---

# --- option_ingredient 的區塊 ---
def update_customization_selection(): # 設定更新selected_type的ession_state
    st.session_state.selected_type = st.session_state.customized_selection
def update_whether_to_add_topping():
    st.session_state.whether_to_add_topping = st.session_state.add_topping
def update_topping_selection(): # 設定更新topping的session_state
    st.session_state.selected_topping = st.session_state.temp_topping_selection
def update_taste_selection(): # 設定更新taste的session_state
    st.session_state.selected_taste = st.session_state.temp_taste_selection
def update_texture_selection(): # 設定更新texture的session_state
    st.session_state.selected_texture = st.session_state.temp_texture_selection

if option_ingredient != 'NO':
    # 區域大標題
    st.markdown("<p style='font-size:20px; color:DarkMagenta; font-weight:bold;'>Customize Your Ingredients</p>", unsafe_allow_html=True)    
    # 標題
    st.markdown("<p style='font-size:16px; color:DarkMagenta; font-weight:bold;'>Select the type you want to customize~</p>", unsafe_allow_html=True)
   
   # 設定 選擇客製化ingredients的segmented_control
    type_customization = ["Topping", "Taste", "Texture"]
    selected_type = st.segmented_control(
        "",
        type_customization,
        selection_mode="multi",
        key="customized_selection",
        on_change=update_customization_selection,
        label_visibility = "collapsed",
    )


# 加料 Topping
if option_ingredient != 'NO' and "Topping" in selected_type:
    st.markdown("<p style='font-size:16px; color:DarkSlateBlue; font-weight:bold;'>Customize Your Topping</p>", unsafe_allow_html=True)
    
    st.markdown("<p margin-bottom: 0px; style='font-size:14px; color:DarkSlateBlue; font-weight:bold;'>Please select whether you want to add topping to your drink or not.</p>", unsafe_allow_html=True)
    whether_to_add_topping = st.toggle(
        "",
        value=True,
        key="add_topping",
        on_change=update_whether_to_add_topping,
        label_visibility="collapsed",
    )

    topping = ["檸檬 Lemon", "香橙 Orange", "甘蔗 Sugar cane", "春梅 Green Plum", "柚子 Yuzu/Pomelo", "珍珠 Golden Bubble/Pearl", "焙烏龍茶凍 Oolong Tea Jelly"]
    if whether_to_add_topping==True:
        selected_topping = st.pills(
            "", 
            topping, 
            selection_mode="multi",
            key="temp_topping_selection",
            label_visibility = "collapsed",
            )
        
        selected_topping_display = ""
        if len(selected_topping) >= 1:
            for i in range((len(selected_topping)-1)):
                selected_topping_display = selected_topping_display + str(selected_topping[i]) + ', '
            selected_topping_display = selected_topping_display + str(selected_topping[-1])
        else:
            selected_topping_display = ""
        
        st.markdown("Your selected topping: " + selected_topping_display + ".")
    else:
        st.markdown("You want a drink without topping.")
st.divider()

# 風味 taste
if option_ingredient != 'NO' and "Taste" in selected_type:
    st.markdown("<p style='font-size:16px; color:DarkSlateBlue; font-weight:bold;'>Choose the taste of the drink you prefer</p>", unsafe_allow_html=True)

    taste = ["清爽回甘 Refreshing & Sweet Tea Flavor", "醇濃茶香 Mellow Tea Flavor", "酸 Sour", "甜 Sweet", "酸甜 Sweet & Sour", "奶香 Milky Flavor"]
    selected_taste = st.pills(
        "", 
        taste, 
        selection_mode="multi",
        key="temp_taste_selection",
        label_visibility = "collapsed",
        )
    
    # display 所有使用者選擇的項目，實際上隨機從中選出一個給generator
    random_taste = ""
    selected_taste_display = ""

    if len(selected_taste) >= 1:
        random_taste = random.choice(selected_taste) # 從使用者選擇的一或多個項目中選出一個
        
        for i in range((len(selected_taste)-1)): # 設定顯示在頁面上的選項
            selected_taste_display = selected_taste_display + str(selected_taste[i]) + ', '
        selected_taste_display = selected_taste_display + str(selected_taste[-1])
        
        st.markdown("Your selected taste: " + selected_taste_display + ".")
    else:
        random_taste = ""
        selected_taste_display = ""
        st.markdown("You'll get random taste of drinks!")
st.divider()

# 口感 Texture
if option_ingredient != 'NO' and "Texture" in selected_type:
    st.markdown("<p style='font-size:16px; color:DarkSlateBlue; font-weight:bold;'>Choose the texture of the drink you prefer</p>", unsafe_allow_html=True)

    texture = ["果粒 Fruitiness", "濃厚 Thick", "嚼感 Chewiness",]
    selected_texture= st.pills(
        "", 
        texture, 
        selection_mode="multi",
        key="temp_texture_selection",
        label_visibility = "collapsed",
        )
    
    # display 所有使用者選擇的項目，實際上隨機從中選出一個給generator
    random_texture = ""
    selected_texture_display = ""

    if len(selected_texture) >= 1:
        random_texture = random.choice(selected_texture) # 從使用者選擇的一或多個項目中選出一個
        
        for i in range((len(selected_texture)-1)): # 設定顯示在頁面上的選項
            selected_texture_display = selected_texture_display + str(selected_texture[i]) + ', '
        selected_texture_display = selected_texture_display + str(selected_texture[-1])
        
        st.markdown("Your selected texture: " + selected_texture_display + ".")
    else:
        random_texture = ""
        selected_texture_display = ""
        st.markdown("You'll get random texture of drinks!")
st.divider()


# 我們將會從你的選擇中隨機選取1-x個(toppings) (x = 使用者的選擇數目 <=5 )
# We will randomly select 1-x (toppings) from your selection.


# 🎲 ✅ ✔️ ⚠️ 💸 🔥 🌟 🔄


# if st.button("✅ 確認配料與風味選擇"): # 之後要跟其他客製化項目合併？？？ 但為什麼覺得不需要加？
        

# --- option_ingredient 的區塊 ---




#---下方皆為舊版code 尚待改版---
#---下方皆為舊版code 尚待改版---
#---下方皆為舊版code 尚待改版---
st.divider()

# 初始化
if 'dice_rolled' not in st.session_state:
    st.session_state['dice_rolled'] = False
if 'add_to_fav' not in st.session_state:
    st.session_state['add_to_fav'] = False

    st.subheader("Random generator")
    
    # 🎲 點擊按鈕後，記住狀態
    if st.button('Roll the dice!'):
        st.session_state['dice_rolled'] = True
    
    if st.session_state['dice_rolled']:
        st.write('\# 執行基本的隨機function') # 這只是檢察功能暫放的東西

        # 連接好方程式之後要再改版這個區塊

        st.markdown(f"""
        <div style='font-size:20px; font-weight:bold;'>
        [store_name] Name_of_the_drink
        </div>
        """, unsafe_allow_html=True)
    
        # ------
       
        # 這裡要再加 Badge
        st.markdown(
        ":green-badge[:material/check: Success]"
        )
        #:orange-badge[⚠️ Needs review] :gray-badge[Deprecated]"
        
        
        col_price, col_calories = st.columns(2)
        with col_price:
            # 這邊之後要加上產出飲料的價位
            st.markdown(f"""
            <p style='margin-bottom: 2px; font-size:16px;'> 💸 Price </p>
            <p style='margin-bottom: 2px; font-size:24px; font-weight:bold;'> fstr_Price </p>
            """, unsafe_allow_html=True
            )


        with col_calories:
            # 這邊之後要加上產出飲料的熱量
            st.markdown(f"""
            <p style='margin-bottom: 2px; font-size:16px;'> 🔥 Calories </p>
            <p style='margin-bottom: 2px; font-size:24px; font-weight:bold;'> fstr_Calories </p>
            """, unsafe_allow_html=True
            )

        st.session_state['add_to_fav'] = st.toggle('Add to favorite?', key="toggle_fav")
        if st.session_state['add_to_fav']:
            st.success("🌟 已加入最愛！")

    # 如果按下reset 把'dice_rolled'和'add_to_fav'的session.state重置
    if st.button("🔄 Reset"):
        st.session_state['dice_rolled'] = False
        st.session_state['add_to_fav'] = False

#



else:
   st.empty()



