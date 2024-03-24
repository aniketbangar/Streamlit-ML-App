import streamlit as st
import requests
from io import BytesIO
import pandas as pd
from requests.exceptions import RequestException
import re


# API endpoint URL
FILTER_URL = 'http://localhost:8000/autoworkflow/filter-dataframe'


def load_data(uploaded_file):
    """Loads data from uploaded file based on its extension."""
    if uploaded_file.name.split('.')[-1] == 'csv':
        data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.split('.')[-1] == 'xlsx':
        data = pd.read_excel(uploaded_file)
    elif uploaded_file.name.split('.')[-1] == 'tsv':
        data = pd.read_table(uploaded_file)
    elif uploaded_file.name.split('.')[-1] == 'json':
        data = pd.read_json(uploaded_file)
    return data

# Define Streamlit app
st.title("Filter DataFrame")

# Add upload file widget
uploaded_file = st.file_uploader("Upload file", type=['tsv', 'csv', 'json', 'xlsx'])

# If file is uploaded, display options to filter the DataFrame
if uploaded_file is not None:
    data_load_state = st.text('Loading data...')
    data = load_data(uploaded_file=uploaded_file)
    # Notify the reader that the data was successfully loaded.
    data_load_state.text("Done!")
    
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    row_start = st.text_input("Row Start", value='')
    row_end = st.text_input("Row End", value='')
    filter_columns = st.text_input("Filter Columns (comma-separated)", value='').split(',')
    data = {
        'row_start': row_start,
        'row_end': row_end,
        'filter_columns': [x.strip() for x in filter_columns if x.strip() != ''],
    }
    # data['upload_file'] = file



    if st.button('Filter Dataframe'):
      try:
          files = {"upload_file": (uploaded_file.name, uploaded_file.getvalue(), "multipart/form-data")}
          
          with requests.post(FILTER_URL, files=files, data=data,stream=True) as r:
              if r.status_code == 200:
                  file_name = ''
                  if "Content-Disposition" in r.headers.keys():
                      file_name = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0].replace('"', '')
                  else:
                      file_name = FILTER_URL.split("/")[-1]
                  
                  st.text('Data transposed! Click below button to download.')
                  st.download_button('Download CSV', data=r.content, file_name=file_name, mime='text/csv')
              else:
                  st.error(r.text)
      except RequestException as e:
          st.error(e)
