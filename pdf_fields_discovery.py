from pypdf import PdfReader

def discover_pdf_fields(pdf_path):
    """Discover form fields in a given PDF."""
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
    return fields