import streamlit as st

st.title(":cup_with_straw: The Destined Pour")
st.header(
"Select the generator mode you want!"
)

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
    ✔️ You selected: {option}
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div style='font-size:18px; font-weight:bold;'>
    You should select the generator mode 🎲
    </div>
    """, unsafe_allow_html=True)

st.divider()

if option == "Random generator":
    st.subheader("Random generator")
    
