# test_pdf_field_service.py
import os
from pdf_field_service import download_pdf, discover_pdf_fields

def test_discover_pdf_fields():
    # Test data
    # template_path = "s3://your-bucket-name/pdf_templates/sample_template.pdf"  # Use local path or S3 path
    template_dir = os.path.expanduser("~/pdf_templates")  # Use local directory or S3 path
    template_path = f"{template_dir}/template_form1.pdf"

    # Download PDF (either from S3 or local)
    pdf_template_path = download_pdf(template_path)

    # Discover form fields
    fields = discover_pdf_fields(pdf_template_path)

    print("Discovered fields:", fields)

if __name__ == "__main__":
    test_discover_pdf_fields()
