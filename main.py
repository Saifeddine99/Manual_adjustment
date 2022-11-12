import streamlit as st
from PIL import Image
import numpy as np

import os

import tkinter as tk
from tkinter import filedialog

import requests
from streamlit_lottie import st_lottie
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

st.markdown("<h1 style='text-align: center; color: #0d325c;'>Manual text deskew angle adjustment </h1>", unsafe_allow_html = True)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_jt1ky9pg.json")

with st.container():
    text, anim = st.columns((2, 1))
    with text:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write('''
        ### You can use this Web application to manually determine the deskew angle of a text in a document
        ''')
    with anim:
        st_lottie(lottie_coding, height=300, key="coding")

st.write('''
---
''')

object_image = st.file_uploader("Upload an image...", type=['png', 'jpg', 'webp', 'jpeg'])

placeholder0 = st.empty()
if(object_image!=None):
    st.sidebar.markdown("<h1 style='text-align: left; color: red;'>Deskew angle: </h1>", unsafe_allow_html=True)
    chosen_angle = st.sidebar.slider("Choose the angle:", -10.0, 10.0, 0.0, 0.1)
    real_image = Image.open(object_image)
    real_image = real_image.convert('RGB')
    original_size = real_image.size

    img = real_image.rotate(-chosen_angle, expand=1, fillcolor=colors(real_image))

    optimal_size = (1000, 1500)
    img = img.resize(optimal_size)

    img_array = np.array(img)
    for i in range(0, len(img_array), 22):
        img_array[i:i+3] = (0, 100, 250)

    img1 = Image.fromarray(img_array)
    img1.resize(original_size)

    st.sidebar.write("# Original image :arrow_down: :")
    st.sidebar.image(real_image)

    with st.container():
        adjusted_image, tbs = st.columns(2)
        with adjusted_image:
            st.markdown("<h1 style='text-align: center; color: #387348;'>Adjusted image  </h1>",
                        unsafe_allow_html=True)

        with tbs:
            st.markdown("<h1 style='text-align: center; color: #387348;'>Image to be saved  </h1>",
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

    placeholder = st.empty()
    placeholder2 = st.empty()
    if submit_yes:

        # Set up tkinter
        root = tk.Tk()
        root.withdraw()

        # Make folder picker dialog appear on top of other windows
        root.wm_attributes('-topmost', 1)
        dirname = placeholder2.text_input('Here is the directory you chose:', filedialog.askdirectory(master=root))

        if(dirname!=''):
            if(chosen_angle<0):
                rot_angle = str(chosen_angle)
            else:
                rot_angle="+"+str(chosen_angle)

            new_object_image = rot_angle +object_image.name
            full_path = os.path.join(dirname, new_object_image)
            img = img.resize(original_size)
            img.save(full_path)

            placeholder.markdown("<h1 style='text-align: center; color: #3ca057;'>Image saved ✅✅ </h1>",
                                 unsafe_allow_html=True)
            lottie_saving = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_ifcdlulh.json")

            with st.container():
                l0, m0, r0 = st.columns((1, 2, 1))
                with l0:
                    st.write('')
                with m0:
                    st_lottie(lottie_saving, height=300)
                with r0:
                    st.write('')

            submit_yes = False
        else:
            placeholder2.empty()
            placeholder.write('''
            ### Image not saved 
            ### To save, click on the 'satisfied' button and choose a directory !!
            ''')

            lottie_error = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_yw3nyrsv.json")

            with st.container():
                l2, m2, r2 = st.columns((1, 2, 1))
                with l2:
                    st.write('')
                with m2:
                    st_lottie(lottie_error, height=300)
                with r2:
                    st.write('')
    else:

        placeholder.markdown("<h1 style='text-align: center; color: #e7372a;'>No image saved  </h1>",
                             unsafe_allow_html=True)
        lottie_not_saved = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_o75swrf7.json")

        with st.container():
            l1, m1, r1 = st.columns((1, 2, 1))
            with l1:
                st.write('')
            with m1:
                st_lottie(lottie_not_saved, height=300)
            with r1:
                st.write('')
else:

    placeholder0.markdown("<h1 style='text-align: center; color:#f25126;'>Please enter an image ! </h1>",
                          unsafe_allow_html=True)

    with st.container():
        l, m, r = st.columns((1, 2, 1))
        with l:
            st.write('')
        with m:
            lottie_image = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_lafs08kHr5.json")
            st_lottie(lottie_image, height=300)
        with r:
            st.write('')
