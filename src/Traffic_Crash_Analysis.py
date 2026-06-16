import mysql.connector
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# code to make Database connection

connection = mysql.connector.connect(
        host="localhost", 
        user="root",
        password="password", # Use your password here
        database="Traffic_Crashes_Data"
    )
cursor = connection.cursor()

# Function to read SQLQuery output, assign column names of database table to dataframe columns and rearrange index starts from 1

def read_sql(cursor):

    # code to get the column names from the SQL Query

    column_names = [desc[0] for desc in cursor.description]
    dict_columns = {}
    i = 0
    for column_name in column_names:

        # code to update column names in a Dictionary

        dict_columns.update({i:column_name})
        i+=1
    data_list = []

    for data in cursor:
        data_list.append(data)
    df = pd.DataFrame(data_list)

    # code to rename column names from the Dictionary

    df.rename(columns=dict_columns,inplace=True)

    # code to rearrange row index starts from 1

    df.index += 1
    return df

# code to create sidebar with radio buttons 

with st.sidebar:
    add_radio = st.radio(
        "",
        ("Home", "SQL Queries")
    )

if add_radio == 'Home':

    st.set_page_config(layout="wide")
    st.markdown(
        """
        <h1 style='text-align: center;'>
            Traffic Crash Analytics & Safety Intelligence Platform
        </h1>
        """,
        unsafe_allow_html=True
    )

    # Use your file path here

    img_home_path = r'/home/rajesh-vijayakumar/Desktop/GUVI_AIML/Traffic_Crash_Analytics_and_Safety_Intelligence_Platform/data/raw/input_images/home_img.webp' 
    st.image(img_home_path,use_container_width=True)

