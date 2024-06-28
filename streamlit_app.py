# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
	"Choose the fruit you want in your custom smoothie!"
)
#option = st.selectbox(
#	'What is your favourite fruit?',
#	('Banana','Strawberries','Peaches'))
#st.write('Your favourite fruit is: ', option)
name_on_order= st.text_input("Name on the smootie:")
st.write("Name on the Smoothie will be : ", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list= st.multiselect(
	'Choose upto 5 ingredients: '
	,my_dataframe
	,max_selections=5
)
if ingredients_list:
	#st.write(ingredients_list)
	#st.text(ingredients_list)
	ingredients_string = ''
	for fruit_chosen in ingredients_list:
		ingredients_string += fruit_chosen+' '

	my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS,NAME_ON_ORDER)
			values ('""" + ingredients_string + """','"""+ name_on_order +"""')"""
	
	#st.write(my_insert_stmt)
	time_to_insert=st.button("Submit")
	if time_to_insert:
		if ingredients_string:
			session.sql(my_insert_stmt).collect()
			#st.write(my_insert_stmt)
		
		st.success('Your Smoothie is ordered!', icon="✅")
