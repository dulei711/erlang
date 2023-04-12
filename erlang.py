import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

def erlang_c(num_agents, traffic_intensity):
    a = (traffic_intensity ** num_agents) / math.factorial(num_agents)
    b = sum([(traffic_intensity ** i) / math.factorial(i) for i in range(num_agents)])
    return a / (a + b)

st.set_page_config(page_title="Call Center Staffing Calculator", page_icon=":telephone_receiver:")

st.title('Call Center Staffing Calculator')

st.markdown('This webapp calculates the number of agents required to meet a desired service level in a call center, based on predicted call volume and average handling time.')

call_volume = st.number_input('Enter predicted call volume per hour:', min_value=1, max_value=10000, value=100)

avg_handle_time = st.number_input('Enter average call handling time (in minutes):', min_value=1, max_value=60, value=5)

traffic_intensity = call_volume * (avg_handle_time / 60)

service_levels = list(range(80, 100, 1))

num_agents_required = []
for service_level in service_levels:
    num_agents = 1
    while erlang_c(num_agents, traffic_intensity) < (service_level / 100):
        num_agents += 1
    num_agents_required.append(num_agents)

fig1, ax1 = plt.subplots()
ax1.plot(service_levels, num_agents_required)
ax1.set_title('Call Center Staffing Optimization')
ax1.set_xlabel('Service Level')
ax1.set_ylabel('Number of Agents Required')
st.pyplot(fig1)

st.markdown('---')

st.subheader('Erlang Calculator')

st.markdown('Use this calculator to estimate the traffic intensity and service level of your call center.')

erlang_call_volume = st.number_input('Enter the call volume in a given time interval:', min_value=1, max_value=10000, value=100)

erlang_avg_handle_time = st.number_input('Enter the average handling time per call (in minutes):', min_value=1, max_value=60, value=5)

erlang_interval_time = st.number_input('Enter the length of the time interval (in minutes):', min_value=1, max_value=60, value=30)

erlang_traffic_intensity = erlang_call_volume / (erlang_interval_time / erlang_avg_handle_time)

erlang_num_agents = st.number_input('Enter the number of agents:', min_value=1, max_value=1000, value=1)

erlang_service_levels = list(range(80, 100, 1))

erlang_service_levels_achieved = []
for erlang_service_level in erlang_service_levels:
    erlang_traffic_intensity_per_agent = erlang_traffic_intensity / erlang_num_agents
    erlang_service_level_achieved = erlang_c(erlang_num_agents, erlang_traffic_intensity_per_agent) * 100
    erlang_service_levels_achieved.append(erlang_service_level_achieved)

fig2, ax2 = plt.subplots()
ax2.plot(erlang_service_levels, erlang_service_levels_achieved)
ax2.set_title('Erlang Calculator Optimization')
ax2.set_xlabel('Desired Service Level')
ax2.set_ylabel('Achieved Service Level')
st.pyplot(fig2)
