import streamlit as st

st.title(":cup_with_straw: The Destined Pour")
st.header("Select the generator mode you want!")

if 'calories_customized' not in st.session_state:
    st.session_state['calories_customized'] = 'NO'
if 'price_customized' not in st.session_state:
    st.session_state['price_customized'] = 'NO'
if 'ingredient_customized' not in st.session_state:
    st.session_state['ingredient_customized'] = 'NO'


def calories_on_change():
    st.session_state['calories_customized'] = st.session_state["calories_temp"]

# st.markdown("<p style='font-size:16px; color:Black; font-weight:bold;'>1. Do you want to customize the “calories” of your drinks?</p>", unsafe_allow_html=True)
option_calories = st.radio(
    ":one: Do you want to customize the “calories” of your drinks?",
    [":rainbow[YES]", "NO",],
    key="calories_temp",
    index=1,
    on_change=calories_on_change,
    horizontal=True,
)
# if option_calories == ':rainbow[YES]':


def price_on_change():
    st.session_state['price_customized'] = st.session_state["price_temp"]

option_price = st.radio(
    ":two: Do you want to customize the “price” of your drinks?",
    [":rainbow[YES]", "NO",], 
    key="price_temp",   
    index=1,
    on_change=price_on_change,
    horizontal=True,
)



option_ingredient = st.radio(
    ":three: Do you want to customize the “ingredient” of your drinks?",
    [":rainbow[YES]", "NO",],    
    index=1,
    horizontal=True,
)


if option_calories == 'NO' and option_price == 'NO' and option_ingredient == 'NO':
    st.markdown(f"""
    <div style='font-size:18px; font-weight:bold;'>
    ✔️ You selected: Random generator </div>""",
    unsafe_allow_html=True)

else: # 還沒改好 要可以適應上面的選項
    st.markdown(f"""
    <div style='font-size:18px; font-weight:bold;'>
    ✔️ You selected: ? </div>""",
    unsafe_allow_html=True)


st.divider()

if option_calories == ':rainbow[YES]':
    budget = st.slider(
    "Schedule your appointment:", 1,1000,50)
    st.write("You're scheduled for:", budget)


#下方皆為舊版code
st.markdown("<p style='font-size:20px; color:DarkMagenta; font-weight:bold;'>Which mode would you like to try?</p>", unsafe_allow_html=True)
option = st.selectbox(
    "",
    ("Random generator", "Calories", "Price", "Ingredient"),
    index=None, 
    placeholder=" Select generator method... ", 
    label_visibility="collapsed"
)



if option != None:
    st.markdown(f"""
    <div style='font-size:18px; font-weight:bold;'>
    ✔️ You selected: {option} </div>""",
    unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div style='font-size:18px; font-weight:bold;'>
    You should select the generator mode 🎲
    </div>""", unsafe_allow_html=True)

st.divider()

# 初始化
if 'dice_rolled' not in st.session_state:
    st.session_state['dice_rolled'] = False
if 'add_to_fav' not in st.session_state:
    st.session_state['add_to_fav'] = False

if option == "Random generator":
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
        


elif option == "Calories":
    st.subheader("Calories")



elif option == "Price":
    st.subheader("Price")



elif option == "Ingredient":
    st.subheader("Ingredient")


else:
   st.empty()

