# Importing Libraries
import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

# Setting up page configuration
icon = Image.open("images.jpg")
st.set_page_config(page_title="Airbnb Analysis",
                   page_icon=icon,
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'About': """# This dashboard app is created by *Jafar Hussain*!
                                        Data has been gathered from MongoDB Atlas"""}
                  )

# Creating option menu in the sidebar
with st.sidebar:
    selected = option_menu("Menu", ["Home", "Overview", "Explore"], 
                           icons=["house", "graph-up-arrow", "bar-chart-line"],
                           menu_icon="menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                                   "nav-link-selected": {"background-color": "#FF5A5F"}}
                          )

# Connecting to MongoDB Atlas and retrieving the data
client = pymongo.MongoClient("mongodb+srv://usersha:Maja@cluster0.8syjnh2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.sample_airbnb
collection = db.listingsAndReviews

# Reading the cleaned dataframe
df = pd.read_csv('Airbnb_data.csv')

# HOME PAGE
if selected == "Home":
    col1, col2 = st.columns(2, gap='medium')
    col1.markdown("## :blue[Domain]: Travel Industry, Property Management, and Tourism")
    col1.markdown("## :blue[Technologies used]: Python, Pandas, Plotly, Streamlit, MongoDB")
    col1.markdown("## :blue[Overview]: Analyze Airbnb data using MongoDB Atlas, perform data cleaning, create visualizations, and generate insights into pricing, availability, and trends.")
    col2.markdown("#   ")
    col2.markdown("#   ")
    col2.image("images.jpg")

# OVERVIEW PAGE
if selected == "Overview":
    tab1, tab2 = st.tabs(["$\huge 📝 RAW DATA $", "$\huge🚀 INSIGHTS $"])

    # RAW DATA TAB
    with tab1:
        col1, col2 = st.columns(2)
        if col1.button("Click to view Raw data"):
            col1.write(collection.find_one())
        if col2.button("Click to view Dataframe"):
            col1.write(collection.find_one())
            col2.write(df)

    # INSIGHTS TAB
    with tab2:
        # Getting user inputs
        countries = st.sidebar.multiselect('Select a Country', sorted(df.Country.unique()), sorted(df.Country.unique()))
        properties = st.sidebar.multiselect('Select Property Type', sorted(df.Property_type.unique()), sorted(df.Property_type.unique()))
        rooms = st.sidebar.multiselect('Select Room Type', sorted(df.Room_type.unique()), sorted(df.Room_type.unique()))
        price_range = st.slider('Select Price', df.Price.min(), df.Price.max(), (df.Price.min(), df.Price.max()))

        # Filtering the dataframe based on user inputs
        filtered_df = df[(df.Country.isin(countries)) & 
                         (df.Property_type.isin(properties)) & 
                         (df.Room_type.isin(rooms)) & 
                         (df.Price >= price_range[0]) & 
                         (df.Price <= price_range[1])]

        # Creating columns for visualizations
        col1, col2 = st.columns(2, gap='medium')

        with col1:
            # Top 10 Property Types bar chart
            top_properties = filtered_df.groupby("Property_type").size().reset_index(name="Listings").sort_values(by='Listings', ascending=False)[:10]
            fig1 = px.bar(top_properties, title='Top 10 Property Types', x='Listings', y='Property_type', orientation='h', color='Property_type', color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig1, use_container_width=True)

            # Top 10 Hosts bar chart
            top_hosts = filtered_df.groupby("Host_name").size().reset_index(name="Listings").sort_values(by='Listings', ascending=False)[:10]
            fig2 = px.bar(top_hosts, title='Top 10 Hosts with Highest Listings', x='Listings', y='Host_name', orientation='h', color='Host_name', color_continuous_scale=px.colors.sequential.Agsunset)
            fig2.update_layout(showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            # Total Listings by Room Type pie chart
            room_counts = filtered_df.groupby("Room_type").size().reset_index(name="counts")
            fig3 = px.pie(room_counts, title='Total Listings by Room Type', names='Room_type', values='counts', color_discrete_sequence=px.colors.sequential.Rainbow)
            fig3.update_traces(textposition='outside', textinfo='value+label')
            st.plotly_chart(fig3, use_container_width=True)

            # Total Listings by Country choropleth map
            country_counts = filtered_df.groupby('Country', as_index=False)['Name'].count().rename(columns={'Name': 'Total_Listings'})
            fig4 = px.choropleth(country_counts, title='Total Listings by Country', locations='Country', locationmode='country names', color='Total_Listings', color_continuous_scale=px.colors.sequential.Plasma)
            st.plotly_chart(fig4, use_container_width=True)

# EXPLORE PAGE
if selected == "Explore":
    st.markdown("## Explore more about the Airbnb data")

    # Getting user inputs
    countries = st.sidebar.multiselect('Select a Country', sorted(df.Country.unique()), sorted(df.Country.unique()))
    properties = st.sidebar.multiselect('Select Property Type', sorted(df.Property_type.unique()), sorted(df.Property_type.unique()))
    rooms = st.sidebar.multiselect('Select Room Type', sorted(df.Room_type.unique()), sorted(df.Room_type.unique()))
    price_range = st.slider('Select Price', df.Price.min(), df.Price.max(), (df.Price.min(), df.Price.max()))

    # Filtering the dataframe based on user inputs
    filtered_df = df[(df.Country.isin(countries)) & 
                     (df.Property_type.isin(properties)) & 
                     (df.Room_type.isin(rooms)) & 
                     (df.Price >= price_range[0]) & 
                     (df.Price <= price_range[1])]

    # Price Analysis heading
    st.markdown("## Price Analysis")

    # Creating columns for visualizations
    col1, col2 = st.columns(2, gap='medium')

    with col1:
        # Average Price by Room Type bar chart
        avg_price_room = filtered_df.groupby('Room_type', as_index=False)['Price'].mean().sort_values(by='Price')
        fig5 = px.bar(data_frame=avg_price_room, x='Room_type', y='Price', color='Price', title='Avg Price by Room Type')
        st.plotly_chart(fig5, use_container_width=True)

        # Availability Analysis heading
        st.markdown("## Availability Analysis")

        # Availability by Room Type box plot
        fig6 = px.box(data_frame=filtered_df, x='Room_type', y='Availability_365', color='Room_type', title='Availability by Room Type')
        st.plotly_chart(fig6, use_container_width=True)

    with col2:
        # Average Price by Country scatter geo
        avg_price_country = filtered_df.groupby('Country', as_index=False)['Price'].mean()
        fig7 = px.scatter_geo(data_frame=avg_price_country, locations='Country', color='Price', hover_data=['Price'], locationmode='country names', size='Price', title='Avg Price by Country', color_continuous_scale='agsunset')
        st.plotly_chart(fig7, use_container_width=True)

        # Blank space
        st.markdown("#   ")
        st.markdown("#   ")

        # Average Availability by Country scatter geo
        avg_avail_country = filtered_df.groupby('Country', as_index=False)['Availability_365'].mean().dropna()
        avg_avail_country['Availability_365'] = avg_avail_country['Availability_365'].astype(int, errors='ignore')
    
        fig8 = px.scatter_geo(data_frame=avg_avail_country, locations='Country', color='Availability_365', hover_data=['Availability_365'], locationmode='country names', size='Availability_365', title='Avg Availability by Country', color_continuous_scale='agsunset')
        st.plotly_chart(fig8, use_container_width=True)
