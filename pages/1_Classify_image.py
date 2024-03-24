import streamlit as st
import keras
import numpy as np
import cv2
from collections import Counter
from tensorflow.keras.utils import load_img

@st.cache_resource
def load_models():
	vgg_best_model = keras.models.load_model('models/vgg_16_-saved-model-39-acc-0.99.hdf5')
	resnet_best_model = keras.models.load_model('models/resnet50-saved-model-16-val_acc-0.99.hdf5')
	inception_best_model = keras.models.load_model('models/inceptionv3_-saved-model-12-val_accuracy-0.97.hdf5')
	benchmark_model = keras.models.load_model('models/bench_mark_-model-12-0.96.hdf5')
	return vgg_best_model,resnet_best_model,inception_best_model,benchmark_model


vgg_best_model,resnet_best_model,inception_best_model,benchmark_model=load_models()

classes={0: 'Baby & Toddler Dresses', 1: 'Belts', 2: 'Coats & Jackets', 3: 'Handbags', 4: 'Lotion & Moisturizer', 5: 'Pants', 6: 'Shirts & Tops', 7: 'Shoes', 8: 'Tea & Infusions', 9: 'Vanity Benches'}
st.subheader('Please upload any image belonging to below category')
st.write([*classes.values()])
def mode(my_list):
	ct = Counter(my_list)
	max_value = max(ct.values())
	return ([key for key, value in ct.items() if value == max_value])



image_file = st.file_uploader('Upload an image', type=['jpg', 'jpeg', 'png','webp'],key='classify')
if image_file is not None:
	st.image(image_file)



	true_value = []
	combined_model_pred =""
	vgg_pred = ""
	resnet_pred ="" 
	inception_pred ='' 
	benchmark_model_pred ='' 
	file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
	img = cv2.resize(cv2.imdecode(file_bytes, 1),(150,150))
	img_normalized = img/255
	#vgg
	vgg16_image_prediction = np.argmax(vgg_best_model.predict(np.array([img_normalized])))

	#resnet50
	resnet_50_image_prediction = np.argmax(resnet_best_model.predict(np.array([img_normalized])))

	#Inception
	inception_image_prediction = np.argmax(inception_best_model.predict(np.array([img_normalized])))

	#benchmark
	benchmark_model_prediction = np.argmax(benchmark_model.predict(np.array([img_normalized])))

	#giving resnet high priority if they all predict something different
	image_prediction = mode([vgg16_image_prediction , resnet_50_image_prediction,inception_image_prediction]) #mode weight to vgg                                  
	combined_model_pred=image_prediction
	print(combined_model_pred,inception_image_prediction,mode([8,7,8]))
	
	st.markdown(f'Resnet 50 Predcition: **{classes[resnet_50_image_prediction]}**')
	st.markdown(f'VGG16 Predcition: **{classes[vgg16_image_prediction]}**')
	st.markdown(f'Inception Prediction: **{classes[inception_image_prediction]}**')
	st.info(f"Final prediction: **{classes[combined_model_pred[0]]}**")
