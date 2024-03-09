# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

session = get_active_session()

# Write directly to the app
st.title(":balloon: Pind Bhatura Menu :balloon:")
st.write(
    """Where Food Meets Family:
    """
)

name_on_order = st.text_input('Name on Order : ')
st.write('Your Order Name will be : ', name_on_order)

my_df_cat = session.table("Pind_bhatura.public.Punjabi_menu").select(col('Category')).distinct()
pb_options = st.selectbox(
    'Select category of Food : '
    ,my_df_cat
)
st.write(pb_options)
if my_df_cat :
   my_df_cat2 = session.table("Pind_bhatura.public.Punjabi_menu").select(col('item_name')).filter(col('Category') == pb_options)
   pb_options1 = st.multiselect(
    'Select Food Item to Order : '
    ,my_df_cat2
)
   if pb_options1:
       item_list = ' '
       for item_chosen in pb_options1:
           item_list += item_chosen + ' '
       st.write(item_list)
       my_insert_stmt = """insert into pind_bhatura.public.pind_bhatura_orders(name_on_order,ingredients) values ('"""+name_on_order+"""','"""+item_list+"""')"""
       time_to_insert1 = st.button('Submit Order')
       st.write(my_insert_stmt)
       if time_to_insert1 :
           session.sql(my_insert_stmt).collect()
           st.success('Your Food is ordered '+ name_on_order,icon="✅")
#created_dataframe = session.create_dataframe(
    #[[50, 25, "Q1"], [20, 35, "Q2"], [hifives_val, 30, "Q3"]],
    #schema=["HIGH_FIVES", "FIST_BUMPS", "QUARTER"],
#)
