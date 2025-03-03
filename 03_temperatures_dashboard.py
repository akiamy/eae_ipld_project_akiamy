# the libraries you have to use
import pandas as pd
import matplotlib.pyplot as plt

# Some extra libraries for date conversions and build the webapp
import streamlit as st


# ----- Left menu -----
with st.sidebar:
    st.image("/Users/akiamy/archivos/finalp/eae_ipld_project-main/eae_img.png", width=200)
    st.write("Interactive Project to load a dataset with information about the daily temperatures of 10 cities around the world, extract some insights usign Pandas and displaying them with Matplotlib.")
    st.write("Data extracted from: https://www.kaggle.com/datasets/sudalairajkumar/daily-temperature-of-major-cities (with some cleaning and modifications).")


# ----- Title of the page -----
st.title("🌦️ Temperatures Dashboard")
st.divider()


# ----- Loading the dataset -----

@st.cache_data
def load_data():
    data_path = "/Users/akiamy/archivos/finalp/eae_ipld_project-main/data/cities_temperatures.csv"

    temps_df = pd.read_csv(data_path)  # TODO: Ex 3.1: Load the dataset using Pandas, use the data_path variable and set the index column to "show_id"

    if temps_df is not None:
        temps_df["Date"] = pd.to_datetime(temps_df["Date"]).dt.date

    return temps_df  # a Pandas DataFrame


temps_df = load_data()

# Displaying the dataset in a expandable table
with st.expander("Check the complete dataset:"):
    st.dataframe(temps_df)


# ----- Data transformation -----

# TODO: Ex 3.2: Create a new column called `AvgTemperatureCelsius` that contains the temperature in Celsius degrees.
temps_df["AvgTemperatureCelsius"] = (temps_df["AvgTemperatureFahrenheit"] - 32) * 5/9     # uncomment this line to complete it


# ----- Extracting some basic information from the dataset -----

# TODO: Ex 3.3: How many different cities are there? Provide a list of them.
unique_countries_list = temps_df['City'].dropna().unique().tolist()

# TODO: Ex 3.4: Which are the minimum and maximum dates?
temps_df['Date'] = pd.to_datetime(temps_df['Date'])
min_date = temps_df['Date'].min()
max_date = temps_df['Date'].max()

# TODO:  Ex 3.5: What are the global minimum and maximum temperatures? Find the city and the date of each of them.
min_idx = temps_df["AvgTemperatureCelsius"].idxmin()
max_idx = temps_df["AvgTemperatureCelsius"].idxmax()

min_row = temps_df.loc[min_idx]
max_row = temps_df.loc[max_idx]

min_temp = min_row["AvgTemperatureCelsius"]
min_temp_city = min_row["City"]
min_temp_date = min_row["Date"]

max_temp = max_row["AvgTemperatureCelsius"]
max_temp_city = max_row["City"]
max_temp_date = max_row["Date"]


# ----- Displaying the extracted information metrics -----

st.write("##")
st.header("Basic Information")

cols1 = st.columns([4, 1, 6])
if unique_countries_list is not None:
    cols1[0].dataframe(pd.Series(unique_countries_list, name="Cities"), use_container_width=True)
else:
    cols1[0].write("⚠️ You still need to develop the Ex 3.3.")

if min_date is not None and max_date is not None:

    cols1[2].write("#")

    min_temp_text = f"""
    ### ☃️ Min Temperature: {min_temp:.1f}°C
    *{min_temp_city} on {min_temp_date}*
    """
    cols1[2].write(min_temp_text)

    cols1[2].write("#")

    max_temp_text = f"""
    ### 🏜️ Max Temperature: {max_temp:.1f}°C
    *{max_temp_city} on {max_temp_date}*
    """
    cols1[2].write(max_temp_text)

else:
    cols1[2].write("⚠️ You still need to develop the Ex 3.5.")


# ----- Plotting the temperatures over time for the selected cities -----

st.write("##")
st.header("Comparing the Temperatures of the Cities")

if unique_countries_list is not None:
    # Getting the list of cities to compare from the user
    selected_cities = st.multiselect("Select the cities to compare:", unique_countries_list, default=["Buenos Aires", "Dakar"], max_selections=4)

    cols2 = st.columns([6, 1, 6])

    start_date = cols2[0].date_input("Select the start date:", pd.to_datetime("2009-01-01").date())     # Getting the start date from the user
    end_date = cols2[2].date_input("Select the end date:", pd.to_datetime("2018-12-31").date())         # Getting the end date from the user

else:
    st.subheader("⚠️ You still need to develop the Ex 3.3.")

if unique_countries_list is not None and len(selected_cities) > 0:

    c = st.container(border=True)

    # TODO: Ex 3.7: Plot the temperatures over time for the selected cities for the selected time period,
    # every city has to be its own line with a different color.

    fig = plt.figure(figsize=(10, 5))

selected_cities = ['Buenos Aires', 'Cairo', 'Canberra']
start_date = pd.to_datetime('2001-01-01')
end_date = pd.to_datetime('2019-12-31')

fig = plt.figure(figsize=(10, 5))

for city in selected_cities:
    # Filter the DataFrame for the current city
    city_df = temps_df[temps_df['City'] == city]
    # Filter for the selected time period
    city_df_period = city_df[(city_df['Date'] >= start_date) & (city_df['Date'] <= end_date)]
    # Plot the temperatures over time; each city gets its own line
    plt.plot(city_df_period['Date'], city_df_period['AvgTemperatureCelsius'], label=city)

plt.title("Temperatures Over Time for Selected Cities")
plt.xlabel("Date")
plt.ylabel("Average Temperature (°C)")
plt.legend()
plt.tight_layout()
plt.show()

plt.legend()
    
c.pyplot(fig)



    # TODO: Make a histogram of the temperature reads of a list of selected cities, for the selected time period, 
    # every city has to be its own distribution with a different color.

fig = plt.figure(figsize=(10, 5))

selected_cities = ['Buenos Aires', 'Cairo', 'Canberra']
start_date = pd.to_datetime('2001-01-01')
end_date = pd.to_datetime('2019-12-31')

fig = plt.figure(figsize=(10, 5))

for city in selected_cities:
    
    city_df = temps_df[temps_df['City'] == city]
    
    city_df_period = city_df[(city_df['Date'] >= start_date) & (city_df['Date'] <= end_date)]
    
    plt.hist(city_df_period['AvgTemperatureCelsius'], bins=20, alpha=0.5, label=city)

plt.title("Temperature Distribution for Selected Cities")
plt.xlabel("Average Temperature (°C)")
plt.ylabel("Frequency")
plt.legend()

c.pyplot(fig)  