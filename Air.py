import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import warnings
from PIL import Image


def show_home():
    image = Image.open("images.jpg")
    st.image(image)
    
    st.header("About Airbnb")
    st.write("""
        **Airbnb** is an online marketplace that connects people who want to rent out their property with people looking for accommodations, typically for short stays. Founded in 2008, the platform allows hosts to list their available spaces—whether it's an entire home, a private room, or a shared space—and guests can search for and book these accommodations.
    """)
    st.markdown(
    """
    <p>For more information about Airbnb, visit the <a href="https://news.airbnb.com/about-us/" target="_blank">Airbnb About Us</a> page.</p>
    """,
    unsafe_allow_html=True
)
    
    st.header("Background of Airbnb")
    st.write("""
        **Airbnb** was born in 2007 when two Hosts welcomed three guests to their San Francisco home. Since then, it has grown to over 4 million Hosts who have welcomed over 1.5 billion guest arrivals in almost every country across the globe.
    """)
    
    st.header("How Airbnb Works")
    st.write("""
        The platform operates by allowing hosts to create a free listing for their property, specifying details such as pricing, availability, and house rules. Guests can browse these listings, read reviews from previous guests, and book accommodations through the site. Airbnb charges service fees to both guests and hosts, which contributes to its revenue.
    """)

    st.header("Key Features and Benefits")
    st.write("""
        - **Diverse Listings**: From urban apartments to countryside cottages, Airbnb offers a wide variety of lodging options.
        - **Experiences**: Beyond just accommodations, Airbnb also offers 'Experiences' where hosts can offer unique activities such as guided tours, cooking classes, and more.
        - **Community**: Airbnb emphasizes a sense of community and belonging, encouraging hosts and guests to build meaningful connections.
        - **Safety and Trust**: The platform provides various features to ensure safety and trust, including verified IDs, reviews, and a secure messaging system.
    """)

    st.header("Impact of Airbnb")
    st.write("""
        **Economic Impact**: Airbnb has had a significant economic impact by providing additional income to hosts and by attracting tourists who spend money in local communities.
        
        **Cultural Exchange**: By staying in local homes, guests often have more authentic cultural experiences compared to traditional hotels.
        
        **Challenges and Controversies**: Despite its success, Airbnb has faced various challenges including regulatory issues, concerns over housing affordability, and the impact on local communities.
    """)

    st.header("Future of Airbnb")
    st.write("""
        **Innovations**: Airbnb continues to innovate with new features and services, including enhanced safety protocols and flexible booking options in response to changing travel behaviors.
        
        **Expansion**: The company is exploring further expansions into new markets and services, such as long-term stays and business travel accommodations.
    """)


def show_about():
    st.header("ABOUT THIS PROJECT")
    
    st.subheader("1. Data Collection")
    st.write("""
        Gather data from Airbnb's public API or other available sources. Collect information on listings, hosts, reviews, pricing, and location data.
    """)
    
    st.subheader("2. Data Cleaning and Preprocessing")
    st.write("""
        Clean and preprocess the data to handle missing values, outliers, and ensure data quality. Convert data types, handle duplicates, and standardize formats.
    """)
    
    st.subheader("3. Exploratory Data Analysis (EDA)")
    st.write("""
        Conduct exploratory data analysis to understand the distribution and patterns in the data. Explore relationships between variables and identify potential insights.
    """)
    
    st.subheader("4. Visualization")
    st.write("""
        Create visualizations to represent key metrics and trends. Use charts, graphs, and maps to convey information effectively. Consider using tools like Matplotlib, Seaborn, or Plotly for visualizations.
    """)
    
    st.subheader("5. Geospatial Analysis")
    st.write("""
        Utilize geospatial analysis to understand the geographical distribution of listings. Map out popular areas, analyze neighborhood characteristics, and visualize pricing variations.
    """)
    
    st.subheader("6. Price Analysis and Visualization")
    st.write("""
        Using the cleaned data, conduct a thorough analysis of how prices vary across different locations, property types, and seasons. Create dynamic plots and charts to enable users to explore price trends, outliers, and correlations with other variables.
    """)
    
    st.subheader("7. Availability Analysis by Season")
    st.write("""
        Analyze the availability of Airbnb listings based on seasonal variations. Visualize occupancy rates, booking patterns, and demand fluctuations throughout the year using line charts, heatmaps, or other suitable visualizations.
    """)
    
    st.subheader("8. Location-Based Insights")
    st.write("""
        Investigate how the price of listings varies across different locations. Use MongoDB queries and data aggregation techniques to extract relevant information for specific regions or neighborhoods. Visualize these insights on interactive maps or dashboards.
    """)
    
    st.subheader("9. Interactive Visualizations")
    st.write("""
        Develop dynamic and interactive visualizations to allow users to filter and drill down into the data based on their preferences. Enable users to interact with the visualizations to explore specific regions, property types, or time periods of interest.
    """)
    
    st.subheader("10. Dashboard Creation using  Power BI")
    st.write("""
        Build a comprehensive dashboard using  Power BI, combining various visualizations to present key insights from the analysis. Provide a holistic view of the Airbnb dataset and its patterns.
    """)

