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

_, tdisp, _ = st.columns([1,1,1])
tdisp.title('🎉 Results')
# tdisp.write('## 🌟 Highlights')

st.snow()

# Display Score, Time Taken, Hints Used
sdisp, tmdisp, hcdisp = st.columns([1,1,1])
sdisp.write(f'## Score: {st.session_state.earned}')
tmdisp.write(f'## Time: {round(st.session_state.time, 2)}')
hcdisp.write(f'## Hints Used: {3-st.session_state.hint_count}')

# _, adisp, _ = st.columns([1,1,1])
# adisp.write('## 📈 Analytics')

arr = st.session_state.earn_list
max_arr = list(np.cumsum(st.session_state.max_round_list))

# Cumulative Reward Plot
fig, ax = plt.subplots()
ax.plot(list(range(len(arr))), arr, 'o--', label='Your Performance')
ax.plot(list(range(len(max_arr))), max_arr, 'o--', label='Optimal Performance')
ax.plot()
ax.set_xlabel('Rounds')
ax.set_ylabel('Cumulative Reward')
ax.title.set_text('Tally your Performance to the Optimal')
ax.xaxis.get_major_locator().set_params(integer=True) 
ax.yaxis.get_major_locator().set_params(integer=True)
ax.legend(loc='upper left')

st.pyplot(fig)

# Button Distribution

mus = st.session_state.expected_rewards
sigma = st.session_state.std_rewards

fig, ax = plt.subplots()
x = np.linspace(min(mus) - 3*sigma, max(mus) + 3*sigma, 100)
ax.plot(x, stats.norm.pdf(x, mus[0], sigma), label='Left Arm')
ax.plot(x, stats.norm.pdf(x, mus[1], sigma), label='Middle Arm')
ax.plot(x, stats.norm.pdf(x, mus[2], sigma), label='Right Arm')
ax.title.set_text('Your Arm Distributions')
ax.legend()

st.pyplot(fig)

st.columns([0.1,1,0.1])[1].write('### 🤺 Wanna see how you tally up against Agents?')

# Agent Page
_, adisp, _ = st.columns([1,1,1])
adisp.button('👾 Click Me', key='agent', use_container_width=True)

if st.session_state.agent:
  nav_page('Agent')