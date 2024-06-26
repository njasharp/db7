import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Gaming Trends Dashboard", layout="wide")
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    body {background-color: #212121;}
    </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html=True)


# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("mena_ex.csv")

df = load_data()

# Set up the main page
st.title("Gaming Trends in MENA Expanded")

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

# Display additional data for Population, Language, and Market Size


pop_mena_df = pd.read_csv("pop_mena.csv")

# Plot Population Data
def plot_population():
    fig, ax = plt.subplots()
    ax.barh(pop_mena_df['Region'], pop_mena_df['Population M'], color='blue')
    ax.set_title('Population by Region')
    st.pyplot(fig)

# Plot Market Size Data
def plot_market_size():
    fig, ax = plt.subplots()
    ax.barh(pop_mena_df['Region'], pop_mena_df['Market Size ($M)'], color='orange')
    ax.set_title('Market Size by Region ($M)')
    st.pyplot(fig)

# Plot Language Data
def plot_language():
    # Count occurrences of languages
    language_counts = pop_mena_df['Language/s'].str.split(', ').explode().value_counts()
    fig, ax = plt.subplots()
    ax.barh(language_counts.index, language_counts.values, color='purple')
    ax.set_title('Languages by Region')
    st.pyplot(fig)

# Plot Region by Languages Data
def plot_region_by_language():
    fig, ax = plt.subplots()
    # Expand language counts to one row per language
    expanded_languages = pop_mena_df.set_index(['Region']).explode('Language/s').reset_index()
    # Calculate the size of each bubble
    language_region_counts = expanded_languages.groupby(['Language/s', 'Region']).size().reset_index(name='Counts')
    # Create a scatter plot
    scatter = ax.scatter(language_region_counts['Language/s'], language_region_counts['Region'],
                         s=language_region_counts['Counts']*100, alpha=0.5, color='brown')
    ax.set_title('Region by Languages')
    ax.set_ylabel('Region')
    ax.set_xlabel('Language')
    plt.xticks(rotation=90, fontsize=8)  # Rotate and set smaller font size for x-axis labels
    st.pyplot(fig)

# Display population, market size, language, and region by language charts
st.subheader("Additional Data")
plot_population()
plot_market_size()
plot_language()
plot_region_by_language()

# Display raw data
if st.checkbox("Show Raw Data filtered"):
    st.subheader("Raw Data")
    st.write(filtered_df)

if st.checkbox("Show Raw Data more "):
    st.subheader("Raw Data more")
    st.write(pop_mena_df)
st.markdown("mobile")  
st.info("built by dw v1 6-26")