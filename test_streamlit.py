import streamlit as st

# This doesn't work, because button "pressed" state doesn't survive rerun, and pressing
# any button triggers a rerun.

st.write("# This doesn't work:")

if st.button("Button1_take1"):
    if st.button("Button2_take1"):
        if st.button("Button3_take1"):
            st.write("Button3")

# So, instead, we use session state to store the "pressed" state of each button, and
# make each button press toggle that entry in the session state.

st.write("# This works:")

# inilialize state to false all
if "button1" not in st.session_state:
    st.session_state["button1"] = False

if "button2" not in st.session_state:
    st.session_state["button2"] = False

if "button3" not in st.session_state:
    st.session_state["button3"] = False


if st.button("Button1"): 
    # "Button 1 is clicked" => st.session_state["button1"] = True
    st.session_state["button1"] = not st.session_state["button1"] 


if st.session_state["button1"]:
    # Button 2 will show up
    if st.button("Button2"):
        # "Button 2 is clicked" => st.session_state["button2"] = True
        st.session_state["button2"] = not st.session_state["button2"]

if st.session_state["button1"] and st.session_state["button2"]:
    # Button 3 will show up unless both state of button 1 and 2 is True
    if st.button("Button3"):
        # toggle button3 session state
        # "Button 3 is clicked" => st.session_state["button3"] = True
        st.session_state["button3"] = not st.session_state["button3"]

if st.session_state["button3"]: # st.session_state["button3"] = True => show result

    st.write("**Button3!!!**")


# Print the session state to make it easier to see what's happening
st.write(
    f"""
    ## Session state:
    {st.session_state["button1"]=}

    {st.session_state["button2"]=}

    {st.session_state["button3"]=}
    """
)