elif add_radio == 'SQL Queries':

    st.set_page_config(layout="wide")
    st.markdown(
        """
        <h1 style='text-align: center;'>
            Traffic Crash Analytics & Safety Intelligence Platform
        </h1>
        """,
        unsafe_allow_html=True
    )

    option = st.selectbox(
                            '',
                            (
                                '--Select a Query--',
                                'Top 5 most dangerous combinations of weather and crash type',
                                'Top 10 streets with the highest number of injury crashes',
                                'Percentage of crashes that resulted in injuries for each crash type',
                                'Peak crash hour for each month',
                                'Top 5 primary causes of crashes during night time',
                                'Average number of injuries in daylight vs darkness conditions',
                                'Traffic control device type has the highest average injuries per crash',
                                'Top 5 locations (latitude/longitude) with the highest crash frequency',
                                'Top 5 streets with the highest injury rate',
                                'Most common crash type of each year',
                                'Day of the week with the highest average crashes per hour',
                                'High-risk time slot of the highest injury crashes',
                                'Top 3 contributing causes for each crash type',
                                'Year-over-year growth rate of crashes',
                                'Highest crash hotspot zones'
                            )
                        )

    options = (
                '--Select--',
                'Top 5 most dangerous combinations of weather and crash type',
                'Top 10 streets with the highest number of injury crashes',
                'Percentage of crashes that resulted in injuries for each crash type',
                'Peak crash hour for each month',
                'Top 5 primary causes of crashes during night time',
                'Average number of injuries in daylight vs darkness conditions',
                'Traffic control device type has the highest average injuries per crash',
                'Top 5 locations (latitude/longitude) with the highest crash frequency',
                'Top 5 streets with the highest injury rate',
                'Most common crash type of each year',
                'Day of the week with the highest average crashes per hour',
                'High-risk time slot of the highest injury crashes',
                'Top 3 contributing causes for each crash type',
                'Year-over-year growth rate of crashes',
                'Highest crash hotspot zones'
              )
    if option == options[1]:

        st.header('Top 5 most dangerous combinations of weather and crash type')

        # 1. Query to find the top 5 most dangerous combinations of weather and crash type based on total crashes.

        query = '''SELECT 
                        WEATHER_CONDITION, 
                        CRASH_TYPE, 
                        COUNT(*) AS TOTAL_CRASHES
                    FROM Traffic_Crashes_Analysis
                    GROUP BY WEATHER_CONDITION, CRASH_TYPE
                    ORDER BY TOTAL_CRASHES DESC
                    LIMIT 5'''
        
        cursor.execute(query)
        df = read_sql(cursor)
        st.dataframe(df)

        st.write('')
        st.write('')

        # Create combined label
        df["COMBINATION"] = (
            df["WEATHER_CONDITION"] + " - " + df["CRASH_TYPE"]
        )

        # Create chart
        fig, ax = plt.subplots(figsize=(10,5))

        bars = ax.bar(
            df["COMBINATION"],
            df["TOTAL_CRASHES"]
        )

        # Title
        ax.set_title(
            "Top 5 Dangerous Crash Combinations",
            fontsize=15,
            fontweight='bold'
        )

        # Axis labels
        ax.set_xlabel("Weather & Crash Type", fontsize=12, fontweight='bold')
        ax.set_ylabel("Total Crashes", fontsize=12, fontweight='bold')

        # Rotate labels
        plt.xticks(rotation=15, fontsize=10)

        # Add values on bars
        ax.bar_label(bars, fontsize=10)

        # Create 3 columns
        col1, col2, col3 = st.columns([1,4,1])

        # Put chart in center column
        with col2:
            st.pyplot(fig)

        st.subheader("Insight")

        st.markdown("""
                    Most crashes occurred under clear weather conditions, with non-injury or drive-away crashes 
                    recording the highest number of incidents (360,238 crashes). 
                    Injury-related crashes were also significantly higher during clear weather, 
                    likely due to increased traffic volume in normal weather conditions.
                    """)
        
    elif option == options[2]:

        st.header('Top 10 streets with the highest number of injury crashes')

        # 2. Query to identify the top 10 streets with the highest number of injury crashes.

        query = '''SELECT 
                        STREET_NAME, 
                        COUNT(*) AS TOTAL_INJURY_CRASHES 
                    FROM Traffic_Crashes_Analysis 
                    WHERE CRASH_TYPE = 'INJURY AND / OR TOW DUE TO CRASH'
                    GROUP BY STREET_NAME 
                    ORDER BY TOTAL_INJURY_CRASHES DESC 
                    LIMIT 10'''
        
        cursor.execute(query)
        df = read_sql(cursor)
        st.dataframe(df)

        st.write('')
        st.write('')

        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(10,6))

        bars = ax.barh(
            df["STREET_NAME"],
            df["TOTAL_INJURY_CRASHES"]
        )

        # Title
        ax.set_title(
            "Top 10 Streets with Highest Injury Crashes",
            fontsize=18,
            fontweight='bold'
        )

        # Axis labels
        ax.set_xlabel("Total Injury Crashes", fontsize=12, fontweight='bold')
        ax.set_ylabel("Street Name", fontsize=12, fontweight='bold')

        # Label size
        ax.tick_params(axis='y', labelsize=10)
        ax.tick_params(axis='x', labelsize=10)

        # Add values on bars
        ax.bar_label(bars, padding=3, fontsize=9)

        # Highest value at top
        ax.invert_yaxis()

        # Show chart
        # Create 3 columns
        col1, col2, col3 = st.columns([1,4,1])

        # Put chart in center column
        with col2:
            st.pyplot(fig)

        st.subheader("Insight")

        st.markdown("""
                    Western Ave recorded the highest number of injury crashes (5,334), followed by Pulaski Rd and Cicero Ave, 
                    indicating that major arterial roads are high-risk zones for injury-related accidents. 
                    High-traffic corridors such as Ashland Ave, Halsted St, Kedzie Ave, and Lake Shore Dr also emerged as major crash hotspots, 
                    likely due to dense traffic flow and heavy commuter activity.
                    """)
        
    elif option == options[3]:

        st.header('Percentage of crashes that resulted in injuries for each crash type')

        # 3. Query to find the percentage of crashes that resulted in injuries for each crash type.

        query = '''SELECT 
                        CRASH_TYPE, 
                        COUNT(*) AS CRASH_COUNT, 
                        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS CRASH_PERCENTAGE
                    FROM Traffic_Crashes_Analysis
                    WHERE INJURIES_TOTAL > 0
                    GROUP BY CRASH_TYPE'''
        
        cursor.execute(query)
        df = read_sql(cursor)
        st.dataframe(df)

        st.write('')
        st.write('')

        # Create donut chart
        fig, ax = plt.subplots(figsize=(5,5))

        wedges, texts, autotexts = ax.pie(
            df["CRASH_COUNT"],
            labels=df["CRASH_TYPE"],
            autopct='%1.2f%%',
            wedgeprops=dict(width=0.8), # creates donut hole
            textprops={'fontsize': 10} # label size
        )

        # Title
        ax.set_title("Crash Type Distribution", fontsize = 12, fontweight='bold')

        # Create 3 columns
        col1, col2, col3 = st.columns([1,4,1])

        # Put chart in center column
        with col2:
            st.pyplot(fig)

        st.subheader("Insight")

        st.markdown("""
                    The dataset is heavily dominated by severe crashes, with 99.22% (103,527 crashes) resulting in injuries or vehicle towing, 
                    while only 0.78% were minor no-injury incidents. This highlights the high severity of recorded crashes 
                    and emphasizes the need for stronger road safety and traffic management measures.
                    """)
        
    elif option == options[4]:

        st.header('Peak crash hour for each month')

        # 4. Query to determine the peak crash hour for each month.

        query = '''WITH MonthlyHourCounts AS (    
                        SELECT 
                            CRASH_MONTH, 
                            CRASH_HOUR, 
                            COUNT(*) AS CRASH_TOTAL,        
                            ROW_NUMBER() OVER (
                                PARTITION BY CRASH_MONTH
                                ORDER BY COUNT(*) DESC
                                ) AS ranking
                        FROM Traffic_Crashes_Analysis
                        GROUP BY CRASH_MONTH, CRASH_HOUR)

                    SELECT 
                        CASE CRASH_MONTH
                                WHEN 1 THEN 'January'
                                WHEN 2 THEN 'February'
                                WHEN 3 THEN 'March'
                                WHEN 4 THEN 'April'
                                WHEN 5 THEN 'May'
                                WHEN 6 THEN 'June'
                                WHEN 7 THEN 'July'
                                WHEN 8 THEN 'August'
                                WHEN 9 THEN 'September'
                                WHEN 10 THEN 'October'
                                WHEN 11 THEN 'November'
                                WHEN 12 THEN 'December'
                        END AS MONTH_OF_CRASH, 
                        CRASH_HOUR, 
                        CRASH_TOTAL
                    FROM MonthlyHourCounts
                    WHERE ranking = 1
                    ORDER BY CRASH_MONTH'''
        
        cursor.execute(query)
        df = read_sql(cursor)
        st.table(df)

        st.write('')
        st.write('')

        # Create labels
        df["MONTH_HOUR"] = (
            df["MONTH_OF_CRASH"] + " (" +
            df["CRASH_HOUR"].astype(str) + ":00)"
        )

        # Create chart
        fig, ax = plt.subplots(figsize=(12,6))

        bars = ax.bar(
            df["MONTH_HOUR"],
            df["CRASH_TOTAL"]
        )

        # Title
        ax.set_title(
            "Peak Crash Hour by Month",
            fontsize=18,
            fontweight='bold'
        )

        # Axis labels
        ax.set_xlabel("Month and Peak Hour", fontsize=12, fontweight='bold')
        ax.set_ylabel("Total Crashes", fontsize=12, fontweight='bold')

        # Rotate labels
        plt.xticks(rotation=45, ha='right', fontsize=10)

        # Add bar labels
        ax.bar_label(bars, fontsize=9)

        # Layout fix
        plt.tight_layout()

        # Show chart
        # Create 3 columns
        col1, col2, col3 = st.columns([1,4,1])

        # Put chart in center column
        with col2:
            st.pyplot(fig)

        st.subheader("Insight")

        st.markdown("""
                    Crash frequency consistently peaks during late afternoon and evening rush hours (3 PM–5 PM) across all months, 
                    indicating that heavy commuter traffic and congestion significantly increase accident risk. 
                    May recorded the highest peak-hour crashes, while seasonal shifts in peak timing suggest that daylight changes 
                    and varying traffic patterns influence crash occurrence throughout the year.
                    """)
        
    elif option == options[5]:

        st.header('Top 5 primary causes of crashes during night time')

        # 5. Query to find the top 5 primary causes of crashes during night time (CRASH_HOUR ≥ 18).

        query = '''SELECT 
                        PRIM_CONTRIBUTORY_CAUSE AS PRIMARY_CAUSE_OF_CRASH, 
                        COUNT(*) AS CRASH_TOTAL
                    FROM Traffic_Crashes_Analysis
                    WHERE CRASH_HOUR >= 18 OR CRASH_HOUR < 6
                    GROUP BY PRIM_CONTRIBUTORY_CAUSE
                    ORDER BY CRASH_TOTAL DESC
                    LIMIT 5'''
        
        cursor.execute(query)
        df = read_sql(cursor)
        st.dataframe(df)

        st.write('')
        st.write('')

        # Create chart
        fig, ax = plt.subplots(figsize=(10,6))

        bars = ax.barh(
            df["PRIMARY_CAUSE_OF_CRASH"],
            df["CRASH_TOTAL"]
        )

        # Title
        ax.set_title(
            "Top 5 Night-Time Crash Causes",
            fontsize=18,
            fontweight='bold'
        )

        # Axis labels
        ax.set_xlabel("Total Crashes", fontsize=12, fontweight='bold')
        ax.set_ylabel("Primary Cause", fontsize=12, fontweight='bold')

        # Label sizes
        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)

        # Add values on bars
        ax.bar_label(
            bars,
            padding=3,
            fontsize=9
        )

        # Highest at top
        ax.invert_yaxis()

        # Layout fix
        plt.tight_layout()

        # Show chart
        # Create 3 columns
        col1, col2, col3 = st.columns([1,4,1])

        # Put chart in center column
        with col2:
            st.pyplot(fig)

        st.subheader("Insight")

        st.markdown("""
                    Night-time crashes were most commonly linked to 'UNABLE TO DETERMINE', 
                    suggesting difficulties in identifying causes due to poor visibility and limited evidence at night. 
                    Among identified causes, failing to yield, following too closely, and speeding-related behavior were major contributors, 
                    highlighting the need for better lighting, speed control, and night-time traffic monitoring.
                    """)
        
    elif option == options[6]:

        st.header('Average number of injuries in daylight vs darkness conditions')

        # 6. Query to compare average number of injuries in daylight vs darkness conditions.

        query = '''SELECT 
                        CASE 
                            WHEN LIGHTING_CONDITION = 'DAYLIGHT' THEN 'Daylight'
                            WHEN LIGHTING_CONDITION LIKE 'DARKNESS%' THEN 'Darkness'
                        END AS LIGHTING, 
                        COUNT(*) AS TOTAL_CRASHES, 
                        ROUND(AVG(INJURIES_TOTAL), 4) AS AVG_INJURIES_PER_CRASH,
                        SUM(INJURIES_TOTAL) AS TOTAL_INJURIES
                    FROM Traffic_Crashes_Analysis
                    WHERE LIGHTING_CONDITION = 'DAYLIGHT' OR LIGHTING_CONDITION LIKE 'DARKNESS%'
                    GROUP BY LIGHTING
                    ORDER BY AVG_INJURIES_PER_CRASH DESC'''
        
        cursor.execute(query)
        df = read_sql(cursor)
        st.dataframe(df)

        st.write('')
        st.write('')

        # Create chart
        fig, ax = plt.subplots(figsize=(8,5))

        bars = ax.bar(
            df["LIGHTING"],
            df["AVG_INJURIES_PER_CRASH"]
        )

        # Title
        ax.set_title(
            "Average Injuries per Crash by Lighting Condition",
            fontsize=18,
            fontweight='bold'
        )

        # Axis labels
        ax.set_xlabel("Lighting Condition", fontsize=12, fontweight='bold')
        ax.set_ylabel("Average Injuries per Crash", fontsize=12, fontweight='bold')

        # Label size
        ax.tick_params(axis='x', labelsize=11)
        ax.tick_params(axis='y', labelsize=11)

        # Add values on bars
        ax.bar_label(
            bars,
            fmt='%.4f',
            fontsize=10
        )

        # Layout fix
        plt.tight_layout()

        # Show chart
        # Create 3 columns
        col1, col2, col3 = st.columns([1,4,1])

        # Put chart in center column
        with col2:
            st.pyplot(fig)

        st.subheader("Insight")

        st.markdown("""
                    Daylight conditions recorded the highest number of crashes and total injuries due to heavier traffic volume, 
                    while darkness-related crashes showed a higher average injury rate per crash, indicating greater severity at night. 
                    This suggests that reduced visibility, driver fatigue, and slower reaction times increase injury risk during darkness conditions.
                    """)
        
    elif option == options[7]:

        st.header('Traffic control device type has the highest average injuries per crash')

        # 7. Query to find which traffic control device type has the highest average injuries per crash.

        query = '''SELECT 
                        TRAFFIC_CONTROL_DEVICE, 
                        ROUND(AVG(INJURIES_TOTAL),2) AS AVG_INJURIES_PER_CRASH
                    FROM Traffic_Crashes_Analysis
                    GROUP BY TRAFFIC_CONTROL_DEVICE
                    ORDER BY AVG_INJURIES_PER_CRASH DESC
                    LIMIT 1'''
        
        cursor.execute(query)
        df = read_sql(cursor)
        st.dataframe(df)

        st.write('')
        st.write('')

        # Create chart
        fig, ax = plt.subplots(figsize=(5,3))

        bars = ax.bar(
            df["TRAFFIC_CONTROL_DEVICE"],
            df["AVG_INJURIES_PER_CRASH"]
        )

        ax.set_ylim(
            0,
            df["AVG_INJURIES_PER_CRASH"].max() + 0.2
        )


        # Title
        ax.set_title(
            "Highest Average Injuries per Crash",
            fontsize=15,
            fontweight='bold'
        )

        # Axis labels
        ax.set_xlabel("Traffic Control Device", fontsize=8, fontweight='bold')
        ax.set_ylabel("Average Injuries per Crash", fontsize=8, fontweight='bold')

        # Tick label sizes
        ax.tick_params(axis='x', labelsize=8)
        ax.tick_params(axis='y', labelsize=8)

        # Add value labels
        ax.bar_label(
            bars,
            fmt='%.2f',
            fontsize=10
        )

        # Rotate x labels if needed
        plt.xticks(rotation=10)

        # Layout fix
        plt.tight_layout()

        # Show chart
        # Create 3 columns
        col1, col2, col3 = st.columns([1,4,1])

        # Put chart in center column
        with col2:
            st.pyplot(fig)
            
        st.subheader("Insight")

        st.markdown("""
                    Crashes near Bicycle Crossing Sign locations recorded the highest average injuries per crash, 
                    indicating that bicycle crossing zones are high-risk areas due to the vulnerability of cyclists 
                    and interactions with vehicles. This highlights the need for improved lighting, road markings, speed control, 
                    and dedicated cycling safety measures in these areas.
                    """)
        
    elif option == options[8]:

        st.header('Top 5 locations (latitude/longitude) with the highest crash frequency')

        # 8. Query to identify the top 5 locations (latitude/longitude) with the highest crash frequency.

        query = '''SELECT 
                        LATITUDE, 
                        LONGITUDE, 
                        COUNT(*) AS CRASH_FREQUENCY
                    FROM Traffic_Crashes_Analysis
                    GROUP BY LATITUDE, LONGITUDE
                    ORDER BY CRASH_FREQUENCY DESC
                    LIMIT 5'''
        
        cursor.execute(query)
        df = read_sql(cursor)
        st.dataframe(df)

        st.write('')
        st.write('')

        # Create location labels
        df["LOCATION"] = (
            df["LATITUDE"].astype(str) + ", " +
            df["LONGITUDE"].astype(str)
        )

        # Create chart
        fig, ax = plt.subplots(figsize=(10,5))

        bars = ax.bar(
            df["LOCATION"],
            df["CRASH_FREQUENCY"]
        )

        # Title
        ax.set_title(
            "Top 5 Crash Hotspot Locations",
            fontsize=18,
            fontweight='bold'
        )

        # Axis labels
        ax.set_xlabel("Latitude / Longitude", fontsize=12, fontweight='bold')
        ax.set_ylabel("Crash Frequency", fontsize=12, fontweight='bold')

        # Tick sizes
        ax.tick_params(axis='x', labelsize=9)
        ax.tick_params(axis='y', labelsize=10)

        # Rotate x labels
        plt.xticks(rotation=15)

        # Add values on bars
        ax.bar_label(
            bars,
            fontsize=10
        )

        # Layout fix
        plt.tight_layout()

        # Show chart
        # Create 3 columns
        col1, col2, col3 = st.columns([1,4,1])

        # Put chart in center column
        with col2:
            st.pyplot(fig)

        st.subheader("Insight")

        st.markdown("""
                    The location at latitude 41.9762 and longitude -87.9053 recorded the highest crash frequency, 
                    making it a major accident hotspot likely influenced by heavy traffic, congestion, or complex road layouts. 
                    The consistently high crash counts across the top locations highlight the need for targeted safety measures 
                    such as improved signals, signage, speed management, and roadway redesign.
                    """)
        
    elif option == options[9]:

        st.header('Top 5 streets with the highest injury rate')

        # 9. Query to find the top 5 streets with the highest injury rate, considering only streets with more than 100 crashes.

        query = '''SELECT 
                        STREET_NAME, 
                        COUNT(*) AS CRASH_TOTAL, 
                        SUM(INJURIES_TOTAL) AS TOTAL_INJURIES, 
                        ROUND(SUM(INJURIES_TOTAL) * 1.0 / COUNT(*), 2) AS INJURY_RATE
                    FROM Traffic_Crashes_Analysis
                    GROUP BY STREET_NAME
                    HAVING COUNT(*) > 100
                    ORDER BY INJURY_RATE DESC
                    LIMIT 5'''
        
        cursor.execute(query)
        df = read_sql(cursor)
        st.dataframe(df)

        st.write('')
        st.write('')

        # Create chart
        fig, ax = plt.subplots(figsize=(10,5))

        bars = ax.bar(
            df["STREET_NAME"],
            df["INJURY_RATE"]
        )

        # Title
        ax.set_title(
            "Top 5 Streets by Injury Rate",
            fontsize=18,
            fontweight='bold'
        )

        # Axis labels
        ax.set_xlabel("Street Name", fontsize=12, fontweight='bold')
        ax.set_ylabel("Injury Rate", fontsize=12, fontweight='bold')

        # Tick label sizes
        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)

        # Rotate x labels
        plt.xticks(rotation=15)

        # Add value labels
        ax.bar_label(
            bars,
            fmt='%.2f',
            fontsize=10
        )

        # Layout fix
        plt.tight_layout()

        # Show chart
        # Create 3 columns
        col1, col2, col3 = st.columns([1,4,1])

        # Put chart in center column
        with col2:
            st.pyplot(fig)

        st.subheader("Insight")

        st.markdown("""
                    Marquette Dr recorded the highest injury rate, while Fifth Ave and Corcoran Pl also showed severe injury-related crash patterns, 
                    indicating that crashes on these streets are more likely to cause injuries. South Chicago Ave stood out as both a high-frequency 
                    and high-severity crash corridor, highlighting the need for improved traffic safety measures and infrastructure.
                    """)
        
    elif option == options[10]:

        st.header('Most common crash type of each year')

        # 10. Query to identify the most common crash type for each year.

        query = '''SELECT 
                        year AS YEAR, 
                        CRASH_TYPE, 
                        CRASH_TOTAL
                    FROM (SELECT 
                            year, CRASH_TYPE, COUNT(*) AS CRASH_TOTAL, 
                            RANK() OVER (
                                PARTITION BY year
                                ORDER BY COUNT(*) DESC
                            ) AS ranking
                            FROM Traffic_Crashes_Analysis
                            GROUP BY year, CRASH_TYPE
                        ) crash_rank
                    WHERE ranking = 1
                    ORDER BY year'''
        
        cursor.execute(query)
        df = read_sql(cursor)
        st.dataframe(df)

        st.write('')
        st.write('')

        # Create chart
        fig, ax = plt.subplots(figsize=(12,8))

        bars = ax.bar(
            df["YEAR"].astype(str),
            df["CRASH_TOTAL"]
        )

        ax.set_ylim(
            0,
            df["CRASH_TOTAL"].max() + 10000
        )

        # Title
        ax.set_title(
            "Most Common Crash Type by Year",
            fontsize=18,
            fontweight='bold',
            pad=50
        )

        # Axis labels
        ax.set_xlabel("Year", fontsize=15, fontweight='bold')
        ax.set_ylabel("Crash Total", fontsize=15, fontweight='bold')

        # Tick label sizes
        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)

        # Add values on bars
        ax.bar_label(
            bars,
            fontsize=10
        )

        # Add crash type labels above bars
        for i, crash_type in enumerate(df["CRASH_TYPE"]):
            ax.text(
                i,
                df["CRASH_TOTAL"].iloc[i] + 100,
                crash_type,
                ha='center',
                fontsize=10,
                rotation=15
            )

        # Layout fix
        plt.tight_layout()

        # Show chart
        # Create 3 columns
        col1, col2, col3 = st.columns([1,4,1])

        # Put chart in center column
        with col2:
            st.pyplot(fig)

        st.subheader("Insight")

        st.markdown("""
                    'NO INJURY / DRIVE AWAY' remained the most common crash type from 2020 to 2026, 
                    showing that most crashes were relatively minor and non-severe. 
                    The steady increase in crash totals until 2024 reflects rising traffic activity, 
                    highlighting the need for better traffic management and preventive road safety measures.
                    """)
        
    elif option == options[11]:

        st.header('Day of the week with the highest average crashes per hour')

        # 11. Query to find the day of the week with the highest average crashes per hour.

        query = '''SELECT 
                        CASE CRASH_DAY_OF_WEEK
                            WHEN 1 THEN 'Sunday'
                            WHEN 2 THEN 'Monday'
                            WHEN 3 THEN 'Tuesday'
                            WHEN 4 THEN 'Wednesday'
                            WHEN 5 THEN 'Thursday'
                            WHEN 6 THEN 'Friday'
                            WHEN 7 THEN 'Saturday'
                        END AS CRASH_DAY, 
                        ROUND(COUNT(*)/24,2) AS CRASH_TOTAL 
                    FROM Traffic_Crashes_Analysis 
                    GROUP BY CRASH_DAY_OF_WEEK 
                    ORDER BY CRASH_TOTAL DESC
                    LIMIT 1'''
        
        cursor.execute(query)
        df = read_sql(cursor)
        st.dataframe(df)

        st.write('')
        st.write('')

        # Create figure
        fig, ax = plt.subplots(figsize=(7,4))

        # Increase top spacing
        fig.subplots_adjust(top=0.82)

        # Bar chart
        bars = ax.bar(
            df["CRASH_DAY"],
            df["CRASH_TOTAL"]
        )

        ax.set_ylim(
            0,
            df["CRASH_TOTAL"].max() + 1000
        )

        # Chart title
        ax.set_title(
            "Highest Average Crashes Per Hour",
            fontsize=18,
            fontweight='bold',
            pad=20
        )

        # Axis labels
        ax.set_xlabel("Day of Week", fontsize=12, fontweight='bold')
        ax.set_ylabel("Average Crashes Per Hour", fontsize=12, fontweight='bold')

        # Tick sizes
        ax.tick_params(axis='x', labelsize=11)
        ax.tick_params(axis='y', labelsize=11)

        # Add value label
        ax.bar_label(
            bars,
            fmt='%.2f',
            fontsize=11,
            fontweight='bold',
            padding=3
        )

        # Layout
        plt.tight_layout()

        # Show chart
        # Create 3 columns
        col1, col2, col3 = st.columns([1,4,1])

        # Put chart in center column
        with col2:
            st.pyplot(fig)

        st.subheader("Insight")

        st.markdown("""
                    Friday recorded the highest average crashes per hour, indicating that end-of-week traffic, 
                    commuter movement, and increased social travel significantly raise accident risk. 
                    The result highlights Fridays as high-risk periods requiring stronger traffic monitoring and road safety enforcement.
                    """)
        
    elif option == options[12]:

        st.header('High-risk time slot of the highest injury crashes')

        # 12. Query to Identify high-risk time slots by grouping hours into buckets (Morning, Afternoon, Evening, Night) 
        #       and find which bucket has the highest injury crashes

        query = '''SELECT 
                        TIMING, 
                        COUNT(*) AS INJURY_CRASHES
                    FROM (
                        SELECT 
                            CASE
                                WHEN crash_hour BETWEEN 5 AND 11 THEN 'Morning'
                                WHEN crash_hour BETWEEN 12 AND 16 THEN 'Afternoon'
                                WHEN crash_hour BETWEEN 17 AND 20 THEN 'Evening'
                                ELSE 'Night'
                            END AS TIMING
                        FROM Traffic_Crashes_Analysis
                        WHERE INJURIES_TOTAL > 0
                        ) time_bucket
                    GROUP BY TIMING
                    ORDER BY INJURY_CRASHES DESC
                    LIMIT 1'''
        cursor.execute(query)
        df = read_sql(cursor)
        st.dataframe(df)

        st.write('')
        st.write('')

        # Create figure
        fig, ax = plt.subplots(figsize=(7,4))

        # Create bar chart
        bars = ax.bar(
            df["TIMING"],
            df["INJURY_CRASHES"]
        )

        # Add top space
        ax.set_ylim(
            0,
            df["INJURY_CRASHES"].max() + 3000
        )

        # Chart title
        ax.set_title(
            "Highest Injury Crash Time Slot",
            fontsize=18,
            fontweight='bold',
            pad=20
        )

        # Axis labels
        ax.set_xlabel("Time Slot", fontsize=12, fontweight='bold')
        ax.set_ylabel("Injury Crashes", fontsize=12, fontweight='bold')

        # Tick sizes
        ax.tick_params(axis='x', labelsize=11)
        ax.tick_params(axis='y', labelsize=11)

        # Add value labels
        ax.bar_label(
            bars,
            labels=[f"{value:,}" for value in df["INJURY_CRASHES"]],
            fontsize=11,
            fontweight='bold',
            padding=3
        )

        # Layout
        plt.tight_layout()

        # Show chart
        # Create 3 columns
        col1, col2, col3 = st.columns([1,4,1])

        # Put chart in center column
        with col2:
            st.pyplot(fig)

        st.subheader("Insight")

        st.markdown("""
                    The Afternoon time slot recorded the highest number of injury crashes, indicating that heavy daytime traffic, 
                    commuter activity, and increased pedestrian movement significantly raise accident risk during this period. 
                    This highlights the need for stronger traffic monitoring, speed control, and intersection management during peak afternoon hours.
                    """)
        
    elif option == options[13]:

        st.header('Top 3 contributing causes for each crash type')

        # 13. Query to find the top 3 contributing causes for each crash type.

        query = '''SELECT 
                        CRASH_TYPE, 
                        PRIM_CONTRIBUTORY_CAUSE, 
                        CRASH_TOTAL
                    FROM (
                        SELECT 
                            CRASH_TYPE, 
                            PRIM_CONTRIBUTORY_CAUSE, 
                            COUNT(*) AS CRASH_TOTAL,
                            RANK() OVER (
                                PARTITION BY CRASH_TYPE
                                ORDER BY COUNT(*) DESC
                            ) AS rank_num
                        FROM Traffic_Crashes_Analysis
                        GROUP BY CRASH_TYPE, PRIM_CONTRIBUTORY_CAUSE
                        ) ranking
                    WHERE rank_num <= 3
                    ORDER BY CRASH_TYPE, CRASH_TOTAL DESC'''
        
        cursor.execute(query)
        df = read_sql(cursor)
        st.dataframe(df)

        st.write('')
        st.write('')

        # Create combined label
        df["LABEL"] = (
            df["CRASH_TYPE"] + "\n" +
            df["PRIM_CONTRIBUTORY_CAUSE"]
        )

        # Create figure
        fig, ax = plt.subplots(figsize=(10,5))

        # Horizontal bar chart
        bars = ax.barh(
            df["LABEL"],
            df["CRASH_TOTAL"]
        )

        # Add top/right spacing
        ax.set_xlim(
            0,
            df["CRASH_TOTAL"].max() + 5000
        )

        # Chart title
        ax.set_title(
            "Top 3 Contributing Causes by Crash Type",
            fontsize=20,
            fontweight='bold',
            pad=20
        )

        # Axis labels
        ax.set_xlabel("Crash Total", fontsize=12, fontweight='bold')
        ax.set_ylabel("Crash Type & Cause", fontsize=12, fontweight='bold')

        # Tick sizes
        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=9)

        # Add values on bars
        ax.bar_label(
            bars,
            labels=[f"{value:,}" for value in df["CRASH_TOTAL"]],
            fontsize=9,
            padding=3
        )

        # Highest value at top
        ax.invert_yaxis()

        # Layout fix
        plt.tight_layout()

        # Show chart
        # Create 3 columns
        col1, col2, col3 = st.columns([1,4,1])

        # Put chart in center column
        with col2:
            st.pyplot(fig)

        st.subheader("Insight")

        st.markdown("""
                    'UNABLE TO DETERMINE' was the leading contributing cause across both major crash categories, while failing to yield, 
                    speeding-related behavior, and following too closely were major identifiable causes of severe and minor crashes. 
                    The findings highlight the strong impact of driver behavior on crash occurrence 
                    and emphasize the need for improved driver awareness, speed control, and traffic enforcement.
                    """)
        
    elif option == options[14]:

        st.header('Year-over-year growth rate of crashes')

        # 14. Query to calculate the year-over-year growth rate of crashes.

        query = '''WITH YEARLY_CRASHES AS (
                            SELECT 
                                year AS YEAR, 
                                COUNT(*) AS CRASH_TOTAL
                            FROM Traffic_Crashes_Analysis
                            GROUP BY year)

                    SELECT 
                        YEAR, 
                        CRASH_TOTAL, 
                        LAG(CRASH_TOTAL) OVER (ORDER BY year) AS PREVIOUS_YEAR_CRASHES,
                        ROUND(
                                (
                                    (CRASH_TOTAL - LAG(CRASH_TOTAL) OVER (ORDER BY year)) 
                                    * 100.0
                                ) 
                                / LAG(CRASH_TOTAL) OVER (ORDER BY year), 
                                2
                            ) AS YEAR_OVER_YEAR_GROWTH_RATE
                    FROM YEARLY_CRASHES
                    ORDER BY year'''
        
        cursor.execute(query)
        df = read_sql(cursor)
        st.dataframe(df)

        st.write('')
        st.write('')

        # Remove first NULL row for plotting
        chart_df = df.dropna()

        # Create figure
        fig, ax = plt.subplots(figsize=(10,5))

        # Create line chart
        ax.plot(
            chart_df["YEAR"].astype(str),
            chart_df["YEAR_OVER_YEAR_GROWTH_RATE"],
            marker='o',
            linewidth=2
        )

        # Add value labels
        for i, value in enumerate(chart_df["YEAR_OVER_YEAR_GROWTH_RATE"]):
            ax.text(
                i,
                float(value) + 0.5,
                f"{value}%",
                ha='center',
                fontsize=10,
                fontweight='bold'
            )

        # Chart title
        ax.set_title(
            "Year-over-Year Crash Growth Rate",
            fontsize=18,
            fontweight='bold',
            pad=20
        )

        # Axis labels
        ax.set_xlabel("Year", fontsize=12, fontweight='bold')
        ax.set_ylabel("Growth Rate (%)", fontsize=12, fontweight='bold')

        # Tick sizes
        ax.tick_params(axis='x', labelsize=11)
        ax.tick_params(axis='y', labelsize=11)

        # Add grid
        ax.grid(True)

        # Layout fix
        plt.tight_layout()

        # Show chart
        # Create 3 columns
        col1, col2, col3 = st.columns([1,4,1])

        # Put chart in center column
        with col2:
            st.pyplot(fig)

        st.subheader("Insight")

        st.markdown("""
                    Crash frequency saw its largest increase in 2021 after the lower traffic levels of 2020, 
                    then remained relatively stable with only minor fluctuations between 2022 and 2025. 
                    The sharp decline in 2026 is likely due to incomplete data rather than an actual reduction in crashes.
                    """)

    elif option == options[15]:

        st.header('Highest crash hotspot zones')

        # 15. Query to identify hotspot zones by grouping nearby locations (round latitude & longitude to 2 decimal places) 
        #       and find top 10 zones with highest crashes

        query = '''SELECT 
                        ROUND(LATITUDE, 2) AS LATITUDE_ZONE, 
                        ROUND(LONGITUDE, 2) AS LONGITUDE_ZONE, 
                        COUNT(*) AS CRASH_TOTAL
                    FROM Traffic_Crashes_Analysis
                    GROUP BY ROUND(LATITUDE, 2), ROUND(LONGITUDE, 2)
                    ORDER BY CRASH_TOTAL DESC
                    LIMIT 10'''
        
        cursor.execute(query)
        df = read_sql(cursor)
        st.dataframe(df)

        st.write('')
        st.write('')

        # Create zone labels
        df["ZONE"] = (
            df["LATITUDE_ZONE"].astype(str)
            + ", " +
            df["LONGITUDE_ZONE"].astype(str)
        )

        # Create figure
        fig, ax = plt.subplots(figsize=(10,6))

        # Horizontal bar chart
        bars = ax.barh(
            df["ZONE"],
            df["CRASH_TOTAL"]
        )

        # Add right-side spacing
        ax.set_xlim(
            0,
            df["CRASH_TOTAL"].max() + 500
        )

        # Chart title
        ax.set_title(
            "Top 10 Crash Hotspot Zones",
            fontsize=18,
            fontweight='bold',
            pad=20
        )

        # Axis labels
        ax.set_xlabel("Crash Total", fontsize=12, fontweight='bold')
        ax.set_ylabel("Latitude / Longitude Zones", fontsize=12, fontweight='bold')

        # Tick sizes
        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)

        # Add values on bars
        ax.bar_label(
            bars,
            labels=[f"{value:,}" for value in df["CRASH_TOTAL"]],
            fontsize=9,
            padding=3
        )

        # Highest value at top
        ax.invert_yaxis()

        # Layout fix
        plt.tight_layout()

        # Show chart
        # Create 3 columns
        col1, col2, col3 = st.columns([1,4,1])

        # Put chart in center column
        with col2:
            st.pyplot(fig)

        st.subheader("Insight")

        st.markdown("""
                    Crash incidents were heavily concentrated in a few hotspot zones, 
                    with the area around latitude 41.89 and longitude -87.63 recording the highest crash frequency. 
                    The clustering of crashes within nearby urban corridors suggests that dense traffic, major intersections, 
                    and congestion-prone road networks significantly increase accident risk.
                    """)
