import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Basic page setup
st.title("📊 Teacher Rating System")
st.write("Rate teachers (1-5 stars)")

# Rating form
with st.form("rate_form"):
    teacher = st.selectbox("Select Teacher", ["galagali sir", "maigur maam", "surpur maam","tilavalli sir"])
    rating = st.radio("Your Rating", [1, 2, 3, 4, 5], horizontal=True)
    if st.form_submit_button("Submit"):
        # Save rating to CSV
        new_data = [[teacher, rating, datetime.now().strftime("%Y-%m-%d")]]
        pd.DataFrame(new_data, columns=["Teacher", "Rating", "Date"]).to_csv(
            "ratings.csv", mode="a", header=not os.path.exists("ratings.csv"), index=False
        )
        st.success("Thanks for your rating!")

# Display monthly results
st.header("This Month's Results")

if os.path.exists("ratings.csv"):
    # Read and process data
    df = pd.read_csv("ratings.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    current_month = datetime.now().strftime("%Y-%m")
    monthly_ratings = df[df["Date"].dt.strftime("%Y-%m") == current_month]
    
    if not monthly_ratings.empty:
        # Calculate averages
        avg_ratings = monthly_ratings.groupby("Teacher")["Rating"].mean().round(1)
        best_teacher = avg_ratings.idxmax()
        best_score = avg_ratings.max()
        
        # Show results
        st.write("Average Ratings:")
        st.bar_chart(avg_ratings)
        st.success(f"🏆 Best Teacher: {best_teacher} ({best_score}/5)")
    else:
        st.info("No ratings yet this month")
else:
    st.info("No ratings submitted yet")