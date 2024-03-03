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

c1 = st.empty()
c2 = st.empty()
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

def run_workflow() -> None:
    welcome_message()
    uploaded_file = c2.file_uploader('UPLOAD DICOM')
    if uploaded_file is not None:
        ds, ds_array = display_dicom_image(uploaded_file)
        df = display_dicom_metadata(ds)
        side_by_side(ds_array, df)
        display_image_histogram(ds_array)

def welcome_message():
    c1.write("""
# DICOM Dashboard

Upload your DICOM data file using the Upload button below and visualize your image!
""")

def upload_button():
    uploaded_file = st.file_uploader('UPLOAD DICOM')
    return uploaded_file
    
def display_dicom_image(uploaded_file) -> None:
    ds = pydicom.dcmread(uploaded_file)
    ds_array = ds.pixel_array
    xmax = float(np.max(ds_array))
    ymax = float(np.size(ds_array))
    return ds, ds_array

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
    return df

def side_by_side(ds_array, df) -> None:
    col1.header("Image")
    col1.image(ds_array, caption="DICOM Images", use_column_width=True)
    col2.header("DICOM Tags")
    col2.table(df)

def display_image_histogram(ds_array) -> None:
    fig = plot_fig(ds_array, col4)
    col3.pyplot(fig)

    return fig

def plot_fig(array,col):
    fig, ax = plt.subplots()
    counts, bins, patches = ax.hist(array.flatten())
    xlim1, xlim2, ylim1, ylim2 = slider_values(col,counts,bins)
    plt.xlim([xlim1,xlim2])
    plt.ylim([ylim1,ylim2])
    plt.title('Image Intesity Histogram')
    plt.xlabel('Intensities')
    plt.ylabel('Count')
    return fig

def slider_values(col, counts, bins):
    xlim1, xlim2 = col.slider(
        'Select a x range of values',
        0.0, np.max(bins), (0.0,np.max(bins)))
    ylim1, ylim2 = col.slider(
        'Select a y range of values',
        0.0, np.max(counts), (0.0,np.max(counts)))
    return xlim1, xlim2, ylim1, ylim2

if __name__ == "__main__":
    run_workflow()
