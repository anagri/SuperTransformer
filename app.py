import os
import logging
import cohere
from cohere.classify import Example

from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

api_key = os.environ["COHERE_API_KEY"]
model_id = os.environ["COHERE_MODEL_ID"]
co = cohere.Client(api_key)
categories = ["Now", "Later", "Delegate", "Discard"]
y_pos = np.arange(len(categories))

"""
# Welcome to SuperTransformer!

Enter email subject, body and click to Categorize! to find the priority of this email
"""

form = st.form('inbox')
with form:
  subject = st.text_input("Subject", key="subject")
  body = st.text_area("Body", key="body")
  submit = st.form_submit_button("Categorize!" )
  if submit:
    if subject == "":
      st.error("Subject cannot be blank")
    else:
      input = f"{subject.strip()}"
      if body != "":
        input +=  f"<body> {body.strip()}"
      try:
        response = co.classify(
          model=model_id,
          inputs=[input])
        logging.info(f"Received response from cohere - {response}")
        prediction = response.classifications[0].prediction
        if not prediction or prediction not in categories:
          st.error(f"Unknown prediction from API: {prediction}")
        else:
          st.write(f"Label: {prediction}")
          pred_map = {c.label: c.confidence for c in response.classifications[0].confidence}
          predictions = [pred_map[c] for c in categories]
          fig, ax = plt.subplots()
          ax.barh(y_pos, predictions, align='center')
          ax.set_yticks(y_pos, labels=categories)
          ax.invert_yaxis()
          ax.set_xlabel('Predictions')
          ax.set_xlim([0.0, 1.0])
          st.pyplot(fig)
      except Exception as e:
        st.error(f"Error calling Cohere API: {type(e)}: {e.message}")
