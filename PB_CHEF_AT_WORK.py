# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col,when_matched
import requests

# Write directly to the app
st.title(" :cup_with_straw: Chef At Work :cup_with_straw: ")
st.write(
    """Orders That need to be filled
    """
)

# Get the current credentials
#session = get_active_session()

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("pind_bhatura.public.pind_bhatura_orders").filter(col("order_filled")==0).collect()
editable_df = st.experimental_data_editor(my_dataframe)
#st.dataframe(data=editable_df, use_container_width=True)

submitted = st.button('Submit')

if submitted :
    st.success("Someone Clicked the Button.")
    og_dataset = session.table("pind_bhatura.public.pind_bhatura_orders")
    edited_dataset = session.create_dataframe(editable_df)
    og_dataset.merge(edited_dataset
                    , (og_dataset['order_uid'] == edited_dataset['order_uid'])
                    , [when_matched().update({'order_filled': edited_dataset['order_filled']})]
                    )
