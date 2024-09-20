import json
import boto3
from pdf_fields_discovery import discover_pdf_fields

s3 = boto3.client('s3')

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