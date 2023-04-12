import streamlit as st
from math import factorial

def erlang_c(num_agents, traffic_intensity):
    a = traffic_intensity ** num_agents / factorial(num_agents)
    b = sum(traffic_intensity ** i / factorial(i) for i in range(num_agents))
    return a / (a + b)

st.title('Call Center Staffing Calculator')

call_volume = st.number_input('Enter predicted call volume per hour:', min_value=1, max_value=10000, value=100)
avg_handle_time = st.number_input('Enter average call handling time (in minutes):', min_value=1, max_value=60, value=5)
traffic_intensity = call_volume * (avg_handle_time / 60)

service_level = st.slider('Select desired service level:', min_value=80, max_value=99, value=90, step=1)

num_agents = sum(erlang_c(i, traffic_intensity) < (service_level / 100) for i in range(1, 1000))

st.write(f'The required number of agents to achieve a service level of {service_level}% is {num_agents}.')
