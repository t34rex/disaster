import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
import seaborn as sns

st.title("DiRA: Disaster Response Assistance")
st.write("A Decision Support System for better Disaster Response Management.")
st.write("Upload a CSV file for analysis.")

location_keywords = ['Abra', 'Agusan Del Norte', 'Agusan Del Sur', 'Aklan', 'Albay',
        'Antique', 'Apayao', 'Aurora', 'Basilan', 'Bataan', 'Batanes', 'Batangas', 'Benguet', 'Biliran',
        'Bohol', 'Bukidnon', 'Bulacan', 'Cagayan', 'Camarines Norte', 'Camarines Sur', 'Camiguin', 'Capiz',
        'Catanduanes', 'Cavite', 'Cebu', 'Cotabato', 'Davao', 'Davao De Oro', 'Davao Del Norte', 'Davao Del Sur',
        'Davao Occidental', 'Davao Oriental', 'Dinagat Islands', 'Eastern Samar', 'Guimaras', 'Ifugao',
        'Ilocos Norte', 'Ilocos Sur', 'Iloilo', 'Isabela', 'Kalinga', 'La Union', 'Laguna', 'Lanao Del Norte',
        'Lanao Del Sur', 'Leyte', 'Maguindanao Del Norte', 'Maguindanao Del Sur', 'Marinduque', 'Masbate',
        'Manila', 'Misamis Occidental', 'Misamis Oriental', 'Mountain Province', 'Negros Occidental',
        'Negros Oriental', 'Northern Samar', 'Nueva Ecija', 'Nueva Vizcaya', 'Mindoro Oriental', 'Mindoro',
        'Palawan', 'Pampanga', 'Pangasinan', 'Quezon', 'Quirino', 'Rizal', 'Romblon', 'Samar', 'Sarangani',
        'Siquijor', 'Sorsogon', 'South Cotabato', 'Southern Leyte', 'Sultan Kudarat', 'Sulu', 'Surigao Del Norte',
        'Surigao Del Sur', 'Tarlac', 'Tawi-tawi', 'Zambales', 'Zamboanga Del Norte', 'Zamboanga Del Sur',
        'Zamboanga Sibugay'] 

needs_keywords = {
    'Drinking Water': ['tubig', 'water', 'inumin', 'bottled water'], 
    'Food': ['food', 'pagkain', 'ulam', 'relief goods'], 
    'Shelter': ['shelter', 'evacuation', 'bahay', 'tirahan', 'house'], 
    'Cash Assistance': ['cash', 'fund', 'pera', 'money', 'cash donation'],
    'Clothes': ['clothes', 'damit', 'clothing', 'blanket'],
    'Hygiene Kits': ['sabon', 'toothpaste', 'soap', 'shampoo', 'panglaba', 'panlaba', 'toothbrush', 'hygiene', 'hygiene kits', 'clean water']
}

disaster_keywords = {
    'Typhoon': ['typhoon', 'storm', 'rain', 'flood', 'flooding', 'ulan', 'bagyo', 'egay', 'maring', 'paeng', 'odette'],
    'Earthquake': ['earthquake', 'quake', 'magnitude', 'lindol', 'lumindol'],
    'Fire': ['fire', 'wildfire'],
    'Hurricane': ['hurricane', 'cyclone'],
    'Tornado': ['tornado', 'twister', 'funnel']
}

uploaded_file = st.file_uploader("Choose a CSV file", type='csv')

