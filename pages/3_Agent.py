# To prevent warning errors in pandas DataFrames
import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.stats as stats
from streamlit.components.v1 import html

st.set_page_config(initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

def nav_page(page_name, timeout_secs=3):
  nav_script = """
      <script type="text/javascript">
          function attempt_nav_page(page_name, start_time, timeout_secs) {
              var links = window.parent.document.getElementsByTagName("a");
              for (var i = 0; i < links.length; i++) {
                  if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                      links[i].click();
                      return;
                  }
              }
              var elasped = new Date() - start_time;
              if (elasped < timeout_secs * 1000) {
                  setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
              } else {
                  alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
              }
          }
          window.addEventListener("load", function() {
              attempt_nav_page("%s", new Date(), %d);
          });
      </script>
  """ % (page_name, timeout_secs)
  html(nav_script)

plt.style.use('dark_background')

_, tidisp, _ = st.columns([1,1,1])
tidisp.title('🤖 Agents')

_, egdisp, _ = st.columns([0.5,1,0.5])
egdisp.write('## 🤑 ε-Greedy Method')

st.checkbox('Use Random Expected Rewards for Each Arm for Each Agent (Set `Independent Agents > 1`)', True, key='rand', help='It checks the robustness of the strategy')

ldisp, mdisp, rdisp = st.columns([1,1,1])
ldisp.number_input('Left Arm', 1, 20, st.session_state.expected_rewards[0], 1, '%d', key='lexp', help='Expected Left Arm Reward', disabled=st.session_state.rand)
mdisp.number_input('Middle Arm', 1, 20, st.session_state.expected_rewards[1], 1, '%d', key='mexp', help='Expected Middle Arm Reward', disabled=st.session_state.rand)
rdisp.number_input('Right Arm', 1, 20, st.session_state.expected_rewards[2], 1, '%d', key='rexp', help='Expected Right Arm Reward', disabled=st.session_state.rand)

ldisp.slider('Exploration ε', 0.0, 1.0, 0.05, 0.01, '%f', key='epsilon', help='Controls Exploration')
mdisp.slider('Step Size', 0.0, 10.0, 0.1, 0.1, '%f', key='step_size', help='Controls Sensitivity to Reward Obtained')
rdisp.slider('Independent Agents', 1, 1000, 1, 1, '%d', key='num_agents', help='Number of Independent Agents')

ldisp.slider('Episode Length', 100, 1000, 200, 10, '%d', key='num_eps', help='Number of Episodes for Each Agent')
mdisp.slider('Initial Values', -20, 20, 0, 1, '%d', key='op_start', help='The Starting Value Estimate for Each Arm')
rdisp.slider('Episode Visualization Gap', 1, 1000, 10, 10, '%d', key='viz_gap', help='The number of episodes after which the plot will be updated')

mdisp.button('🏃🏻‍♂️ Run Simulation', key='run', use_container_width=True)

# Handle Simulation
if st.session_state.run:
  fig, ax = plt.subplots()

  arm_exps = np.array([st.session_state.lexp, st.session_state.mexp, st.session_state.rexp])
  # Q-values
  q_values = np.array([st.session_state.op_start, st.session_state.op_start, st.session_state.op_start])

  sum_over_runs = np.array([0] * st.session_state.num_eps, dtype=np.float32)

  if st.session_state.rand:
    ax.set_ylim(0, 20 + 3*1) # Edit Standard Dev
  else:
    ax.set_ylim(0, max(st.session_state.lexp, st.session_state.mexp, st.session_state.rexp) + 3*1) # Edit Standard Dev
  line, = ax.plot(list(range(st.session_state.num_eps)), sum_over_runs)
  avg_line, = ax.plot(list(range(st.session_state.num_eps)), sum_over_runs)
  the_plot = st.pyplot(plt)

  def init():  # give a clean slate to start
    line.set_ydata([np.nan] * st.session_state.num_eps)
    avg_line.set_ydata([np.nan] * st.session_state.num_eps)

  def animate(cumrewards, avgrewards):  # update the y values
    line.set_ydata(np.array(list(cumrewards) + [np.nan] * (st.session_state.num_eps - len(cumrewards)), dtype=np.float32))
    avg_line.set_ydata(avgrewards)
    the_plot.pyplot(plt)

  def argmax(q_values):
    """argmax with random tie-breaking
    Args:
      q_values (Numpy array): the array of action-values
    Returns:
      action (int): an action with the highest value
    """
    top = float("-inf")
    ties = []

    for i in range(len(q_values)):
      if q_values[i] > top:
        top = q_values[i]
        ties = []

      if q_values[i] == top:
        ties.append(i)

    return np.random.choice(ties)

  def agent_policy(q_vals):
    """
    epsilon greedy policy
    """
    if np.random.uniform() > st.session_state.epsilon:
      return argmax(q_vals)
    else:
      return np.random.choice([0,1,2])

  def get_cumrewards(cumrewards, q_vals):
    choice_arm = agent_policy(q_vals)
    reward_arm = float(int(np.random.randn(1) * 1 + arm_exps[choice_arm])) # Edit Standard Dev
    q_vals[choice_arm] += st.session_state.step_size * (reward_arm - q_vals[choice_arm])
    new_cumreward = float(cumrewards[-1]) + reward_arm
    cumrewards.append(float(new_cumreward))
    # plot_cumrewards = cumrewards
    # plot_cumrewards.extend([np.nan] * (st.session_state.num_eps - len(cumrewards)))
    return cumrewards, q_vals

  init()
  for i in range(st.session_state.num_agents):

    # For each agent set different bandit problem
    if st.session_state.rand:
      arm_exps = np.random.choice(np.arange(1,21), 3, False)
    curr_cumrewards = [0.0]
    q_values = np.array([st.session_state.op_start, st.session_state.op_start, st.session_state.op_start])
    
    for j in range(st.session_state.num_eps-1):
      curr_cumrewards, q_values = get_cumrewards(curr_cumrewards, q_values)
      # st.write(curr_cumrewards)
      if (j+1) % st.session_state.viz_gap == 0:
        animate(
          np.array(curr_cumrewards, dtype=np.float32) / (np.arange(j+2) + 1), 
          list(sum_over_runs/(i+1))
          )
        time.sleep(0.0001)
      # st.write(np.array(curr_cumrewards, dtype=np.float32) / (np.arange(j+2) + 1))
    sum_over_runs += np.array(curr_cumrewards, dtype=np.float32) / (np.arange(st.session_state.num_eps)+1)
    # st.write(list(sum_over_runs/(i+1)))
    # st.write(list(np.array(curr_cumrewards, dtype=np.float32)))
    # st.write(sum_over_runs)
    # st.write(curr_cumrewards)