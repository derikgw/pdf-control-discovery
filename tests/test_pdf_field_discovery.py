import json
import sys
from pathlib import Path

# Add the top-level directory to sys.path
top_level_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(top_level_dir))

from pdf_fields_discovery import discover_pdf_fields  # Absolute import


def test_discover_pdf_fields(pdf_template_path):
    # Discover form fields
    discovered_fields = discover_pdf_fields(pdf_template_path)
    print(json.dumps(discovered_fields, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_pdf_field_discovery.py <path_to_pdf>")
        sys.exit(1)

    pdf_template_path = sys.argv[1]
    test_discover_pdf_fields(pdf_template_path)