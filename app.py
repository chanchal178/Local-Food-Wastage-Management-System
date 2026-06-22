import mysql.connector
import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="Local Food Wastage Management System",
    page_icon="🍲",
    layout="wide"
)

# Load Data
providers = pd.read_csv("providers_data.csv")
receivers = pd.read_csv("receivers_data.csv")
food = pd.read_csv("food_listings_data.csv")
claims = pd.read_csv("claims_data.csv")

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="food_waste_db"
    )

# Title
st.title("🍲 Local Food Wastage Management System")

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.selectbox(
    "Select Page",
    [
        
    
    "Dashboard",
    "Food Listings",
    "Providers",
    "Receivers",
    "Claims",
    "SQL Queries",
    "CRUD"


    ]
)

# DASHBOARD
if page == "Dashboard":

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Providers", len(providers))

    with col2:
        st.metric("Receivers", len(receivers))

    with col3:
        st.metric("Food Listings", len(food))

    with col4:
        st.metric("Claims", len(claims))

    st.markdown("---")

    st.subheader("Food Listings Data")
    st.dataframe(food.head(20))

    # Food Type Distribution
    st.subheader("Food Type Distribution")

    food_chart = food["Food_Type"].value_counts().reset_index()
    food_chart.columns = ["Food_Type", "Count"]

    fig1 = px.pie(
        food_chart,
        names="Food_Type",
        values="Count",
        title="Food Type Distribution"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Meal Type Distribution
    st.subheader("Meal Type Distribution")

    meal_chart = food["Meal_Type"].value_counts().reset_index()
    meal_chart.columns = ["Meal_Type", "Count"]

    fig2 = px.bar(
        meal_chart,
        x="Meal_Type",
        y="Count",
        title="Meal Type Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Claim Status Distribution
    st.subheader("Claim Status Distribution")

    claim_chart = claims["Status"].value_counts().reset_index()
    claim_chart.columns = ["Status", "Count"]

    fig3 = px.pie(
        claim_chart,
        names="Status",
        values="Count",
        title="Claim Status Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

# FOOD LISTINGS
elif page == "Food Listings":

    st.header("Food Listings")

    city = st.selectbox(
        "Select City",
        sorted(food["Location"].dropna().unique())
    )

    food_type = st.selectbox(
        "Select Food Type",
        sorted(food["Food_Type"].dropna().unique())
    )

    meal_type = st.selectbox(
        "Select Meal Type",
        sorted(food["Meal_Type"].dropna().unique())
    )

    filtered_food = food[
        (food["Location"] == city)
        & (food["Food_Type"] == food_type)
        & (food["Meal_Type"] == meal_type)
    ]

    st.dataframe(filtered_food)

# PROVIDERS
elif page == "Providers":

    st.header("Providers Details")

    city = st.selectbox(
        "Select Provider City",
        sorted(providers["City"].dropna().unique())
    )

    filtered_provider = providers[
        providers["City"] == city
    ]

    st.dataframe(filtered_provider)

# RECEIVERS
elif page == "Receivers":

    st.header("Receivers Details")

    city = st.selectbox(
        "Select Receiver City",
        sorted(receivers["City"].dropna().unique())
    )

    filtered_receiver = receivers[
        receivers["City"] == city
    ]

    st.dataframe(filtered_receiver)

# CLAIMS
elif page == "Claims":

    st.header("Claims Details")

    status = st.selectbox(
        "Select Claim Status",
        sorted(claims["Status"].dropna().unique())
    )

    filtered_claims = claims[
        claims["Status"] == status
    ]

    st.dataframe(filtered_claims)
# SQL QUERIES
elif page == "SQL Queries":

    st.header("SQL Query Results")

    st.subheader("1. Providers in Each City")
    st.dataframe(
        providers.groupby("City")
        .size()
        .reset_index(name="Total_Providers")
    )

    st.subheader("2. Receivers in Each City")
    st.dataframe(
        receivers.groupby("City")
        .size()
        .reset_index(name="Total_Receivers")
    )

    st.subheader("3. Food Contribution by Provider Type")
    st.dataframe(
        food.groupby("Provider_Type")["Quantity"]
        .sum()
        .reset_index()
        .sort_values("Quantity", ascending=False)
    )

    st.subheader("4. Total Food Available")
    st.write(food["Quantity"].sum())

    st.subheader("5. Food Type Distribution")
    st.dataframe(
        food.groupby("Food_Type")
        .size()
        .reset_index(name="Count")
    )

    st.subheader("6. Claim Status Count")
    st.dataframe(
        claims.groupby("Status")
        .size()
        .reset_index(name="Count")
    )
# CRUD PAGE
elif page == "CRUD":

    st.header("CRUD Operations")

    action = st.selectbox(
        "Select Operation",
        ["Create", "Update", "Delete", "View Records"]
    )

    # CREATE
    if action == "Create":

        food_id = st.number_input("Food ID", min_value=1)
        food_name = st.text_input("Food Name")
        quantity = st.number_input("Quantity", min_value=1)
        expiry_date = st.text_input("Expiry Date (YYYY-MM-DD)")
        provider_id = st.number_input("Provider ID", min_value=1)
        provider_type = st.text_input("Provider Type")
        location = st.text_input("Location")

        food_type = st.selectbox(
            "Food Type",
            ["Vegetarian", "Non-Vegetarian", "Vegan"]
        )

        meal_type = st.selectbox(
            "Meal Type",
            ["Breakfast", "Lunch", "Dinner", "Snacks"]
        )

        if st.button("Add Food"):

            conn = get_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO food_listings
            (Food_ID, Food_Name, Quantity, Expiry_Date,
            Provider_ID, Provider_Type, Location,
            Food_Type, Meal_Type)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

            values = (
                food_id,
                food_name,
                quantity,
                expiry_date,
                provider_id,
                provider_type,
                location,
                food_type,
                meal_type
            )

            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()

            st.success("Record Added Successfully!")

    # UPDATE
    elif action == "Update":

        food_id = st.number_input(
            "Food ID to Update",
            min_value=1
        )

        new_quantity = st.number_input(
            "New Quantity",
            min_value=1
        )

        if st.button("Update Record"):

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE food_listings
                SET Quantity=%s
                WHERE Food_ID=%s
                """,
                (new_quantity, food_id)
            )

            conn.commit()

            cursor.close()
            conn.close()

            st.success("Record Updated Successfully!")

    # DELETE
    elif action == "Delete":

        food_id = st.number_input(
            "Food ID to Delete",
            min_value=1
        )

        if st.button("Delete Record"):

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM food_listings
                WHERE Food_ID=%s
                """,
                (food_id,)
            )

            conn.commit()

            cursor.close()
            conn.close()

            st.success("Record Deleted Successfully!")

    # VIEW
    elif action == "View Records":

        conn = get_connection()

        query = """
        SELECT *
        FROM food_listings
        ORDER BY Food_ID DESC
        LIMIT 50
        """

        df = pd.read_sql(query, conn)

        st.dataframe(df)

        conn.close()