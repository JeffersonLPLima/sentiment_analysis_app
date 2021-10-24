import streamlit as st
import pickle, lzma
import numpy as np
import pandas as pd
from preprocessing  import Preprocess
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.write(f"""
         # Sentiment Analysis
         """)


st.text("")


@st.cache(allow_output_mutation=True)
def load_pipeline():
    return pickle.load(lzma.open('sentiment_classifier.lzma'))


model = load_pipeline() 

    
def classify_post(message_text):
  message_text = Preprocess().transform(texts=[message_text])
  prob = model['classifier'].predict_proba(model['vectorizer'].transform(message_text))[0]
  classification = model['classifier'].predict(model['vectorizer'].transform(message_text))[0]
  sent = "Neutral"
  if classification==2:
    sent = "Positive 😃"
    prob = str(round(prob[1],2)*100)+"%"
  elif classification == 0:
    sent = "Negative 😠"
    prob = str(round(prob[0],2)*100)+"%"
  return f"Sentiment {str(sent)} with {prob} of confidence."

 

message_text = st.text_input(f"Insert the message:")

if message_text != '':
  
  result = classify_post(message_text)
  
  st.write("Message: \""+message_text+"\"")
  st.text("\n")
  if("Negative" in result):
    st.error(result)
  elif("Neutral" in result):
    st.warning(result)
  else:
    st.success(result)


st.markdown("""\n\n---\n\n""")

 
with st.expander("Classifier Report"):
  dataframe = pd.DataFrame([[model['report']['2']['f1-score']],[model['report']['0']['f1-score']]],columns=["F1 Score"], index=["Positive", "Negative"])
  st.table(dataframe)
