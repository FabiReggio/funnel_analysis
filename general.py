import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Step 1: Load the data
home_df = pd.read_csv('home_page_table.csv')     
search_df = pd.read_csv('search_page_table.csv') 
payment_df = pd.read_csv('payment_page_table.csv') 
confirmation_df = pd.read_csv('payment_confirmation_table.csv')
user_df = pd.read_csv('user_table.csv')

# Step 2: Count unique users at each stage

total_home_visits = home_df['user_id'].nunique() #90400
total_search_visits = search_df['user_id'].nunique() #45200
total_payment_visits = payment_df['user_id'].nunique() #6030
total_confirmations = confirmation_df['user_id'].nunique() #452

# Step 3: Calculate conversion rates

search_conversion_rate = (total_search_visits / total_home_visits) * 100 if total_home_visits > 0 else 0             #50
payment_conversion_rate = (total_payment_visits / total_search_visits) * 100 if total_search_visits > 0 else 0       #13.3
confirmation_conversion_rate = (total_confirmations / total_payment_visits) * 100 if total_payment_visits > 0 else 0 #7.4

# Step 4: Identify drop-off points

drop_off_home_to_search = total_home_visits - total_search_visits              #45200
drop_off_search_to_payment = total_search_visits - total_payment_visits        #39170
drop_off_payment_to_confirmation = total_payment_visits - total_confirmations  #5578

# Print results

print(f"Total Home Visits: {total_home_visits}")
print(f"Total Search Visits: {total_search_visits}")
print(f"Total Payment Visits: {total_payment_visits}")
print(f"Total Confirmations: {total_confirmations}")

print(f"Search Conversion Rate: {search_conversion_rate:.2f}%")
print(f"Payment Conversion Rate: {payment_conversion_rate:.2f}%")
print(f"Confirmation Conversion Rate: {confirmation_conversion_rate:.2f}%")

print(f"Drop-off from Home to Search: {drop_off_home_to_search}")
print(f"Drop-off from Search to Payment: {drop_off_search_to_payment}")
print(f"Drop-off from Payment to Confirmation: {drop_off_payment_to_confirmation}")

# Step 5: Visualize the conversion funnel - Option 1

funnel_data = {
    'Stage': ['Home', 'Search', 'Payment', 'Confirmation'],
    'Users': [total_home_visits, total_search_visits, total_payment_visits, total_confirmations]
}

funnel_df = pd.DataFrame(funnel_data)

plt.figure(figsize=(10, 6))
plt.bar(funnel_df['Stage'], funnel_df['Users'], color='skyblue')
plt.title('E-commerce Conversion Funnel')
plt.xlabel('Funnel Stage')
plt.ylabel('Number of Users')
plt.xticks(rotation=45)
plt.show()


# Step 5 - Visualize the conversion funnel - Option 2

# Data for the funnel chart
funnel_data = {
    'Stage': ['Home', 'Search', 'Payment', 'Confirmation'],
    'Users': [total_home_visits, total_search_visits, total_payment_visits, total_confirmations]
}

# Create a funnel chart
fig = go.Figure(go.Funnel(
    y=funnel_data['Stage'],
    x=funnel_data['Users'],
    textinfo="value+percent initial"
))

# Update layout
fig.update_layout(
    title='E-commerce Conversion Funnel',
    funnelmode="stack",  # Stack mode for a cumulative view
)

# Show the funnel chart
fig.show()