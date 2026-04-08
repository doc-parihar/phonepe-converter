# PhonePe Statement Converter - Project Context

## Project Overview
This project is a Python-based CLI tool designed to convert PhonePe Transaction Statement PDFs into structured spreadsheet formats (CSV, Excel) or JSON. It automates the extraction of transaction details like Date, Time, Amount, Transaction ID, and UTR Number, which are otherwise difficult to extract from the PDF format.

### Key Technologies
- **Python 3.8+**: Core language.
- **pdfplumber**: Used for high-fidelity text extraction from PDFs, including support for password-protected files.
- **pandas**: Used for data structuring and exporting to CSV/Excel.
- **openpyxl**: Engine for Excel (`.xlsx`) file generation.
- **re (Regex)**: Core logic for parsing unstructured text into structured transaction blocks.

## Architecture
- `main.py`: The entry point that handles CLI arguments (input path, output path, format, password) and orchestrates the parsing and exporting flow.
- `src/parser.py`: Contains logic for PDF text extraction (`extract_text_from_pdf`) and regex-based transaction parsing (`parse_transactions`).
- `src/exporter.py`: Handles saving the list of transaction dictionaries into the desired output format using pandas.

## Building and Running

### Setup
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Tool
- **Basic Conversion (to CSV)**:
  ```bash
  python main.py statement.pdf
  ```
- **Convert to Excel**:
  ```bash
  python main.py statement.pdf --format excel
  ```
- **Convert to JSON**:
  ```bash
  python main.py statement.pdf --format json
  ```
- **Password Protected PDF**:
  ```bash
  python main.py statement.pdf --password YOUR_MOBILE_NUMBER
  ```

### Testing
- There are currently no automated tests (e.g., `pytest`).
- **TODO**: Implement unit tests for `src/parser.py` using sample PDF text blocks to ensure regex robustness.

## Development Conventions

### Code Style
- Follows standard Python (PEP 8) conventions.
- Functions are documented with docstrings explaining their purpose and parameters.
- Modular design: Logic is separated into parsing and exporting modules.

### Parsing Logic
- The parser relies on a `date_pattern` (`MMM DD, YYYY`) to identify the start of a transaction block.
- Transaction blocks are joined into a single string before being parsed by specific regex patterns for Date, Time, Amount, and IDs.
- **Note**: PhonePe statement formats may change; the regex in `src/parser.py` should be the first place to check if parsing fails.

### Contributing
- Ensure any new dependency is added to `requirements.txt`.
- When adding new export formats, update both `main.py` (argparse) and `src/exporter.py`.
