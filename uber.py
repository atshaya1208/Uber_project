import streamlit as st
import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="project_uber_eats",
    port="3306"
)

st.title("UBER EATS BANGALORE RESTAURANT INTELLIGENCE AND DECISION")

option = st.selectbox("Which dataset would you like to view?",("Dashboard", "Q&A", "Order Analysis"))
st.write(f"You selected: {option}")

if option == "Dashboard":
    query = "SELECT * FROM uber_cleaned_data"
    df = pd.read_sql(query, mydb)
    st.dataframe(df)
    query1 = "SELECT * FROM order_data"
    df1 = pd.read_sql(query1, mydb)
    st.dataframe(df1)


    selected_location = st.sidebar.text_input("Search loaction", "")

    if "name" in df.columns:
        unique_name = sorted(df['name'].dropna().unique())
        selected_name = st.sidebar.multiselect("Select name", unique_name, default=[])
    else:
        selected_name=[]

    min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.5, step=0.1)

    amount = st.sidebar.slider("amount", 0, 3000, 100, step=100)

    filtered_df = df.copy()

    if selected_location:
        filtered_df = filtered_df[filtered_df['location'].str.contains(selected_location, case=False, na=False)]


    if selected_name:
        filtered_df = filtered_df[filtered_df['name'].isin(selected_name)]

    filtered_df = filtered_df[filtered_df['rate'] >= min_rating]

    filtered_df = filtered_df[filtered_df['cost_for_two_people'] >= amount]

    st.write(f"Showing **{len(filtered_df)}** restaurants matching your criteria:")
    st.dataframe(filtered_df, width=True)

    if not filtered_df.empty:
        top_restaurant = filtered_df.sort_values(by='rate', ascending=False).iloc[0]
        st.success(f"Top rated restaurant based on selection: **{top_restaurant['name']}** with a {top_restaurant['rate']} rate!")
    else:
        st.warning("No restaurants found. Try adjusting your filters.")

if option == "Q&A":
    
    st.header("Q&A page")

    with st.expander("Which Bangalore locations have the highest average restaurant ratings?"):
        query = "SELECT location, round(AVG(rate),2) FROM uber_cleaned_data GROUP BY location ORDER BY AVG(rate) DESC LIMIT 10"
        df = pd.read_sql(query, mydb)

        st.dataframe(df)


    with st.expander("Which locations are over-saturated with restaurants?"):
        query = """SELECT location, count(*), FORMAT(SUM(votes),0) 
                FROM uber_cleaned_data 
                GROUP BY location HAVING count(*) > 200 
                ORDER BY count(*) DESC LIMIT 10"""
        df = pd.read_sql(query, mydb)
       
        st.dataframe(df)

    with st.expander("Does online ordering improve restaurant ratings?"):
        query = "SELECT online_order, count(*), round(AVG(rate),2) FROM uber_cleaned_data GROUP BY online_order"
        df = pd.read_sql(query, mydb)
        
        st.dataframe(df)

    with st.expander("Does table booking correlate with higher customer ratings?"):
        query = "SELECT book_table, round(AVG(rate),1) FROM uber_cleaned_data GROUP BY book_table"

        df = pd.read_sql(query, mydb)
        st.dataframe(df)

    with st.expander("What price range delivers the best customer satisfaction?"):
        query = """SELECT 
	CASE 
        WHEN `cost_for_two_people` < 400 THEN 'LOW-RANGE (<400)'
        WHEN `cost_for_two_people` BETWEEN 400 AND 800 THEN 'MEDIUM-RANGE (400-800)'
		WHEN `cost_for_two_people` BETWEEN 800 AND 1500 THEN 'HIGH-RANGE (800-1500)'
        ELSE 'PREMIUM (>1500)'
    END as price_range,
    COUNT(*) AS total_restaurants, FORMAT(SUM(votes),0) FROM uber_cleaned_data GROUP BY price_range ORDER BY FORMAT(sum(votes),0) """
        
        df = pd.read_sql(query, mydb)
        st.dataframe(df)

    with st.expander("How do low, mid, and premium-priced restaurants perform in terms of ratings?"):
        query = """SELECT 
	CASE 
        WHEN `cost_for_two_people` < 400 THEN 'LOW-RANGE (<400)'
        WHEN `cost_for_two_people` BETWEEN 400 AND 1000 THEN 'MID-RANGE (400-1000)'
        ELSE 'PREMIUM (>1000)'
    END as price_segmant,
    COUNT(*) AS total_restaurants, ROUND(AVG(rate),1) FROM uber_cleaned_data GROUP BY price_segmant ORDER BY ROUND(AVG(rate),1) DESC"""
       
        df = pd.read_sql(query, mydb)
        st.dataframe(df)

    with st.expander("Which cuisines are most common in Bangalore?"):
        query = "SELECT cuisines, count(*), location FROM uber_cleaned_data GROUP BY cuisines, location ORDER BY count(*) DESC limit 20" 

        df = pd.read_sql(query, mydb)
        st.dataframe(df)

    with st.expander("Which cuisines receive the highest average ratings?"):
        query = "SELECT cuisines, count(*), round(AVG(rate),1) FROM uber_cleaned_data GROUP BY cuisines HAVING AVG(rate)> 4.75"

        df = pd.read_sql(query, mydb)
        st.dataframe(df)

    with st.expander("Which locations show high demand but lower average ratings?"):
        query = """SELECT location, COUNT(*), ROUND(AVG(rate),2)
    FROM uber_cleaned_data 
    GROUP BY location HAVING COUNT(*)>300 AND AVG(rate)<3.8 
    ORDER BY count(*) DESC"""

        df = pd.read_sql(query, mydb)
        st.dataframe(df)

    with st.expander("Do restaurants offering both online ordering and table booking perform better?"):
        query = """SELECT online_order, book_table, count(*), ROUND(AVG(rate),1), FORMAT(SUM(votes),0) 
    FROM uber_cleaned_data 
    GROUP BY online_order, book_table 
    ORDER BY ROUND(AVG(rate),1) DESC"""

        df = pd.read_sql(query, mydb)
        st.dataframe(df)
        
if option == "Order Analysis":
    
    st.header("Order Analysis Q&A page")

    with st.expander("Which Bangalore restaurant has high number of orders?"):
        query1 = "SELECT restaurant_name, count(order_id) as total_orders FROM order_data GROUP BY restaurant_name HAVING total_orders>20"

        df1 = pd.read_sql(query1, mydb)
        st.dataframe(df1)

    with st.expander("Which payment method is most common in ordering food?"):
        query1 = "SELECT payment_method, count(*) FROM order_data GROUP BY payment_method"

        df1 = pd.read_sql(query1, mydb)
        st.dataframe(df1)

    with st.expander("How many of them used discounts?"):
        query1 = "SELECT discount_used, count(*) FROM order_data GROUP BY discount_used"

        df1 = pd.read_sql(query1, mydb)
        st.dataframe(df1)
    
    with st.expander("In which day orders count incresed(weekday/weekend)?"):
        query1 = "SELECT DAYNAME(order_date), COUNT(order_id) AS total_orders FROM order_data GROUP BY DAYNAME(order_date) ORDER BY total_orders DESC"

        df1 = pd.read_sql(query1, mydb)
        st.dataframe(df1)

    with st.expander("In which restaurant used most discounts?"):
        query1 = "SELECT restaurant_name, count(*) FROM order_data WHERE discount_used = 'yes' GROUP BY restaurant_name ORDER BY count(*) DESC"

        df1 = pd.read_sql(query1, mydb)
        st.dataframe(df1)

        mydb.close()