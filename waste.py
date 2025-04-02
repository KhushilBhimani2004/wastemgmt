import streamlit as st
import plotly.express as px
import pandas as pd

# Load cleaned data
df = pd.read_csv('waste.csv')

df_cleaned = df.iloc[5:].reset_index(drop=True)
df_cleaned.columns = [
    "Sr No", "State/UT", "MSW Generation (MMTPA)", "Total Waste Generation (TPD)",
    "Total Waste Collection (TPD)", "Total Waste Treatment (TPD)", "No. of Compost Plants",
    "No. of Dumpsites", "Collection Rate (%)", "Treatment Rate (%)"
]
df_cleaned = df_cleaned.dropna(subset=["State/UT"]).reset_index(drop=True)

numeric_columns = [
    "MSW Generation (MMTPA)", "Total Waste Generation (TPD)", "Total Waste Collection (TPD)",
    "Total Waste Treatment (TPD)", "No. of Compost Plants", "No. of Dumpsites",
    "Collection Rate (%)", "Treatment Rate (%)"
]
df_cleaned[numeric_columns] = df_cleaned[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Replace NaN values in size-related and color-related columns with a small default value
df_cleaned['Total Waste Generation (TPD)'].fillna(1, inplace=True)
df_cleaned['Treatment Rate (%)'].fillna(0, inplace=True)

# Streamlit UI
st.title("Municipal Solid Waste Dashboard")
st.markdown("### Insights from Municipal Solid Waste Data")

# Total Waste Generation
fig1 = px.bar(
    df_cleaned, x='State/UT', y='Total Waste Generation (TPD)',
    title='Total Waste Generation by State', color='Total Waste Generation (TPD)',
    color_continuous_scale='blues'
)
st.plotly_chart(fig1)

# Collection vs Treatment
fig2 = px.scatter(
    df_cleaned, x='Total Waste Collection (TPD)', y='Total Waste Treatment (TPD)',
    hover_name='State/UT', title='Collection vs. Treatment Efficiency',
    size='Total Waste Generation (TPD)', color='Treatment Rate (%)',
    color_continuous_scale='viridis'
)
st.plotly_chart(fig2)

# Dumpsites by State
fig3 = px.bar(
    df_cleaned, x='State/UT', y='No. of Dumpsites',
    title='Number of Dumpsites by State', color='No. of Dumpsites',
    color_continuous_scale='reds'
)
st.plotly_chart(fig3)

# Compost Plants Availability
fig4 = px.scatter(
    df_cleaned, x='State/UT', y='No. of Compost Plants',
    size='Total Waste Generation (TPD)', title='Compost Plants Availability',
    color='No. of Compost Plants', color_continuous_scale='greens'
)
st.plotly_chart(fig4)
