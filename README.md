# DICOM Dashboard

## Introduction
If you've ever wanted to visualize a DICOM image quickly, analyze the intensity histogram, view the effects on each using filters, and view the DICOM metadata then the DICOM Dashboard is for you! 

Upload a Pydicom-compliant DICOM image to the web application and instantly review the image, filtering options, intensity histograms, and metadata!

https://github.com/aziz66710/dicom_dashboard/assets/65475783/17d81403-10a7-4ae8-8090-bc4d40e97267


## Libraries and Skills Used
- Streamlit - Python library that makes it easy to develop custom data web applications. 
- Pydicom - Python library that allows for read and write of DICOM images
- Matplotlib - Python library that was used to generate the histogram plot
- Numpy - Python library used to manipulate pixel data for image
- Pandas - Python library used to generate the DICOM metadata table
- OpenCV - Python library used to create the filtering that is performed on the images

## Dataset
The dataset can be found at the following link: [Sample DICOM Images](https://www.rubomedical.com/dicom_files/)

## Method
Below describes the method and usage of the application. 

### Installation

1. Install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) so you can clone the repository
2. Clone the dicom-dashboard repository to any directory of your choosing
```bash
git clone https://github.com/aziz66710/dicom_dashboard.git
```
3. Use the package manager [anaconda](https://docs.anaconda.com/free/anaconda/install/index.html) to install anaconda.

4. After installing Anaconda, open **Anaconda Prompt** or any terminal of your choosing and run the following command to create and activate the environment. 
```bash
conda env create -f environment.yml
conda activate dicom_dashboard
```
5. Now you can launch the application. Run the following command to launch the streamlit application.
```bash
streamlit run run_dicom_dashboard.py
```
6. The application will open on your browser at http://localhost:8501/

### Usage

1. Upload any DICOM-compliant image. 
- **NOTE:** The assumption is that the DICOM image contains the following DICOM metadata: Patient Name, Patient Age, Patient Sex, Patient Birth Date, Referring Physician Name, Study Date.
2. Select any of the filtering options provided via the radio buttons and observe the impact it has on the image uploaded
3. Observe the generated histogram based on the filtering option selected in step 2. The histogram and its slider values adjusts according to the filter. 


## Future Work and Improvements
- Add caching to speed up performance of the web app
- Save figure to disk option
- Add different filtering options 
- Add entire DICOM metadata table and allow values to be edited


