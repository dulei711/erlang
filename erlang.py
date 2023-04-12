import streamlit as st
from decimal import Decimal
import math

def erlang_c(num_agents, traffic_intensity):
    a = (traffic_intensity ** num_agents) / math.factorial(num_agents)
    b = sum([(traffic_intensity ** i) / math.factorial(i) for i in range(num_agents)])
    return Decimal(a) / (Decimal(a) + Decimal(b))

st.set_page_config(page_title="Call Center Staffing Calculator", page_icon=":telephone_receiver:")

st.title('Call Center Staffing Calculator')

st.markdown('This webapp calculates the number of agents required to meet a desired service level in a call center, based on predicted call volume and average handling time.')

call_volume = st.number_input('Enter predicted call volume per hour:', min_value=1, max_value=10000, value=100)

avg_handle_time = st.number_input('Enter average call handling time (in minutes):', min_value=1, max_value=60, value=5)

traffic_intensity = Decimal(call_volume) * (Decimal(avg_handle_time) / Decimal(60))

service_levels = list(range(80, 100, 1))

num_agents_required = []
for service_level in service_levels:
    num_agents = 1
    while erlang_c(num_agents, traffic_intensity) < (Decimal(service_level) / Decimal(100)):
        num_agents += 1
    num_agents_required.append(num_agents)

# Show chart to visualize optimization
st.subheader('Optimization for Required Number of Agents')
chart_data = {"Service Levels": service_levels, "Agents Required": num_agents_required}
df = pd.DataFrame(chart_data)
fig = px.line(df, x="Service Levels", y="Agents Required")
st.plotly_chart(fig, use_container_width=True)

st.markdown('---')

st.subheader('Erlang Calculator')

st.markdown('Use this calculator to estimate the traffic intensity and service level of your call center.')

erlang_call_volume = st.number_input('Enter the call volume in a given time interval:', min_value=1, max_value=10000, value=100)

erlang_avg_handle_time = st.number_input('Enter the average handling time per call (in minutes):', min_value=1, max_value=60, value=5)

erlang_interval_time = st.number_input('Enter the length of the time interval (in minutes):', min_value=1, max_value=60, value=30)

erlang_traffic_intensity = Decimal(erlang_call_volume) / (Decimal(erlang_interval_time) / Decimal(erlang_avg_handle_time))

erlang_num_agents = st.number_input('Enter the number of agents:', min_value=1, max_value=1000, value=1)

erlang_service_levels = list(range(80, 100, 1))

erlang_service_levels_achieved = []
for erlang_service_level in erlang_service_levels:
    erlang_traffic_intensity_per_agent = erlang_traffic_intensity / Decimal(erlang_num_agents)
    erlang_service_level_achieved = erlang_c(erlang_num_agents, erlang_traffic_intensity_per_agent) * Decimal(100)
    erlang_service_levels_achieved.append(erlang_service_level_achieved)

# Show chart to visualize optimization
st.subheader('Optimization for Achieved Service Levels')
chart_data = {"Service Levels": erlang_service_levels, "Achieved Service Levels": erlang_service_levels_achieved}
df = pd.DataFrame(chart_data)
fig = px.line(df, x="Service Levels", y="Achieved Service Levels")
st.plotly_chart(fig, use_container_width=True)
