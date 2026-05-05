# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
  "Choose the fruits you want in your custom Smoothie"
)

# option = st.selectbox(
#     "What is your favirout fruit?",
#     ("Banana","Strawberries","Peaches"),
# )

# st.write("You selected:", option)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input('Name on Smoothie:')


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
)

if ingredients_list:

    ingredients_string = ''

    for fruit_choose in ingredients_list:
        ingredients_string += fruit_choose + ' '


time_to_insert = st.button('Submit Button')

if time_to_insert:
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    session.sql(my_insert_stmt).collect()

    st.success('Your Smoothie is ordered!', icon="✅")
