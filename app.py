import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config (Ensure it's the first Streamlit command)
st.set_page_config(page_title="Campaign Performance Dashboard", layout="wide")

# Load the data
file_path = 'Data/conversion_data.csv'
data = pd.read_csv(file_path)

# Sidebar options for grouping
st.sidebar.header("Group by Options")
group_by_options = st.sidebar.multiselect(
    "Select columns to group by:",
    options=["xyz_campaign_id", "age", "gender", "interest"],
    default=["xyz_campaign_id"]
)

if not group_by_options:
    st.warning("Please select at least one grouping option.")
    st.stop()

# Aggregate data
segment_groups = data.groupby(group_by_options).agg({
    'Impressions': 'sum',
    'Clicks': 'sum',
    'Spent': 'sum',
    'Total_Conversion': 'sum',
    'Approved_Conversion': 'sum',
    'ad_id': 'nunique'
}).reset_index()

# Rename column
segment_groups.rename(columns={'ad_id': 'Count of Ads'}, inplace=True)

# Compute additional metrics
segment_groups['Click-Through Rate'] = ((segment_groups['Clicks'] / segment_groups['Impressions']) * 100).fillna(0).round(4).astype(str) + "%"
segment_groups['Conversion Rate'] = ((segment_groups['Total_Conversion'] / segment_groups['Clicks']) * 100).fillna(0).round(0).astype(int).astype(str) + "%"
segment_groups['Cost per Conversion'] = (segment_groups['Spent'] / segment_groups['Total_Conversion']).fillna(0).round(0)
segment_groups['Approved Conversion Rate'] = ((segment_groups['Approved_Conversion'] / segment_groups['Clicks']) * 100).fillna(0).round(0).astype(int).astype(str) + "%"
segment_groups['Cost per Approved Conversion'] = (segment_groups['Spent'] / segment_groups['Approved_Conversion']).fillna(0).round(0)

# Display Title
st.title("Campaign Performance Dashboard")
st.markdown("""
This dashboard provides insights into campaign performance metrics, including Click-Through Rate (CTR), Conversion Rate, and Spend Analysis.

- **CTR:** Percentage of impressions that resulted in clicks.
- **Conversion Rate:** Percentage of clicks that led to conversions.
- **Spend Analysis:** How budget allocation varies across segments.
""")

# Display the aggregated table
st.dataframe(segment_groups, use_container_width=True)

# CTR Plot
fig_ctr = px.bar(
    segment_groups, 
    x=group_by_options[0], 
    y='Click-Through Rate', 
    title='Click-Through Rate by Segment', 
    text='Click-Through Rate'
)
st.plotly_chart(fig_ctr, use_container_width=True)

# Spend Plot
fig_spend = px.bar(
    segment_groups, 
    x=group_by_options[0], 
    y='Spent', 
    title='Total Spend by Segment',
    text='Spent',
    color='Spent'
)
st.plotly_chart(fig_spend, use_container_width=True)
