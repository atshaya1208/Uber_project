import streamlit as st
import pandas as pd

st.title("UBER EATS BANGALORE RESTAURANT INTELLIGENCE AND DECISION")

option = st.selectbox("Which dataset would you like to view?",("Dashboard", "Q&A", "Order Analysis"))
st.write(f"You selected: {option}")

if option == "Dashboard":
    @st.cache_data
    def load_data():
        try:
            df = pd.read_csv("uber_cleaned_data.csv")
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None
    df = load_data()

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
    
    st.title("UBER EATS BANGALORE RESTAURANT INTELLIGENCE AND DECISION")
    st.header("Q&A page")

    with st.expander("Which Bangalore locations have the highest average restaurant ratings?"):
        df = pd.DataFrame({
            "location":["lavelle road ","koramangala 5th block","cunningham road ","st. marks road","koramangala 3rd block"],
            "ratings" :["4.21","4.19","4.15","4.15","4.14"]      
        })
        st.dataframe(df)

    with st.expander("Which locations are over-saturated with restaurants?"):
        df = pd.DataFrame({
            "location":["koramangala 5th block","indiranagar","btm","hsr","whitefield"],
            "count":["1323","1208","939","897","803"],
            "votes":[" 1,988,751"," 1,116,774"," 360,829"," 399,574","440,219"]
        })
        st.dataframe(df)

    with st.expander("Does online ordering improve restaurant ratings?"):
        df = pd.DataFrame({
            "online_order":["no","yes"],
            "count":["5388","12599"],
            "ratings":["3.97","3.91"]
        })
        st.dataframe(df)

    with st.expander("Does table booking correlate with higher customer ratings?"):
        df = pd.DataFrame({
            "book_table":["no","yes"],
            "ratings":["3.8","4.2"]
        })
        st.dataframe(df)

    with st.expander("What price range delivers the best customer satisfaction?"):
        df = pd.DataFrame({
            "price_range":["PREMIUM(>1500)","HIGH-RANGE(800-1500)","MEDIUM-RANGE(400-800)","LOW-RANGE(<400)"],
            "total_restaurants":["1327","4327","9363","2970"],
            "sum(votes)":["2,069,727","5,265,056","4,448,073","603,161"]
        })
        st.dataframe(df)

    with st.expander("How do low, mid, and premium-priced restaurants perform in terms of ratings?"):
        df = pd.DataFrame({
            "price_segmant":["PREMIUM(>1000)","MID-RANGE(400-1000)","LOW-RANGE(<400)"],
            "total_restaurants":["4086","10931","2970"],
            "ratings":["4.2","3.9","3.8"]
        })
        st.dataframe(df)

    with st.expander("Which cuisines are most common in Bangalore?"):
        df = pd.DataFrame({
            "cuisines":["north indian","north indian","north indian,chinese"],
            "count":["71","66","60"],
            "location":["btm","whitefield","btm"]
        })
        st.dataframe(df)

    with st.expander("Which cuisines receive the highest average ratings?"):
        df = pd.DataFrame({
            "cuisines":["asian, chinese, thai, momos","asian, mediterranean, north indian, bbq","continental, north indian, chinese, european, bbq, finger food, asian","continental, north indian, italian, south indian, finger food ","european, mediterranean, north indian, bbq","healthy food, salad, mediterranean","north indian, european, mediterranean, bbq"],
            "count":["19","6","10","6","18","1","5"],
            "ratings":["4.9","4.8","4.8","4.9","4.8","4.9","4.8"]
        })
        st.dataframe(df)

    with st.expander("Which locations show high demand but lower average ratings?"):
        df = pd.DataFrame({
            "location":["marathahalli","bellandur","bannerghatta road","electronic city"],
            "count":["652","430","402","317"],
            "ratings":["3.74","3.7","3.72","3.7"]
        })
        st.dataframe(df)

    with st.expander("Do restaurants offering both online ordering and table booking perform better?"):
        df = pd.DataFrame({
            "online_order":["yes","no","yes","no"],
            "book_table":["yes","yes","no","no"],
            "count":["3088","2182","9511","3206"],
            "ratings":["4.2","4.2","3.8","3.8"],
            "sum(votes)":["3,994,638","2,817,463","3,786,633","1,827,283"]
        })
        st.dataframe(df)
        
if option == "Order Analysis":
    st.title("UBER EATS BANGALORE RESTAURANT INTELLIGENCE AND DECISION")
    st.header("Order Analysis Q&A page")

    with st.expander("Which Bangalore restaurant has high number of orders?"):
        df = pd.DataFrame({
            "restaurant_name":["caf morish","caf secret alley","khan saheb grills and rolls","moto store caf","mums kitchen","urban solace caf for the soul"],
            "total_orders":["29","25","25","21","22","21"]   
        })
        st.dataframe(df)

    with st.expander("Which payment method is most common in ordering food?"):
        df = pd.DataFrame({
            "payment_method":["card","cash","upi"],
            "count":["8364","8384","8252"]
        })
        st.dataframe(df)

    with st.expander("How many of them used discounts?"):
        df = pd.DataFrame({
            "discount_used":["no","yes"],
            "count":["12509","12491"]
        })
        st.dataframe(df)
    
    with st.expander("In which day orders count incresed(weekday/weekend)?"):
        df = pd.DataFrame({
            "day":["Thursday","Monday","Wednesday","Tuesday","Friday","Saturday","Sunday"],
            "total_orders":["3623","3613","3598","3596","3567","3505","3498"]
        })
        st.dataframe(df)

    with st.expander("In which restaurant used most discounts?"):
        df = pd.DataFrame({
            "restaurant_name":["caf morish","khan saheb grills and rolls","kesar sweet shop and fast food","pingara","moto store caf"],
            "count":["17","16","13","12","12"]
        })
        st.dataframe(df)
