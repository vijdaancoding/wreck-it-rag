"""
Author: Ali Vijdaan
Description: streamlit GUI for no-code pre-processing with UNSTRUCTURED.IO and LLMs
"""

import tempfile
import os
import base64
import html
import streamlit as st
import PIL.Image

from extraction_ocr import ocr_extraction, image_element_items, text_element_items, table_element_items, convert_to_json
from vision_llm_summarizer import get_response
from converter import html_to_json_table
from prompt import prompt

#sanitize elements for HTML
def sanitize_html(content):
    return html.escape(content)


#Create a temporary directory to store uplaoded documents
def create_temp_dir(uploaded_file):
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)

    with open(temp_file_path, 'wb') as temp_file:
        temp_file.write(uploaded_file.read())

    output_dir = 'images'

    return temp_file_path, output_dir


# Main function to perform OCR and text extraction
def run_ocr(file):

    if file is None:
        st.write("No file found")
        return None, None

    if file.type != 'application/pdf':
        st.write("No PDF file found")
        return None, None

    temp_file_path, output_dir = create_temp_dir(file)
    raw_elements = ocr_extraction(file_name=temp_file_path, output_dir=output_dir)

    return raw_elements, temp_file_path


# Return file in base64
def get_base64_of_file(file_path):
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode()


# Doc Viewer on streamlit app
def show_uploaded_docs(uploaded_file, temp_file_path):

    if uploaded_file is None:
        st.write("No file found")
        return

    st.subheader("Doc Viewer")

    if uploaded_file.type == 'application/pdf':
        display_pdf(temp_file_path)


# Iframe display of PDFs
def display_pdf(file_path):
    pdf_base64 = get_base64_of_file(file_path)
    pdf_display = f"""<iframe src="data:application/pdf;base64,{pdf_base64}"
                    height="500" width="100%" type="application/pdf">
                    </iframe>"""
    st.markdown(pdf_display, unsafe_allow_html=True)


def filter_extracted_text(raw_elements, llm_summary):

    # Add custom CSS to style the container
    st.markdown(
        """
        <style>
        .scrollable-container {
            height: 500px;
            width: 100%;
            overflow-y: scroll;
            border: 1px solid #ccc;
            padding: 10px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Differentiate Between OCR and LLM
    def generate_element_html(element, is_summary):
        sanitized_element = sanitize_html(str(element))
        if type(element) in image_element_items:
            summary_text = (element.metadata.summary
                            if is_summary and hasattr(element, 'metadata')
                            else sanitized_element)
            return f"""<p style= "text-align:center;">
                ----------------IMAGE / TABLE -------------------- <br>
                {summary_text} <br>
                ----------------------------------------------
                </p><br>"""

        elif type(element) in table_element_items:
            json_table = html_to_json_table(element.metadata.text_as_html)
            element.metadata.json_table = json_table
            return f"<p>{element.metadata.json_table}</p><br>"
        return f"<p>{sanitized_element}</p><br>"

    #Create a container with the custom class
    container_html = '<div class="scrollable-container">'
    container_html += ''.join(generate_element_html(ele, llm_summary) for ele in raw_elements)
    container_html += '</div>'

    st.markdown(container_html, unsafe_allow_html=True)


def add_summary(image_summary, element):
    element.metadata.summary = image_summary
    return element

def get_image_summary(raw_elements):

    for element in raw_elements:
        if type(element) in image_element_items:

            image_path = element.metadata.image_path

            if os.path.exists(image_path):

                image = PIL.Image.open(image_path)
                image_summary = get_response(prompt=prompt, image=image)

                print("\n-----------------------IMAGE SUMMARY--------------------------")
                print(image_summary)

                element = add_summary(image_summary=image_summary.text, element=element)
                print("---------------------------------------")
                print(element)

            else:
                image_summary = "Image does not exist"
                element = add_summary(image_summary=image_summary, element=element)
                print("---------------------------------------")
                print(element)

    for element in raw_elements:
        print(element)

    return raw_elements

def edit_json(llm_elements):
    for i, element in enumerate(llm_elements):
        if type(element) in text_element_items:
            edited_text = st.text_area(label="-",
                                       value=element.text,
                                       label_visibility="collapsed",
                                       key=i)
            element.text = edited_text
        elif type(element) in image_element_items:
            edited_image = st.text_area(label="-",
                                        value=element.metadata.summary,
                                        label_visibility="collapsed",
                                        key=i)
            element.metadata.summary = edited_image
        elif type(element) in table_element_items:
            edited_table = st.text_area(label="-",
                                        value=element.metadata.json_table,
                                        label_visibility="collapsed",
                                        key=i)
            element.metadata.json_table = edited_table

def main():
    st.set_page_config(page_title="Doc Extractor", layout="wide")

    with st.container():
        st.title("Document Data Extractor")
        st.write("The goal is to create an ETL pipeline that can load documents and preprocess them to make them RAG Ready!")

    uploaded_file = st.file_uploader("Choose a file", type=["pdf"])

    # defining session state for llm
    if 'llm' not in st.session_state:
        st.session_state.llm = False    #default llm state is set to FALSE
    if 'run_ocr' not in st.session_state:
        st.session_state.run_ocr = False    #default OCR state is set to FALSE
    if 'json' not in st.session_state:
        st.session_state.json = False   #default JSON state is set to FALSE

    if uploaded_file is not None:
        if not st.session_state.run_ocr:    #if OCR doesnt exsit

            raw_elements, temp_file_path = run_ocr(uploaded_file)

            # defining session state for ocr run
            st.session_state['ocr_run_raw_ele'] = raw_elements
            st.session_state['ocr_run_temp_file'] = temp_file_path
            st.session_state['ocr_run_uploaded_file'] = uploaded_file

            st.session_state.run_ocr = True #session state for OCR set to TRUE

        with st.container():
            left_column, right_column = st.columns(2)

            with left_column:
                with st.expander("Show original document"):
                    show_uploaded_docs(st.session_state['ocr_run_uploaded_file'], st.session_state['ocr_run_temp_file'])

            with right_column:
                with st.expander("Show Extracted Text"):
                    st.subheader("Extracted Text")
                    filter_extracted_text(st.session_state['ocr_run_raw_ele'], llm_summary=False)

        summarizer = st.button("Show LLM Summary")
        if summarizer:
            st.session_state.llm = True #llm state set to TRUE when button pressed

        if st.session_state.llm:
            with st.container():
                with st.expander("Show Image Summaries via LLM"):

                    if 'llm_elements' not in st.session_state:
                        st.session_state.llm_elements = get_image_summary(st.session_state['ocr_run_raw_ele'])

                    filter_extracted_text(st.session_state.llm_elements, llm_summary=True)

        if st.session_state.llm:
            with st.container():
                st.subheader("Edit Extracted Text")
                first_col, second_col, third_col = st.columns(3)

            with first_col:
                with st.expander("OCR Extracted Text"):
                    filter_extracted_text(st.session_state['ocr_run_raw_ele'], llm_summary=False)

            with second_col:
                with st.expander("LLM Extracted Image Summaries"):
                    filter_extracted_text(st.session_state.llm_elements, llm_summary=True)

            with third_col:
                with st.expander("Edit JSON"):
                    with st.container(height=500):
                        edit_json(st.session_state.llm_elements)


        json_converter = st.button("Convert to JSON")
        if json_converter:
            st.session_state.json = True #json state set to TRUE

        if st.session_state.json:
            convert_to_json(st.session_state.llm_elements, filename='output.json')


if __name__ == "__main__":
    main()
