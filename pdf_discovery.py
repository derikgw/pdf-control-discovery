import json
from pypdf import PdfReader
import boto3

s3 = boto3.client('s3')

def discover_pdf_fields(pdf_path):
    """Discover form fields in a given PDF."""
    pdf_reader = PdfReader(pdf_path)
    fields = {}
    for page_num, page in enumerate(pdf_reader.pages):
        if '/Annots' in page:
            for annotation in page['/Annots']:
                field = annotation.get_object()
                field_name = field.get('/T')
                if field_name:
                    field_name = field_name.strip('()')
                    fields[field_name] = ""
    return fields

def lambda_handler(event, context):
    try:
        # Define S3 bucket and template path
        bucket_name = 'aws-sam-cli-managed-default-samclisourcebucket-kdvjqzoec6pg'
        pdf_template_s3_key = 'pdf-function-test/template.pdf'

        # Paths in Lambda's tmp directory
        pdf_template_path = '/tmp/template.pdf'

        # Download the template PDF from S3
        s3.download_file(bucket_name, pdf_template_s3_key, pdf_template_path)

        # Discover form fields from the template
        discovered_fields = discover_pdf_fields(pdf_template_path)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'formData': discovered_fields
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Internal server error',
                'error': str(e)
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }