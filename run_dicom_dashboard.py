import streamlit as st
from io import StringIO
import pydicom
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import functools
from dataclasses import dataclass
import altair as alt 
import matplotlib
#import cv2


def check_session_state():
    #if "col1" and "col2" not in st.session_state:
        st.session_state.col1, st.session_state.col2 = st.columns(2)

def run_workflow() -> None:
    check_session_state()
    upload_button()
    if st.session_state.uploaded_file is not None:
        display_dicom_image()
        display_dicom_metadata()
        side_by_side()
        display_image_histogram()

def upload_button():
    #if "uploaded_file" not in st.session_state: 
    st.session_state.uploaded_file = st.file_uploader('UPLOAD DICOM')
    return st.session_state.uploaded_file
    
#@st.cache_data
def display_dicom_image() -> None:
    st.session_state.ds = pydicom.dcmread(st.session_state.uploaded_file)
    #reshape to smaller
    if "ds_array" not in st.session_state:
        st.session_state.ds_array = st.session_state.ds.pixel_array
    st.session_state.xmax = float(np.max(st.session_state.ds_array))
    st.session_state.ymax = float(np.size(st.session_state.ds_array))
    return st.session_state.ds, st.session_state.ds_array

#@st.cache_data
def display_dicom_metadata() -> None:
    common_metadata: dict = {
        'DICOM Tag': ['Patient Name',
                    'Patient Age',
                    'Patient Sex',
                    'Patient Birth Date',
                    'Referring Physician Name', 
                    'Study Date'],
        'Value': [str(st.session_state.ds.PatientName),
                st.session_state.ds.PatientAge,
                st.session_state.ds.PatientSex,
                st.session_state.ds.PatientBirthDate,
                st.session_state.ds.ReferringPhysicianName,
                st.session_state.ds.StudyDate 
        ]

    }
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(common_metadata)
    st.session_state.df = st.session_state.df.replace(r'^\s*$', np.nan, regex=True)
    return st.session_state.df

def side_by_side() -> None:
    st.session_state.col1.header("Image")
    st.session_state.col1.image(st.session_state.ds_array, caption="DICOM Images", use_column_width=True)
    st.session_state.col2.header("DICOM Tags")
    st.session_state.col2.table(st.session_state.df)

#@st.cache_data(hash_funcs={matplotlib.figure.Figure: lambda _: None})
def display_image_histogram() -> None:
    # if "col3" and "col4" not in st.session_state:
    #     st.session_state.col3, st.session_state.col4 = st.columns(2)
    if "xlim1" and "xlim2" and "ylim1" and "xlim2"  not in st.session_state:
        st.session_state.xlim1, st.session_state.xlim2, st.session_state.ylim1, st.session_state.ylim2, st.session_state.xmax, st.session_state.ymax = (0.0,)*6
    col3, col4 = st.columns(2)
    fig = plot_fig(st.session_state.ds_array, col4)
    col3.pyplot(fig)

    return fig

#@st.cache_data(#experimental_allow_widgets=True,
#                   hash_funcs={matplotlib.figure.Figure: lambda _: None})
def plot_fig(array,col):
    fig, ax = plt.subplots()
    #counts, bins = np.histogram(array.flatten())
    counts, bins, patches = ax.hist(array.flatten())
    #slider_limits(counts, bins)
    xlim1, xlim2, ylim1, ylim2 = slider_values(col,counts,bins)
    plt.xlim([xlim1,xlim2])
    plt.ylim([ylim1,ylim2])
    plt.title('Image Intesity Histogram')
    plt.xlabel('Intensities')
    plt.ylabel('Count')
    return fig

#@st.cache_data
def slider_limits(counts, bins):
    st.session_state.xlim1, st.session_state.xlim2, st.session_state.ylim1, st.session_state.ylim2 = slider_values(counts, bins)


#@st.cache_data(experimental_allow_widgets=True)
def slider_values(col, counts, bins):
    xlim1, xlim2 = col.slider(
        'Select a x range of values',
        0.0, np.max(bins), (0.0,np.max(bins)))
    ylim1, ylim2 = col.slider(
        'Select a y range of values',
        0.0, np.max(counts), (0.0,np.max(counts)))
    return xlim1, xlim2, ylim1, ylim2
