# pdf_field_service.py
import boto3
import logging
from pypdf import PdfReader
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize the S3 client
s3 = boto3.client('s3')


def download_pdf(bucket_or_path, s3_key=None, local_path=None):
    """
    Download a PDF template from S3 or use the local path if provided.

    :param bucket_or_path: The name of the S3 bucket or local file path
    :param s3_key: The S3 key (path) to the PDF template if using S3
    :param local_path: The local file path to store the downloaded PDF if using S3
    :return: The path to the PDF file (local or downloaded)
    """
    if bucket_or_path.startswith("s3://"):
        # Extract bucket name and key from the S3 path
        bucket_name = bucket_or_path.split('/')[2]
        s3_key = '/'.join(bucket_or_path.split('/')[3:])

        if not local_path:
            local_path = f'/tmp/{os.path.basename(s3_key)}'

        try:
            logger.info(f"Downloading PDF from S3 bucket: {bucket_name}, key: {s3_key}")
            s3.download_file(bucket_name, s3_key, local_path)
            logger.info(f"Downloaded PDF to local path: {local_path}")
            return local_path
        except Exception as e:
            logger.error(f"Error downloading PDF from S3: {str(e)}", exc_info=True)
            raise e
    else:
        # If it's a local path, just return the local path directly
        logger.info(f"Using local PDF path: {bucket_or_path}")
        return bucket_or_path


def discover_pdf_fields(pdf_template_path):
    """
    Discover form fields in a given PDF.

    :param pdf_template_path: The local file path of the template PDF
    :return: A dictionary of discovered form fields
    """
    logger.info(f"Opening PDF template: {pdf_template_path}")
    pdf_reader = PdfReader(pdf_template_path)
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
