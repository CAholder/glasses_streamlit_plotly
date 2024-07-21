import streamlit as st
import pandas as pd
import plotly.express as px

# Set page title
st.set_page_config(page_title="Glasses Frames Inventory Dashboard", layout="wide")

# Function to load data
@st.cache_data
def load_data():
    return pd.read_csv('glasses_frames_data.csv')

# Function to create sorted bar chart
def create_sorted_bar_chart_frame_type(data, sort_by, title):
    if sort_by == 'Frame Type (A-Z)':
        data = data.sort_values('Frame Type')
    elif sort_by == 'Inventory (Low to High)':
        data = data.sort_values('Inventory Count')
    elif sort_by == 'Inventory (High to Low)':
        data = data.sort_values('Inventory Count', ascending=False)
    else:
        data = data

    fig = px.bar(data, x=title, y='Inventory Count',
                 title=f'Total Inventory by {title}',
                 labels={'Inventory Count': 'Total Inventory'},
                 color=title)

    fig.update_layout(xaxis_title=title,
                      yaxis_title='Total Inventory',
                      showlegend=False)
    return fig

def create_sorted_bar_chart_brand_type(data, sort_by, title):
    if sort_by == 'Brand Type (A-Z)':
        data = data.sort_values('Brand')
    elif sort_by == 'Inventory (Low to High)':
        data = data.sort_values('Inventory Count')
    elif sort_by == 'Inventory (High to Low)':
        data = data.sort_values('Inventory Count', ascending=False)
    else:
        data = data

    fig = px.bar(data, x=title, y='Inventory Count',
                 title=f'Total Inventory by {title}',
                 labels={'Inventory Count': 'Total Inventory'},
                 color=title)

    fig.update_layout(xaxis_title=title,
                      yaxis_title='Total Inventory',
                      showlegend=False)
    return fig


# Load the data
df = load_data()

# Calculate total inventory per frame type
inventory_by_frame = df.groupby('Frame Type')['Inventory Count'].sum().reset_index()
inventory_by_brand = df.groupby('Brand')['Inventory Count'].sum().reset_index()

# Create the bar chart
fig = px.bar(inventory_by_frame, x='Frame Type', y='Inventory Count',
             title='Total Inventory by Frame Type',
             labels={'Inventory Count': 'Total Inventory'},
             color='Frame Type')

# Customize the layout
fig.update_layout(xaxis_title='Frame Type',
                  yaxis_title='Total Inventory',
                  showlegend=False)

fig_brand = px.bar(inventory_by_brand, x='Brand', y='Inventory Count',
                   title='Total Inventory by Brand',
                   labels={'Inventory Count': 'Total Inventory'},
                   color='Brand')

fig_brand.update_layout(xaxis_title='Brand',
                        yaxis_title='Total Inventory',
                        showlegend=False)

# Streamlit app
st.title('Glasses Frames Inventory Dashboard')

sort_options = ['Frame Type (A-Z)', 'Brand Type (A-Z)','Inventory (Low to High)', 'Inventory (High to Low)']
sort_by = st.selectbox('Sort by:', sort_options)

# Add a filter for brands
st.sidebar.header('Filters')
# selected_brands = st.sidebar.multiselect('Select Brands', options=df['Brand'].unique(), default=df['Brand'].unique())
selected_brands = st.sidebar.multiselect('Select Brands', options=df['Brand'].unique(), default="Burberry")

# Filter the dataframe
filtered_df = df[df['Brand'].isin(selected_brands)]

# Update the bar chart with filtered data
filtered_inventory_by_frame = filtered_df.groupby('Frame Type')['Inventory Count'].sum().reset_index()
filtered_fig = px.bar(filtered_inventory_by_frame, x='Frame Type', y='Inventory Count',
                      title='Total Inventory by Frame Type (Filtered)',
                      labels={'Inventory Count': 'Total Inventory'},
                      color='Frame Type')
filtered_fig.update_layout(xaxis_title='Frame Type',
                           yaxis_title='Total Inventory',
                           showlegend=False)
filtered_fig = create_sorted_bar_chart_frame_type(filtered_inventory_by_frame, sort_by, filtered_fig.layout.xaxis.title.text)


# Display the filtered bar chart
st.plotly_chart(filtered_fig, use_container_width=True)

# Display the bar chart
if sort_options == 'Frame Type (A-Z)':
    fig = create_sorted_bar_chart_frame_type(inventory_by_frame, sort_by, fig.layout.xaxis.title.text)
    st.plotly_chart(fig, use_container_width=True)
elif sort_options == 'Brand type (A-Z)':
    fig_brand = create_sorted_bar_chart_brand_type(inventory_by_brand, sort_by, fig_brand.layout.xaxis.title.text)
    st.plotly_chart(fig_brand, use_container_width=True)
else:
    fig = create_sorted_bar_chart_frame_type(inventory_by_frame, sort_by, fig.layout.xaxis.title.text)
    st.plotly_chart(fig, use_container_width=True)
    fig_brand = create_sorted_bar_chart_brand_type(inventory_by_brand, sort_by, fig_brand.layout.xaxis.title.text)
    st.plotly_chart(fig_brand, use_container_width=True)
# Display the raw data
st.subheader('Raw Data')
st.dataframe(df)

# Add some statistics
st.subheader('Statistics')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric('Total Frames', df['Inventory Count'].sum())
with col2:
    st.metric('Average Price', f"${df['Price'].mean():.2f}")
with col3:
    st.metric('Number of Brands', df['Brand'].nunique())

