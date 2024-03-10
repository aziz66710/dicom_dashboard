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
import cv2

container_1 = st.empty()
container_2 = st.empty()
column_1, column_2 = st.columns(2)
column_3, column_4 = st.columns(2)

def run_workflow() -> None:
    welcome_message()
    uploaded_file = container_2.file_uploader('UPLOAD DICOM')
    if uploaded_file is not None:
        ds, ds_array = load_dicom_image(uploaded_file)
        ds_array = image_processing_techniques(ds_array)
        side_by_side(ds_array)
        display_image_histogram(ds_array)
        df = display_dicom_metadata(ds)

def welcome_message():
    container_1.write("""
# DICOM Dashboard

Upload your DICOM data file using the Upload button below and visualize your image!
""")

def upload_button():
    uploaded_file = st.file_uploader('UPLOAD DICOM')
    return uploaded_file
    
def load_dicom_image(uploaded_file) -> None:
    ds = pydicom.dcmread(uploaded_file)
    ds_array = ds.pixel_array
    return ds, ds_array

def image_processing_techniques(ds_array):
    processing_techniques = ["Original",
                            "Mean Filter", 
                            "Median Filter", 
                            "Gaussian Smoothing"
                            ]
    column_2.header("Image Filtering")
    filter_tech = column_2.radio("Select an Image Filter",
                processing_techniques,
                captions = ["Original unfiltered image",
                            "Noise Reduction using mean of neighborhood",
                            "Noise Reduction using median of neighborhood", 
                            "Noise Reduction using convolution with a Gaussian smoothing kernel"])
    if filter_tech == 'Original':
        return ds_array
    elif filter_tech == 'Mean Filter':
        window=(5, 5)
        return cv2.blur(ds_array, window)
    elif filter_tech == 'Median Filter':
        window=3
        return cv2.medianBlur(ds_array, window)
    elif filter_tech == 'Gaussian Smoothing':
        window=(5, 5)
        return cv2.GaussianBlur(ds_array, window, 0)
    else:
        return None

def side_by_side(ds_array) -> None:
    column_1.header("Image")
    column_1.image(ds_array, caption="DICOM Images", use_column_width=True)
    
def display_image_histogram(ds_array) -> None:
    fig = plot_fig(ds_array, column_4)
    column_3.header("Intensity Histogram")
    column_3.pyplot(fig)

    return fig

def display_dicom_metadata(ds) -> None:
    common_metadata: dict = {
        'DICOM Tag': ['Patient Name',
                    'Patient Age',
                    'Patient Sex',
                    'Patient Birth Date',
                    'Referring Physician Name', 
                    'Study Date'],
        'Value': [str(ds.PatientName),
                ds.PatientAge,
                ds.PatientSex,
                ds.PatientBirthDate,
                ds.ReferringPhysicianName,
                ds.StudyDate 
        ]

    }
    df = pd.DataFrame(common_metadata)
    df = df.replace(r'^\s*$', np.nan, regex=True)
    st.header("DICOM Metadata")
    st.table(df)

    return df

def plot_fig(array,col):
    fig, ax = plt.subplots()
    counts, bins, patches = ax.hist(array.flatten())
    xlim1, xlim2, ylim1, ylim2 = slider_values(col,counts,bins)
    plt.xlim([xlim1,xlim2])
    plt.ylim([ylim1,ylim2])
    plt.xlabel('Intensities')
    plt.ylabel('Count')
    return fig

def slider_values(column, counts, bins):
    column.header("Bin and Count Range")
    xlim1, xlim2 = column.slider(
        'Select a x range of values',
        0.0, np.max(bins), (0.0,np.max(bins)))
    ylim1, ylim2 = column.slider(
        'Select a y range of values',
        0.0, np.max(counts), (0.0,np.max(counts)))
    return xlim1, xlim2, ylim1, ylim2    

if __name__ == "__main__":
    run_workflow()
