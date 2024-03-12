import pandas as pd
import plotly.express as px
import streamlit as st

dat = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

# Extract unique country names
countries = ['Select a country'] + dat['Country/Region'].unique().tolist()

st.title('COVID-19 Recovery Data')

# Streamlit app
selected_country = st.selectbox('Select a country ', countries)

if selected_country != 'Select a country':
    # Filter the DataFrame for data of selected country
    selected_recovery_data = dat[dat['Country/Region'] == selected_country ]
    
    # Drop unnecessary columns
    selected_recovery_data = selected_recovery_data.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], axis=1)
    
    # Transpose the DataFrame so that dates become rows
    selected_recovery_data = selected_recovery_data.transpose()
    
    # Reset index to make dates a column
    selected_recovery_data = selected_recovery_data.reset_index()
    
    # Rename columns
    selected_recovery_data.columns = ['Date', 'Recovery']
    
    # Convert cumulative recovery data to daily recovery data
    selected_recovery_data['Daily_Recovery'] = selected_recovery_data['Recovery'] - selected_recovery_data['Recovery'].shift(1)
    
    # Replace negative values with 0
    selected_recovery_data['Daily_Recovery'] = selected_recovery_data['Daily_Recovery'].apply(lambda x: max(0, x))
    
    
    # Display the DataFrame
    fig = px.line( x=selected_recovery_data['Date'], y=selected_recovery_data['Daily_Recovery'])
    fig.update_layout(title='COVID-19 Recoveries in the ' + selected_country,
                      xaxis_title='Date',
                      yaxis_title='Number of Recoveries',
                      hovermode='x unified')
    
    fig.update_xaxes(tickangle=45,  # Rotate tick labels by 45 degrees
                     tickformat='%b %d, %Y',  # Format tick labels as 'Month Day, Year'
                     tickmode='auto',  # Let Plotly automatically choose the tick spacing
                     nticks=15)  # Set the maximum number of ticks on the x-axis
    
    fig.show()
else:
    st.write('Please select a country.')