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

st.title('🕹 Casino Time')


player_name = st.text_input('📇 Your Name', help="If you are willing to enter your friend's name, just a small note that winner will get an actual mini prize :)")
start_button = st.button('🏁 Start')

if not start_button:

  rule_modal = st.expander('📝 Game Rules')

  rule_modal.write('👉🏻 Each Player will be displayed 3 buttons.')
  rule_modal.write('🏎 Each Player will play for 200 rounds.')
  rule_modal.write('👀 Each Player has to click a button in each round.')
  rule_modal.write('💵 This will yield a reward corresponding to that button.')
  rule_modal.write('👑 The Player with the highest accumulated reward wins the game.')
  rule_modal.write('👩🏼‍❤️‍👨🏻 Cooperation is not allowed.')
  rule_modal.write('👔 Ties are broken first by number of hints used, lesser is better.')
  rule_modal.write('⏰ If further ties appear they are broken by lesser time taken.')
  rule_modal.write('🏁 Click Start when ready to play.')

  hint_modal = st.expander('🔍 Hints')

  hint_modal.write('📈 Although the rewards are stochastic, there is a pattern in this random madness.')
  hint_modal.write('🙇🏼‍♂️ Random Button Clicks or Strategical Game Play?')
  hint_modal.write('🔆 You would have 3 💡 hints available to you, which are nothing but your own logs.')
  hint_modal.write('💔 Clicking on the 💡hint will display your logs and will immediately decrease hint count by 1.')

else:
  if len(player_name) == 0:
    st.error('Anonymous Players are not allowed! Please Enter a Name.', icon="🚨")
    time.sleep(3)
    st.experimental_rerun()
  else:
    nav_page('GamePlay')

st.warning('Do not Reload the page anytime until results are shown!', icon='⚠️')