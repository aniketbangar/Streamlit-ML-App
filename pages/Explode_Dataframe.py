import streamlit as st
import requests
from io import BytesIO
import pandas as pd
from requests.exceptions import RequestException
import re
import json



# API endpoint URL
EXPLODE_URL = 'http://localhost:8000/autoworkflow/explode-dataframe'


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
st.title("Explode DataFrame")

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

	explode_columns = st.text_input("Index Coulumns (comma-separated)", value='').split(',')
	

  

	if st.button('Explode Dataframe'):
	
	   
		data = {
		'explode_columns': [x.strip() for x in explode_columns if x.strip() != ''],
		}
		
		
		try:
			files = {"upload_file": (uploaded_file.name, uploaded_file.getvalue(), "multipart/form-data")}
			with requests.post(EXPLODE_URL, files=files, data=data,stream=True) as r:
				if r.status_code == 200:
					file_name = ''
					if "Content-Disposition" in r.headers.keys():
						file_name = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0].replace('"', '')
					else:
						file_name = EXPLODE_URL.split("/")[-1]
						
					st.text('Data transposed! Click below button to download.')
					st.download_button('Download CSV', data=r.content, file_name=file_name, mime='text/csv')
				else:
				  	st.error(r.text)
		except RequestException as e:
			st.error(e)