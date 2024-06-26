import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Gaming Trends Dashboard", layout="wide")

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("mena_ex.csv")

df = load_data()

# Set up the main page
st.title("Gaming Trends in MENA Expanded")
st.markdown("mobile")
# Country selector (radio buttons)
default_countries = ["Saudi Arabia", "UAE", "Egypt", "Morocco", "Iraq"]
selected_country = st.sidebar.radio(
    "Select Country",
    options=df['Country'].unique(),
    index=list(df['Country'].unique()).index(default_countries[0])  # Default to Saudi Arabia
)

# Filter data based on selected country
filtered_df = df[df['Country'] == selected_country]

# Function to clean and format data items
def clean_data_items(data):
    cleaned_items = [item.split(". ", 1)[1] if ". " in item else item for item in data]
    return cleaned_items

# Function to display top 5 list
def display_top_5(data, title):
    st.subheader(title)
    cleaned_items = clean_data_items(data)
    for i, item in enumerate(cleaned_items):
        st.write(f"{i+1}. {item}")
    st.write("---")

# Function to plot top 5 list as bar chart
def plot_top_5(data, title):
    cleaned_items = clean_data_items(data)
    values = [5, 4, 3, 2, 1]  # Correct order to show top items at the top
    fig, ax = plt.subplots()
    ax.barh(cleaned_items, values, color='green')
    ax.set_xticks([])  # Remove the x-axis labels
    ax.set_title(title)
    ax.invert_yaxis()  # Reverse the order of the y-axis
    st.pyplot(fig)

# Display top 5 lists
engagement_data = filtered_df['Top Games (Engagement)'].tolist()
monetization_data = filtered_df['Top Games (Monetization)'].tolist()
genres_data = filtered_df['Top Genres'].tolist()
publishers_data = filtered_df['Top Publishers'].tolist()
trends_data = filtered_df['Emerging Trends'].tolist()

col1, col2 = st.columns(2)

with col1:
    display_top_5(engagement_data, f"Top Games (Engagement) - {selected_country}")
    plot_top_5(engagement_data, f"Top Games (Engagement) - {selected_country}")

    display_top_5(genres_data, f"Top Genres - {selected_country}")
    plot_top_5(genres_data, f"Top Genres - {selected_country}")

    display_top_5(trends_data, f"Emerging Trends - {selected_country}")
    plot_top_5(trends_data, f"Emerging Trends - {selected_country}")

with col2:

    display_top_5(monetization_data, f"Top Games (Monetization) - {selected_country}")
    plot_top_5(monetization_data, f"Top Games (Monetization) - {selected_country}")    

    display_top_5(publishers_data, f"Top Publishers - {selected_country}")
    plot_top_5(publishers_data, f"Top Publishers - {selected_country}")



# Display raw data
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.write(filtered_df)

st.info("built by dw v1 6-26")