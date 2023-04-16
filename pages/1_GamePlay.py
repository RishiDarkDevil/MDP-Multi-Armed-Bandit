# To prevent warning errors in pandas DataFrames
import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import pandas as pd
import numpy as np
import time
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

if 'round' in st.session_state and st.session_state.round == 20:
  nav_page('Result')

st.title('🦾 Pull an Arm')

# Hard-Coding it as of now
if 'expected_rewards' not in st.session_state:
  st.session_state['expected_rewards'] = np.random.choice([4, 8, 10], 3, False)

if 'std_rewards' not in st.session_state:
  st.session_state['std_rewards'] = 3

col1, col2, col3 = st.columns([1,1,1])

with col1:
  st.button('🕹', key='left', use_container_width=True)
with col2:
  st.button('🕹', key='middle', use_container_width=True)
with col3:
  st.button('🕹', key='right', use_container_width=True)

# st.write(st.session_state.expected_rewards)

if 'round' not in st.session_state:
  st.session_state['round'] = 0

if 'max_round_list' not in st.session_state:
  st.session_state['max_round_list'] = list()

if 'earned' not in st.session_state:
  st.session_state['earned'] = 0

if 'response' not in st.session_state:
  st.session_state['response'] = {'left': [], 'middle': [], 'right': []}

if 'hint_count' not in st.session_state:
  st.session_state['hint_count'] = 3

if 'earn_list' not in st.session_state:
  st.session_state['earn_list'] = list()

rdisp, edisp, sdisp = st.columns([1,1,1])
_, hdisp, _ = st.columns([1,1,1])

if st.session_state.left:
  val = int(np.random.randn(1)*st.session_state.std_rewards + st.session_state.expected_rewards[0])
  val_left = val
  val_middle = int(np.random.randn(1)*st.session_state.std_rewards + st.session_state.expected_rewards[1])
  val_right = int(np.random.randn(1)*st.session_state.std_rewards + st.session_state.expected_rewards[2])
  st.session_state.max_round_list.append(max(val_left, val_middle, val_right))
  st.session_state.earned += val
  pos = '+' if val >= 0 else '-'
  st.session_state.response['left'].append(val)
  st.session_state.response['middle'].append('NA')
  st.session_state.response['right'].append('NA')
  edisp.write(f'## Earned {pos}{abs(val)}')
  st.session_state.round += 1
  st.session_state.earn_list.append(st.session_state.earned)
  if 'time' not in st.session_state:
    st.session_state['time'] = time.time()
    st.info('Time has started', icon='⏰')
  if 'round' in st.session_state and st.session_state.round == 20:
    st.session_state.time = time.time() - st.session_state.time
    nav_page('Result')

if st.session_state.middle:
  val = int(np.random.randn(1)*st.session_state.std_rewards + st.session_state.expected_rewards[1])
  val_left = int(np.random.randn(1)*st.session_state.std_rewards + st.session_state.expected_rewards[0])
  val_middle = val
  val_right = int(np.random.randn(1)*st.session_state.std_rewards + st.session_state.expected_rewards[2])
  st.session_state.max_round_list.append(max(val_left, val_middle, val_right))
  st.session_state.earned += val
  pos = '+' if val >= 0 else '-'
  st.session_state.response['left'].append('NA')
  st.session_state.response['middle'].append(val)
  st.session_state.response['right'].append('NA')
  edisp.write(f'## Earned {pos}{abs(val)}')
  st.session_state.round += 1
  st.session_state.earn_list.append(st.session_state.earned)
  if 'time' not in st.session_state:
    st.session_state['time'] = time.time()
    st.info('Time has started', icon='⏰')
  if 'round' in st.session_state and st.session_state.round == 20:
    st.session_state.time = time.time() - st.session_state.time
    nav_page('Result')

if st.session_state.right:
  val = int(np.random.randn(1)*st.session_state.std_rewards + st.session_state.expected_rewards[2])
  val_left = int(np.random.randn(1)*st.session_state.std_rewards + st.session_state.expected_rewards[0])
  val_middle = int(np.random.randn(1)*st.session_state.std_rewards + st.session_state.expected_rewards[1])
  val_right = val
  st.session_state.max_round_list.append(max(val_left, val_middle, val_right))
  st.session_state.earned += val
  pos = '+' if val >= 0 else '-'
  st.session_state.response['left'].append('NA')
  st.session_state.response['middle'].append('NA')
  st.session_state.response['right'].append(val)
  edisp.write(f'## Earned {pos}{abs(val)}')
  st.session_state.round += 1
  st.session_state.earn_list.append(st.session_state.earned)
  if 'time' not in st.session_state:
    st.session_state['time'] = time.time()
    st.info('Time has started', icon='⏰')
  if 'round' in st.session_state and st.session_state.round == 20:
    st.session_state.time = time.time() - st.session_state.time
    nav_page('Result')

# Display Score
if st.session_state.earned > 0:
  sdisp.write(f'## Score: {st.session_state.earned}')
if 'round' in st.session_state and st.session_state.round == 20:
  st.session_state.time = time.time() - st.session_state.time
  nav_page('Result')

# Display Round
if st.session_state.round > 0:
  rdisp.write(f'## Round: {st.session_state.round}')
if 'round' in st.session_state and st.session_state.round == 20:
  st.session_state.time = time.time() - st.session_state.time
  nav_page('Result')

# Display Hint Button
hc = '💡'* st.session_state.hint_count
hdisp.button(f'{hc} Hint', use_container_width=True, key='hint')

# Handle When hint Button Clicked
if st.session_state.hint:
  if st.session_state.hint_count > 0:
    response = pd.DataFrame(st.session_state.response)
    response.index.name = 'Round'
    st.table(response)
    st.session_state.hint_count -= 1
  else:
    st.error('No more hints available!', icon='❌')

