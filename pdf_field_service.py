# pdf_field_service.py
import boto3
import logging
from pypdf import PdfReader

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize the S3 client
s3 = boto3.client('s3')


def discover_pdf_fields(pdf_path):
    """
    Discover form fields in a given PDF.

    :param pdf_path: The local path to the PDF file
    :return: A dictionary of discovered form fields
    """
    logger.info(f"Discovering fields in PDF at path: {pdf_path}")

    pdf_reader = PdfReader(pdf_path)
    fields = {}

    for page in pdf_reader.pages:
        if '/Annots' in page:
            for annotation in page['/Annots']:
                field = annotation.get_object()
                field_name = field.get('/T')
                if field_name:
                    field_name = field_name.strip('()')
                    fields[field_name] = ""

    logger.info(f"Discovered fields: {fields}")
    return fields


def download_pdf_from_s3(bucket_name, s3_key, local_path):
    """
    Download a PDF template from S3.

    :param bucket_name: The name of the S3 bucket
    :param s3_key: The S3 key (path) to the PDF template
    :param local_path: The local file path to store the downloaded PDF
    """
    try:
        logger.info(f"Downloading PDF from S3 bucket: {bucket_name}, key: {s3_key}")
        s3.download_file(bucket_name, s3_key, local_path)
        logger.info(f"Downloaded PDF to local path: {local_path}")
    except Exception as e:
        logger.error(f"Error downloading PDF from S3: {str(e)}", exc_info=True)
        raise e
