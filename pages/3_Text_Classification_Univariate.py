import streamlit as st
import numpy as np
import pickle
import json
import pandas as pd


st.title('Text Classifer - Taxanomy Predictor')

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


def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


pickle_in = open("univariate-text-classifier/univariate_model.pkl","rb")
model=pickle.load(pickle_in)


# Testing phase
tf1 = pickle.load(open("univariate-text-classifier/tfidf1.pkl", 'rb'))


with open('univariate-text-classifier/id_to_category.txt') as f:
   id_to_category = json.load(f)



prediction_type = st.radio(
    "Select Preodction type",
    ('Manual', "Bulk"))


if prediction_type =="Manual":
	description = st.text_area(label="Please enter description text to predict")

	if st.button('Predict Taxanomy'):
		features = tf1.transform([description])
		predictions=model.predict(features)
		preidcted_label=str(id_to_category[str(predictions[0])])
		print(preidcted_label)
		st.markdown("**The above text belongs to category:**")
		st.info(f"**{preidcted_label}**")

else:

	uploaded_file = st.file_uploader(label="Upload file to predict", type=['tsv', 'csv', 'json', 'xlsx'])

	# If file is uploaded, display options to filter the DataFrame
	if uploaded_file is not None:
		try:
			data=load_data(uploaded_file=uploaded_file)
		except Exception as e:
			st.error(f'Something went wrong-  {e}')
			st.stop()
		st.success('Data Loaded sucesfully!!')
		if st.checkbox('Show raw data'):
			st.subheader('Raw data')
			st.dataframe(data)
		columns=list(data.columns)
		columns.insert(0,'')
		column_option = st.selectbox(
		'Please choose a text column which needs to be used for prediction',
		(columns))

		if column_option is not None and column_option is not '':	
			descriptions=data[column_option].astype(str) 

			features = tf1.transform(descriptions)
			predictions=list(model.predict(features))

			# # # return {
			# # #     'prediction': prediction
			# # # }
			for index in range(0,len(predictions)):
				predictions[index]=str(id_to_category[str(predictions[index])])
			data['prediction']=predictions
			st.subheader('Prediction results:')
			st.dataframe(data)

			csv = convert_df(data)

			st.download_button(
			   "Download Output",
			   csv,
			   "Univariate-Output.csv",
			   "text/csv",
			   key='download-csv'
			)
