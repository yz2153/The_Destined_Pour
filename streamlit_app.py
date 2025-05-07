import streamlit as st

st.title(":cup_with_straw: The Destined Pour")
st.header("Select the generator mode you want!")

st.markdown("<p style='font-size:20px; color:DarkMagenta; font-weight:bold;'>Which mode would you like to try?</p>", unsafe_allow_html=True)
option = st.selectbox(
    "",
    ("Random generator", "Calories", "Price", "Ingredient"),
    index=None, 
    placeholder=" Select generator method... ", 
    label_visibility="collapsed"
)

st.write(":ideograph_advantage:")

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