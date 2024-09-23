import pandas as pd
import plotly.graph_objects as go

# Step 1: Load the data
home_df = pd.read_csv('home_page_table.csv')     
search_df = pd.read_csv('search_page_table.csv') 
payment_df = pd.read_csv('payment_page_table.csv') 
confirmation_df = pd.read_csv('payment_confirmation_table.csv')
user_df = pd.read_csv('user_table.csv')

# Step 2: Count unique users at each stage by sex and device
def calculate_conversion_by_group(df, group_by):
    grouped = df.groupby(group_by)['user_id'].nunique()
    return grouped

# Unique users by sex
home_users_by_sex = calculate_conversion_by_group(home_df.merge(user_df, on='user_id'), ['sex'])
search_users_by_sex = calculate_conversion_by_group(search_df.merge(user_df, on='user_id'), ['sex'])
payment_users_by_sex = calculate_conversion_by_group(payment_df.merge(user_df, on='user_id'), ['sex'])
confirmation_users_by_sex = calculate_conversion_by_group(confirmation_df.merge(user_df, on='user_id'), ['sex'])

# Unique users by device
home_users_by_device = calculate_conversion_by_group(home_df.merge(user_df, on='user_id'), ['device'])
search_users_by_device = calculate_conversion_by_group(search_df.merge(user_df, on='user_id'), ['device'])
payment_users_by_device = calculate_conversion_by_group(payment_df.merge(user_df, on='user_id'), ['device'])
confirmation_users_by_device = calculate_conversion_by_group(confirmation_df.merge(user_df, on='user_id'), ['device'])

# Function to calculate conversion rates and drop-off points
def calculate_conversion_metrics(total_home, total_search, total_payment, total_confirmations):
    search_conversion_rate = (total_search / total_home) * 100 if total_home > 0 else 0
    payment_conversion_rate = (total_payment / total_search) * 100 if total_search > 0 else 0
    confirmation_conversion_rate = (total_confirmations / total_payment) * 100 if total_payment > 0 else 0
    
    drop_off_home_to_search = total_home - total_search
    drop_off_search_to_payment = total_search - total_payment
    drop_off_payment_to_confirmation = total_payment - total_confirmations
    
    return (search_conversion_rate, payment_conversion_rate, confirmation_conversion_rate,
            drop_off_home_to_search, drop_off_search_to_payment, drop_off_payment_to_confirmation)

# Calculate metrics for each sex
metrics_by_sex = {}
for sex in home_users_by_sex.index:
    metrics_by_sex[sex] = calculate_conversion_metrics(
        home_users_by_sex[sex], 
        search_users_by_sex.get(sex, 0), 
        payment_users_by_sex.get(sex, 0), 
        confirmation_users_by_sex.get(sex, 0)
    )

# Calculate metrics for each device
metrics_by_device = {}
for device in home_users_by_device.index:
    metrics_by_device[device] = calculate_conversion_metrics(
        home_users_by_device[device], 
        search_users_by_device.get(device, 0), 
        payment_users_by_device.get(device, 0), 
        confirmation_users_by_device.get(device, 0)
    )

# Print results for sex
print("Conversion Metrics by Sex:")
for sex, metrics in metrics_by_sex.items():
    print(f"{sex}: Search Conversion Rate: {metrics[0]:.2f}%, Payment Conversion Rate: {metrics[1]:.2f}%, "
          f"Confirmation Conversion Rate: {metrics[2]:.2f}%, "
          f"Drop-off Home to Search: {metrics[3]}, Drop-off Search to Payment: {metrics[4]}, "
          f"Drop-off Payment to Confirmation: {metrics[5]}")

# Print results for device
print("\nConversion Metrics by Device:")
for device, metrics in metrics_by_device.items():
    print(f"{device}: Search Conversion Rate: {metrics[0]:.2f}%, Payment Conversion Rate: {metrics[1]:.2f}%, "
          f"Confirmation Conversion Rate: {metrics[2]:.2f}%, "
          f"Drop-off Home to Search: {metrics[3]}, Drop-off Search to Payment: {metrics[4]}, "
          f"Drop-off Payment to Confirmation: {metrics[5]}")

# Step 5: Visualize the conversion funnel by sex using Plotly
funnel_data_sex = {
    'Stage': ['Home', 'Search', 'Payment', 'Confirmation'],
    'Male': [home_users_by_sex.get('Male', 0), search_users_by_sex.get('Male', 0), 
             payment_users_by_sex.get('Male', 0), confirmation_users_by_sex.get('Male', 0)],
    'Female': [home_users_by_sex.get('Female', 0), search_users_by_sex.get('Female', 0), 
               payment_users_by_sex.get('Female', 0), confirmation_users_by_sex.get('Female', 0)]
}

# Create a funnel chart for sex
fig_sex = go.Figure()

for sex in ['Male', 'Female']:
    fig_sex.add_trace(go.Funnel(
        name=sex,
        y=funnel_data_sex['Stage'],
        x=funnel_data_sex[sex],
        textinfo="value+percent initial"
    ))

# Update layout for sex funnel
fig_sex.update_layout(
    title='E-commerce Conversion Funnel by Sex',
    funnelmode="stack"
)

# Show the funnel chart for sex
fig_sex.show()

# Step 5: Visualize the conversion funnel by device using Plotly
funnel_data_device = {
    'Stage': ['Home', 'Search', 'Payment', 'Confirmation'],
    'Desktop': [home_users_by_device.get('Desktop', 0), search_users_by_device.get('Desktop', 0), 
                payment_users_by_device.get('Desktop', 0), confirmation_users_by_device.get('Desktop', 0)],
    'Mobile': [home_users_by_device.get('Mobile', 0), search_users_by_device.get('Mobile', 0), 
               payment_users_by_device.get('Mobile', 0), confirmation_users_by_device.get('Mobile', 0)]
}

# Create a funnel chart for device
fig_device = go.Figure()

for device in ['Desktop', 'Mobile']:
    fig_device.add_trace(go.Funnel(
        name=device,
        y=funnel_data_device['Stage'],
        x=funnel_data_device[device],
        textinfo="value+percent initial"
    ))

# Update layout for device funnel
fig_device.update_layout(
    title='E-commerce Conversion Funnel by Device',
    funnelmode="stack"
)

# Show the funnel chart for device
fig_device.show()