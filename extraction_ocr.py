"""
Author: Ali Vijdaan
Description: UNSTRUCTURED.IO functions
"""

import unstructured
import unstructured.documents
import unstructured.documents.elements
from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import elements_to_json


#Function for OCR Extraction from PDFs
def ocr_extraction(file_name, output_dir):
    raw_elements = partition_pdf(
        filename=file_name,
        strategy='hi_res',
        infer_table_structure=True,
        extract_images_in_pdf=True,
        extract_image_block_output_dir=output_dir
    )

    return raw_elements

#Filtering Text Elements
text_element_items = [unstructured.documents.elements.Text,
                      unstructured.documents.elements.NarrativeText,
                      unstructured.documents.elements.ListItem,
                      unstructured.documents.elements.Header,
                      unstructured.documents.elements.Footer,
                      unstructured.documents.elements.Title,
                      unstructured.documents.elements.CompositeElement]

image_element_items = [unstructured.documents.elements.Image]

table_element_items = [unstructured.documents.elements.Table,
                       unstructured.documents.elements.TableChunk]

def filter_text_elements(raw_elements: list) -> list:
    return [ele for ele in raw_elements if type(ele) in text_element_items]

def filter_image_elements(raw_elements: list) -> list:
    return [ele for ele in raw_elements if type(ele) in image_element_items]

def filter_table_elements(raw_elements: list) -> list:
    return [ele for ele in raw_elements if type(ele) in table_element_items]

def convert_to_json(elements, filename):
    elements_to_json(elements, filename=filename)