warnings.filterwarnings("ignore")
st.set_page_config(layout="wide",page_icon="C:/Users/HameedS/Desktop/New folder/images.jpg")
st.title("Airbnb Data Analysis")



@st.cache_data
def load_data(filepath):
    return pd.read_csv(filepath)

df = load_data("Airbnbfinal.csv")

with st.sidebar:
    selected_option = option_menu("Main Menu", ["Home", "Data Exploration", "About"])

if selected_option == "Home":
   show_home()

if selected_option == "Data Exploration":
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Price Analysis", "Availability Analysis", "Location Based", "Geospatial Visualization", "Top Charts"])

    with tab1:
        st.title("Price Difference")

        country = st.selectbox("Select the Country", df["country"].unique())
        filtered_df = df[df["country"] == country]

        room_type = st.selectbox("Select the Room Type", filtered_df["room_type"].unique())
        filtered_room_df = filtered_df[filtered_df["room_type"] == room_type]

        property_price_df = filtered_room_df.groupby("property_type")[["price", "review_scores", "number_of_reviews"]].sum().reset_index()
        
        property_type = st.selectbox("Select the Property Type", filtered_room_df["property_type"].unique())
        property_filtered_df = filtered_room_df[filtered_room_df["property_type"] == property_type]

        host_response_time = st.selectbox("Select the Host Response Time", property_filtered_df["host_response_time"].unique())
        host_response_filtered_df = property_filtered_df[property_filtered_df["host_response_time"] == host_response_time]

        col1, col2 = st.columns(2)

        with col1:
            fig_bar = px.bar(property_price_df, x='property_type', y="price", title="Price for Property Types",
                            hover_data=["number_of_reviews", "review_scores"], color_discrete_sequence=px.colors.sequential.Redor_r, width=600, height=500)
            st.plotly_chart(fig_bar)

        #property_type = st.selectbox("Select the Property Type", filtered_room_df["property_type"].unique())
        #property_filtered_df = filtered_room_df[filtered_room_df["property_type"] == property_type]

        with col2:
            host_response_df = property_filtered_df.groupby("host_response_time")[["price", "bedrooms"]].sum().reset_index()
            fig_pie = px.pie(host_response_df, values="price", names="host_response_time",
                            hover_data=["bedrooms"], color_discrete_sequence=px.colors.sequential.BuPu_r,
                            title="Price Difference Based on Host Response Time", width=600, height=500)
            st.plotly_chart(fig_pie)

        #host_response_time = st.selectbox("Select the Host Response Time", property_filtered_df["host_response_time"].unique())
        #host_response_filtered_df = property_filtered_df[property_filtered_df["host_response_time"] == host_response_time]

        bed_type_nights_df = host_response_filtered_df.groupby("bed_type")[["minimum_nights", "maximum_nights", "price"]].sum().reset_index()
        
        col3, col4 = st.columns(2)

        with col3:
            fig_min_max_nights = px.bar(bed_type_nights_df, x='bed_type', y=['minimum_nights', 'maximum_nights'],
                                        title='Minimum and Maximum Nights', hover_data=["price"],
                                        barmode='group', color_discrete_sequence=px.colors.sequential.Rainbow, width=600, height=500)
            st.plotly_chart(fig_min_max_nights)

        bed_type_accommodates_df = host_response_filtered_df.groupby("bed_type")[["bedrooms", "beds", "accommodates", "price"]].sum().reset_index()
        
        with col4:
            fig_bedrooms_beds = px.bar(bed_type_accommodates_df, x='bed_type', y=['bedrooms', 'beds', 'accommodates'],
                                    title='Bedrooms and Beds Accommodates', hover_data=["price"],
                                    barmode='group', color_discrete_sequence=px.colors.sequential.Rainbow_r, width=600, height=500)
            st.plotly_chart(fig_bedrooms_beds)

    with tab2:
        st.title("Availability Analysis")
    
        country_a = st.selectbox("Select the Country", df["country"].unique(), key="country_a")
        availability_df = df[df["country"] == country_a]
        
        property_type_a = st.selectbox("Select the Property Type", availability_df["property_type"].unique(), key="property_type_a")
        property_availability_df = availability_df[availability_df["property_type"] == property_type_a]
        
        #room_type_a = st.selectbox("Select the Room Type", property_availability_df["room_type"].unique(), key="room_type_a")
        #room_availability_df = property_availability_df[property_availability_df["room_type"] == room_type_a]

        col1, col2 = st.columns(2)

        with col1:
            for period in ["availability_30", "availability_60"]:
                fig_sunburst = px.sunburst(property_availability_df, path=["room_type", "bed_type", "is_location_exact"], values=period,
                #fig_sunburst = px.sunburst(room_availability_df, path=["room_type", "bed_type", "is_location_exact"], values=period,                           
                                        width=600, height=500, title=f"{period.replace('_', ' ').title()}", color_discrete_sequence=px.colors.sequential.Peach_r)
                st.plotly_chart(fig_sunburst)
        
        with col2:
            for period in ["availability_90", "availability_365"]:
                fig_sunburst = px.sunburst(property_availability_df, path=["room_type", "bed_type", "is_location_exact"], values=period,
                                        width=600, height=500, title=f"{period.replace('_', ' ').title()}", color_discrete_sequence=px.colors.sequential.Agsunset)
                st.plotly_chart(fig_sunburst)

        room_type_a = st.selectbox("Select the Room Type", property_availability_df["room_type"].unique(), key="room_type_a")
        room_availability_df = property_availability_df[property_availability_df["room_type"] == room_type_a]
        
        availability_response_df = room_availability_df.groupby("host_response_time")[["availability_30", "availability_60", "availability_90", "availability_365", "price"]].sum().reset_index()
        
        fig_availability_response = px.bar(availability_response_df, x='host_response_time', y=['availability_30', 'availability_60', 'availability_90', "availability_365"],
                                        title='Availability Based on Host Response Time', hover_data=["price"],
                                        barmode='group', color_discrete_sequence=px.colors.sequential.Rainbow_r, width=1000)
        st.plotly_chart(fig_availability_response)

    with tab3:

        st.title("Location Analysis")

        country_l = st.selectbox("Select the Country", df["country"].unique(), key="country_l")
        location_df = df[df["country"] == country_l]
        property_type_l = st.selectbox("Select the Property Type", location_df["property_type"].unique(), key="property_type_l")
        property_location_df = location_df[location_df["property_type"] == property_type_l]
        room_type_l = st.selectbox("Select the Room Type", property_location_df["room_type"].unique(), key="room_type_l")  

        price_range_options = [
            f"{property_location_df['price'].min()} to {property_location_df['price'].max() * 0.30:.2f} (30% of the Value)",
            f"{property_location_df['price'].max() * 0.30:.2f} to {property_location_df['price'].max() * 0.60:.2f} (30% to 60% of the Value)",
            f"{property_location_df['price'].max() * 0.60:.2f} to {property_location_df['price'].max():.2f} (60% to 100% of the Value)"
        ]
        selected_price_range = st.radio("Select the Price Range", price_range_options)

        if selected_price_range:
            price_range_parts = selected_price_range.split(" to ")[0].split("-")
            if len(price_range_parts) == 1:
                min_price = max_price = float(price_range_parts[0])
            else:
                min_price, max_price = map(float, price_range_parts)
            filtered_price_df = property_location_df[(property_location_df["price"] >= min_price) & (property_location_df["price"] <= max_price)]
            st.dataframe(filtered_price_df)

            
            room_ty_l = st.selectbox("Select the Room_Type_l", filtered_price_df["room_type"].unique())
            df_val_sel_rt = filtered_price_df[filtered_price_df["room_type"] == room_ty_l]

            fig_2 = px.bar(df_val_sel_rt, x=["street", "host_location", "host_neighbourhood"], y="market", title="MARKET",
                        hover_data=["name", "host_name", "market"], barmode='group', orientation='h',
                        color_discrete_sequence=px.colors.sequential.Rainbow_r, width=1000)
            st.plotly_chart(fig_2)

            fig_3 = px.bar(df_val_sel_rt, x="government_area", y=["host_is_superhost", "host_neighbourhood", "cancellation_policy"], title="GOVERNMENT_AREA",
                        hover_data=["guests_included", "location_type"], barmode='group',
                        color_discrete_sequence=px.colors.sequential.Rainbow_r, width=1000)
            st.plotly_chart(fig_3)

    with tab4:
        st.title("Geospatial Visualization")
        st.write("") #'  #add space'

        fig_map = px.scatter_mapbox(df, lat="latitude", lon="longitude", color="price", size="accommodates",
                                    color_continuous_scale="rainbow", hover_name="name", range_color=(0, 49000),
                                    mapbox_style="carto-positron", zoom=1)
        fig_map.update_layout(width=1150, height=800, title="Geospatial Distribution of Listings")
        st.plotly_chart(fig_map)

    with tab5:
        st.title("Top Charts Analysis")

        country_t = st.selectbox("Select the Country_t", df["country"].unique())
        df1_t = df[df["country"] == country_t]

        property_ty_t = st.selectbox("Select the Property_type_t", df1_t["property_type"].unique())
        df2_t = df1_t[df1_t["property_type"] == property_ty_t]
        df2_t.reset_index(drop=True, inplace=True)

        df2_t_sorted = df2_t.sort_values(by="price")
        df2_t_sorted.reset_index(drop=True, inplace=True)

        df_price = pd.DataFrame(df2_t_sorted.groupby("host_neighbourhood")["price"].agg(["sum", "mean"]))
        df_price.reset_index(inplace=True)
        df_price.columns = ["host_neighbourhood", "Total_price", "Avarage_price"] #renaming 

        col1, col2 = st.columns(2)

        with col1:
            fig_price = px.bar(df_price, x="Total_price", y="host_neighbourhood", orientation='h',
                            title="PRICE BASED ON HOST_NEIGHBOURHOOD", width=600, height=800)
            st.plotly_chart(fig_price)

        with col2:
            fig_price_2 = px.bar(df_price, x="Avarage_price", y="host_neighbourhood", orientation='h',
                                title="AVERAGE PRICE BASED ON HOST_NEIGHBOURHOOD", width=600, height=800)
            st.plotly_chart(fig_price_2)

        col1, col2 = st.columns(2)

        with col1:
            df_price_1 = pd.DataFrame(df2_t_sorted.groupby("host_location")["price"].agg(["sum", "mean"]))
            df_price_1.reset_index(inplace=True)
            df_price_1.columns = ["host_location", "Total_price", "Avarage_price"]

            fig_price_3 = px.bar(df_price_1, x="Total_price", y="host_location", orientation='h',
                                width=600, height=800, color_discrete_sequence=px.colors.sequential.Bluered_r,
                                title="PRICE BASED ON HOST_LOCATION")
            st.plotly_chart(fig_price_3)

        with col2:
            fig_price_4 = px.bar(df_price_1, x="Avarage_price", y="host_location", orientation='h',
                                width=600, height=800, color_discrete_sequence=px.colors.sequential.Bluered_r,
                                title="AVERAGE PRICE BASED ON HOST_LOCATION")
            st.plotly_chart(fig_price_4)

        room_type_t = st.selectbox("Select the Room_Type_t", df2_t_sorted["room_type"].unique())

        df3_t = df2_t_sorted[df2_t_sorted["room_type"] == room_type_t]
        df3_t_sorted_price = df3_t.sort_values(by="price")
        df3_t_sorted_price.reset_index(drop=True, inplace=True)

        df3_top_50_price = df3_t_sorted_price.head(100)

        fig_top_50_price_1 = px.bar(df3_top_50_price, x="name", y="price", color="price",
                                    color_continuous_scale="rainbow",
                                    range_color=(0, df3_top_50_price["price"].max()),
                                    title="MINIMUM_NIGHTS MAXIMUM_NIGHTS AND ACCOMMODATES",
                                    width=1200, height=800,
                                    hover_data=["minimum_nights", "maximum_nights", "accommodates"])

        st.plotly_chart(fig_top_50_price_1)

        fig_top_50_price_2 = px.bar(df3_top_50_price, x="name", y="price", color="price",
                                    color_continuous_scale="greens",
                                    title="BEDROOMS, BEDS, ACCOMMODATES AND BED_TYPE",
                                    range_color=(0, df3_top_50_price["price"].max()),
                                    width=1200, height=800,
                                    hover_data=["accommodates", "bedrooms", "beds", "bed_type"])

        st.plotly_chart(fig_top_50_price_2)

if selected_option == "About":
    show_about()
