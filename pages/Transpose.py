import streamlit as st
import pandas as pd
import numpy as np
import re
import requests
from requests.exceptions import RequestException


# Define Streamlit app
st.title("Transpose DataFrame")

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


# Present an uploader for the user to upload a file of type csv, tsv or xlsx.
uploaded_file = st.file_uploader(label="Choose a file", type=['tsv', 'csv', 'json', 'xlsx'])
st.set_option('deprecation.showfileUploaderEncoding', False)  # Enabling the automatic file decoder.

if uploaded_file is not None:
    
    data_load_state = st.text('Loading data...')
    data = load_data(uploaded_file=uploaded_file)
    # Notify the reader that the data was successfully loaded.
    data_load_state.text("Done!")
    
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    if st.button('Get Transpose'):
        try:
            transpose_url = "http://127.0.0.1:8000/autoworkflow/transpose-dataframe"
            files = {"upload_file": (uploaded_file.name, uploaded_file.getvalue(), "multipart/form-data")}
            
            with requests.post(transpose_url, files=files, stream=True) as r:
                if r.status_code == 200:
                    file_name = ''
                    if "Content-Disposition" in r.headers.keys():
                        file_name = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0].replace('"', '')
                    else:
                        file_name = transpose_url.split("/")[-1]
                    
                    st.text('Data transposed! Click below button to download.')
                    st.download_button('Download CSV', data=r.content, file_name=file_name, mime='text/csv')
                else:
                    st.error(r.text)

        except RequestException as e:
            st.error(e)
