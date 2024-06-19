import warnings
warnings.filterwarnings('ignore')

from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError
from unstructured.staging.base import dict_to_elements
from IPython.display import Image
from Utils import Utils

import os
from io import StringIO
from lxml import etree

# Initialize utilities and UnstructuredClient
utils = Utils()
DLAI_API_KEY = utils.get_dlai_api_key()
DLAI_API_URL = utils.get_dlai_url()

s = UnstructuredClient(
    api_key_auth=DLAI_API_KEY,
    server_url=DLAI_API_URL,
)

# Define the path to the PDF file
filename = r"C:\Users\Ashutosh\Desktop\using_elser\vectorstore_test.pdf"

# Ensure the file exists before proceeding
if not os.path.exists(filename):
    raise FileNotFoundError(f"The file {filename} does not exist.")

# Read the file content
with open(filename, "rb") as f:
    file_content = f.read()

# Create the Files object
files = shared.Files(
    content=file_content,
    file_name=filename,
)

# Define the partition parameters
req = shared.PartitionParameters(
    files=files,
    strategy="hi_res",
    hi_res_model_name="yolox",
    skip_infer_table_types=[],
    pdf_infer_table_structure=True,
)

# Try to partition the document and handle potential errors
try:
    resp = s.general.partition(req)
    elements = dict_to_elements(resp.elements)
except SDKError as e:
    print(f"An error occurred while partitioning the document: {e}")
    elements = []

# Extract tables from the elements
tables = [el for el in elements if el.category == "Table"]

# Check if any tables were found
if not tables:
    raise ValueError("No tables found in the document.")

# Extract and print the first table's HTML
table_html = tables[0].metadata.text_as_html

# Parse the HTML string
parser = etree.XMLParser(remove_blank_text=True)
file_obj = StringIO(table_html)
tree = etree.parse(file_obj, parser)

# Print the formatted HTML
formatted_html = etree.tostring(tree, pretty_print=True).decode()
print(formatted_html)
