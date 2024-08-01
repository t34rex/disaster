import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    'Clean Water': ['tubig', 'water', 'inumin'], 
    'Food': ['food', 'pagkain', 'ulam', 'relief goods'], 
    'Shelter': ['shelter', 'evacuation', 'bahay', 'tirahan', 'house'], 
    'Donation': ['donation', 'cash', 'pera', 'money', 'fund'],
    'Clothes': ['clothes', 'damit', 'clothing'], 
}

disaster_keywords = {
    'Typhoon': ['typhoon', 'storm', 'rain', 'flood', 'flooding', 'ulan', 'bagyo', 'egay', 'maring', 'paeng', 'odette'],
    'Earthquake': ['earthquake', 'quake', 'magnitude', 'lindol', 'lumindol'],
    'Fire': ['fire', 'wildfire'],
    'Hurricane': ['hurricane', 'cyclone'],
    'Tornado': ['tornado', 'twister', 'funnel']
}

uploaded_file = st.file_uploader("Choose a CSV file", type='csv')

if uploaded_file is not None:  # fix: 'none' should be 'None'
    try:
        df = pd.read_csv(uploaded_file)

        st.write("Here's the data from your CSV file:")
        st.write(df)

        if 'text' in df.columns and 'date' in df.columns:  # Ensure 'date' column exists
            filtered_results = []

            for location in location_keywords:
                location_condition = df['text'].str.contains(location, case=False, na=False)
                location_filtered_df = df[location_condition]

                if not location_filtered_df.empty:
                    for index, row in location_filtered_df.iterrows():
                        tweet_text = row['text'].lower()
                        identified_needs = None
                        identified_disaster_type = 'Unknown'

                        # Check needs keywords. You may want to consider iterating over needs_keywords
                        for need, keywords in needs_keywords.items():
                            if any(keyword in tweet_text for keyword in keywords):
                                identified_needs = need  # Store the identified need
                                break

                        # Check disaster type
                        for disaster_type, keywords in disaster_keywords.items():
                            if any(k in tweet_text for k in keywords):
                                identified_disaster_type = disaster_type
                                break

                        if identified_needs:
                            filtered_results.append({
                                'Location': location,
                                'Disaster Type': identified_disaster_type,
                                'Needs': identified_needs,
                                'Tweet Snippets': row['text'],
                                'Date': row['date']
                            })

            if filtered_results:
                results_df = pd.DataFrame(filtered_results)  # Correct the typo here from dataframe to DataFrame
                st.subheader("Results")
                st.write(results_df)

                # Calculate statistics: count of needs for each disaster type
                stats_df = results_df.groupby(['Disaster Type', 'Needs']).size().reset_index(name='Count')
                st.subheader("Statistics of Needs by Disaster Type")
                st.write(stats_df)

                for disaster in stats_df['Disaster Type'].unique():
                    data = stats_df[stats_df['Disaster Type'] == disaster]
                    fig, ax = plt.subplots()
                    ax.pie(data['Count'], labels=data['Needs'], autopct='%1.1f%%')
                    plt.title(f"Distribution of Needs in {disaster}")
                    st.pyplot(fig)

            else:
                st.warning("No tweets found matching the specified criteria.")
        else:
            st.error("The uploaded csv file must contain both 'text' and 'date' columns.")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
else:
    st.info("Please upload a CSV file.")