if uploaded_file is not None:  # fix: 'none' should be 'none'
    try:
        df = pd.read_csv(uploaded_file)

        st.write("Here's the data from your CSV file:")
        st.write(df)

        if 'text' in df.columns and 'date' in df.columns:  # ensure 'date' column exists
            filtered_results = []

            for location in location_keywords:
                location_condition = df['text'].str.contains(location, case=False, na=False)  # case issue fixed
                location_filtered_df = df[location_condition]

                if not location_filtered_df.empty:
                    for index, row in location_filtered_df.iterrows():
                        tweet_text = row['text'].lower()
                        identified_disaster_type = 'unknown'

                        # Store multiple identified needs
                        identified_needs_list = []

                        # check needs keywords
                        for need, keywords in needs_keywords.items():
                            if any(keyword in tweet_text for keyword in keywords):
                                identified_needs_list.append(need)  # Store all identified needs

                        # check disaster type
                        for disaster_type, keywords in disaster_keywords.items():
                            if any(k in tweet_text for k in keywords):
                                identified_disaster_type = disaster_type
                                break

                        # Record results for each identified need
                        for identified_needs in identified_needs_list:
                            filtered_results.append({
                                'Location': location,
                                'Disaster Type': identified_disaster_type,
                                'Needs': identified_needs,
                                'Tweet Snippets': row['text'],
                                'date': row['date']
                            })

            if filtered_results:
                results_df = pd.DataFrame(filtered_results)  # corrected typo from dataframe to DataFrame
                st.subheader("Results")
                st.write(results_df)

                pivot_df = results_df.pivot_table(index='Location', columns='Needs', aggfunc='size', fill_value=0)

                # Radar Chart
                st.subheader("Radar Chart of Needs for Specific Location")
                specific_location = st.selectbox("Select Location", results_df['Location'].unique())

                if specific_location in pivot_df.index:
                    # Prepare data for radar chart using all needs
                    all_needs = list(needs_keywords.keys())
                    values = [pivot_df.loc[specific_location].get(need, 0) for need in all_needs]  # Fill missing needs with 0

                    # Close the loop for radar chart
                    values += values[:1]  # Repeat the first value to close the loop
                    num_vars = len(all_needs)
                    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
                    angles += angles[:1]  # Repeat the first angle to close the loop

                    # Plot radar chart
                    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

                    # Fill shading for all needs
                    ax.fill(angles, values, color='blue', alpha=0.25)  # Fill for shading
                    ax.plot(angles, values, color='blue', linewidth=0.5)  # Outline the area
                    ax.set_yticklabels([])  # No labels on the radial axis
                    plt.xticks(angles[:-1], all_needs)  # Use all needs for labels
                    plt.title(f"Radar Chart of Needs for {specific_location}")
                    st.pyplot(fig)
                else:
                    st.warning(f"No data found for {specific_location}.")
                
                # Stacked Bar chart
                st.subheader("Stacked Bar Chart of Needs by Location")
                pivot_df.plot(kind='bar', stacked=True, figsize=(10, 6))
                plt.title("Needs Distribution by Location")
                plt.ylabel('Count')
                plt.xlabel('Location')
                plt.xticks(rotation=45)
                st.pyplot(plt.gcf())  # Ensure to use the current figure and clear it later if needed
                plt.clf()  # Clear plt for future plots                
                               
                # Statistics
                stats_df = results_df.groupby(['Disaster Type', 'Needs']).size().reset_index(name='Count')
                st.subheader("Statistics of Needs by Disaster Type")
                st.write(stats_df)

                st.subheader("Pie Chart of Distribution of Needs in Disasters")

                # Pie Chart
                for disaster in stats_df['Disaster Type'].unique():
                    data = stats_df[stats_df['Disaster Type'] == disaster]
                    fig, ax = plt.subplots()
                    ax.pie(data['Count'], labels=data['Needs'], autopct='%1.1f%%')
                    plt.title(f"Distribution of Needs in {disaster}")
                    st.pyplot(fig)

                # New statistics: count of needs by location
                #location_stats_df = results_df.groupby(['location', 'needs']).size().reset_index(name='count')
                #st.subheader("statistics of needs by location")
                #st.write(location_stats_df)

                #for location in location_stats_df['location'].unique():
                    #data = location_stats_df[location_stats_df['location'] == location]
                    #fig, ax = plt.subplots()
                    #ax.pie(data['count'], labels=data['needs'], autopct='%1.1f%%')
                    #plt.title(f"distribution of needs in {location}")
                    #st.pyplot(fig)
                
                # Creating a pivot table for stacked bar chart
                # Fill missing needs with zero

                # After filtering results and creating stats_df
                overall_needs_stats = results_df.groupby('Needs').size().reset_index(name='Count')

                # Bar chart
                st.subheader("Overall Distribution of Needs")
                fig, ax = plt.subplots()
                sns.barplot(data=overall_needs_stats, x='Needs', y='Count', ax=ax, palette='viridis')
                plt.xticks(rotation=45)
                plt.title("Distribution of Needs Across All Locations")
                st.pyplot(fig)

            else:
                st.warning("No tweets found matching the specified criteria.")
        else:
            st.error("The uploaded csv file must contain both 'text' and 'date' columns.")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
else:
    st.info("Please upload a CSV file.")