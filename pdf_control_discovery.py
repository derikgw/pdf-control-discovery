import json
import boto3
from pdf_fields_discovery import discover_pdf_fields

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Extract the template name from the request
        template_name = event.get('queryStringParameters', {}).get('templateName')
        if not template_name:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'templateName parameter is required'}),
                'headers': {'Content-Type': 'application/json'}
            }

        # Define S3 bucket and template path
        bucket_name = 'aws-sam-cli-managed-default-samclisourcebucket-kdvjqzoec6pg'
        pdf_template_s3_key = f'pdf_templates/{template_name}'

        # Paths in Lambda's tmp directory
        pdf_template_path = f'/tmp/{template_name}'

        # Download the template PDF from S3
        s3.download_file(bucket_name, pdf_template_s3_key, pdf_template_path)

        # Discover form fields from the template
        discovered_fields = discover_pdf_fields(pdf_template_path)

        # Return the form fields
        return {
            'statusCode': 200,
            'body': json.dumps({'formData': discovered_fields}),
            'headers': {'Content-Type': 'application/json'}
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }