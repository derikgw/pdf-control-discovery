import json
import logging
from pdf_field_service import discover_pdf_fields, download_pdf  # Import functions from the service module

# Set up logging
if logging.getLogger().hasHandlers():
    # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
    # `.basicConfig` does not execute. Thus we set the level directly.
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

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

        # Log the extracted template name for debugging
        logger.info(f"Received template name: {template_name}")

        # Define S3 bucket and template path
        bucket_name = 's3://aws-sam-cli-managed-default-samclisourcebucket-kdvjqzoec6pg'
        pdf_template_s3_key = f'pdf_templates/{template_name}'

        # Log the generated S3 key for debugging
        logger.info(f"Generated S3 key: {pdf_template_s3_key}")

        # Paths in Lambda's tmp directory
        pdf_template_path = f'/tmp/{template_name}'

        # Download the template PDF from S3 using the new service function
        download_pdf(bucket_name, pdf_template_s3_key, pdf_template_path)

        # Discover form fields from the template
        discovered_fields = discover_pdf_fields(pdf_template_path)

        # Return the form fields
        return {
            'statusCode': 200,
            'body': json.dumps({'formData': discovered_fields}),
            'headers': {'Content-Type': 'application/json'}
        }

    except Exception as e:
        logger.error(f"Error processing the PDF discovery: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
