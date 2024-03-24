import streamlit as st
import numpy as np
from DeepImageSearch import Load_Data,Search_Setup
# image_list = Load_Data().from_folder(['train-images'])

@st.cache_resource
def setup_engine():
	image_list = Load_Data().from_folder(['train-images'])

	search_engine=Search_Setup(image_list=image_list,model_name='convnext_small_384_in22ft1k',pretrained=True,image_count=5000)
	# Update metadata
	search_engine.get_image_metadata_file()
	return search_engine,image_list


# make any grid with a function
def make_grid(cols,rows):
	grid = [0]*cols
	for i in range(cols):
		with st.container():
			grid[i] = st.columns(rows)
	return grid

search_engine,image_list=setup_engine()
image_file = st.file_uploader('Upload an image', type=['jpg', 'jpeg', 'png','webp'],key='similarity')

if image_file is not None:
	col1, col2, col3 = st.columns(3)

	with col1:
		st.write('Uploaded Image: ')

	with col2:
		st.image(image_file,width=300)

	with col3:
		st.write(' ')
	
	st.subheader('Top Similar Images:')

	similar_images=search_engine.get_similar_images(image_path=image_file,number_of_images=6)
	# print(similar_images.values())
	similar_images=list(similar_images.values())
	grid_width=3
	groups=[]
	for i in range(0,len(similar_images),grid_width):
		groups.append(similar_images[i:i+grid_width])
	print(groups)
	columns=st.columns(grid_width)

	for group in groups:
		for i,image in enumerate(group):
			columns[i].image(image)
	st.write(similar_images)



	# for image_id in range(0,len(similar_images)):
	# 	columns[image_id].image(image_list[image_id])


