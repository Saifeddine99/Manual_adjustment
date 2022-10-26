import streamlit as st
from PIL import Image
import numpy as np
import os

def colors(img):
    jadwel = np.array(img).astype(int)
    flat1 = np.reshape(jadwel[:, :8], (-1, 3))
    flat2 = np.reshape(jadwel[:, -8:], (-1, 3))
    flat3 = np.reshape(jadwel[:8, 8:-8], (-1, 3))
    flat4 = np.reshape(jadwel[-8:, 8:-8], (-1, 3))

    flatten_image = np.concatenate((flat1, flat2, flat3, flat4))

    moy = [int(np.mean(k)) for k in flatten_image]
    mean1 = np.array(moy).astype(int)
    k = np.bincount(mean1).argmax()
    color_index = np.where(moy == k)[0][0]
    return tuple(flatten_image[color_index].astype(int))


st.set_page_config(page_title="Manual deskew adjustment", page_icon=":scroll:", layout="centered")
st.markdown("<h1 style='text-align: center; color: green;'>Manual text deskew angle adjustment </h1>", unsafe_allow_html = True)
st.write('''
### You can use this Web application to manually determine the deskew angle of a text in a document
''')

st.sidebar.markdown("<h1 style='text-align: left; color: red;'>Deskew angle: </h1>", unsafe_allow_html = True)
chosen_angle = st.sidebar.slider("Choose the angle:", -10.0, 10.0, 0.0, 0.1)

st.markdown("<h1 style='text-align: center; color: brown;'>Please enter your saving directory : </h1>", unsafe_allow_html = True)

direction = st.text_input("Enter your directory here")

st.write('''
---
''')
object_image = st.file_uploader("Upload an image...", type=['png', 'jpg', 'webp', 'jpeg'])

real_image = Image.open(object_image)
real_image = real_image.convert('RGB')

original_size = real_image.size

img = real_image.rotate(-chosen_angle, expand=1, fillcolor=colors(real_image))
img = img.resize(original_size)

img_array = np.array(img)
for i in range(0, len(img_array), 20):
    img_array[i:i+2] = (0, 0, 255)

img1 = Image.fromarray(img_array)
img1.resize(original_size)

st.sidebar.write("# Original image :arrow_down: :")
st.sidebar.image(real_image)

with st.container():
    adjusted_image, tbs = st.columns(2)
    with adjusted_image:
        st.markdown("<h1 style='text-align: center; color: black;'>Adjusted image  </h1>",
                    unsafe_allow_html=True)

    with tbs:
        st.markdown("<h1 style='text-align: center; color: black;'>Image to be saved  </h1>",
                    unsafe_allow_html=True)

with st.container():
    adjusted_image1, tbs1 = st.columns(2)
    with adjusted_image1:
        st.image(img1)
    with tbs1:
        st.image(img)

st.write('''
---
### If you are satisfied with this adjustment click on the button "satisfied" below :arrow_down: else continue your process :repeat:
''')
st.write('''
---
''')
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('')
    with col2:
        submit_yes = st.button("Satisfied ✔")
    with col3:
        st.write('')

new_object_image = "0rot_"+object_image.name
full_path = os.path.join(direction, new_object_image)

placeholder = st.empty()
if submit_yes:
    img.save(full_path)
    placeholder.markdown("<h1 style='text-align: center; grey: black;'>Image saved ✅ </h1>",
                unsafe_allow_html=True)
    submit_yes = False
else:
    placeholder.markdown("<h1 style='text-align: center; grey: black;'>No image saved ✖ </h1>",
                         unsafe_allow_html=True)
