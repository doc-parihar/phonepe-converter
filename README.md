# PhonePe Statement Converter

A robust, cross-platform CLI tool for converting PhonePe Transaction Statement PDFs to Spreadsheet (CSV/Excel) format.

## Setup

1. Make sure you have Python 3.8+ installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

You can extract transactions from your PhonePe statement PDF into a CSV or Excel file. 
*Note: Make sure your PDF is unlocked/decrypted before parsing.*

**Convert to CSV (Default):**
```bash
python main.py path/to/PhonePe_Statement.pdf
```
*Outputs to `output_statement.csv` by default in the current directory.*

**Convert to Excel:**
```bash
python main.py path/to/PhonePe_Statement.pdf --format excel
```

**Convert to JSON:**
```bash
python main.py path/to/PhonePe_Statement.pdf --format json
```

**Specify Custom Output Path:**
```bash
python main.py path/to/PhonePe_Statement.pdf --output my_finances.json --format json
```

**Password-Protected PDFs:**
If your bank statement is locked, simply pass the `--password` (`-p`) flag. PhonePe statements are typically protected by the user's 10-digit registered mobile number.
```bash
python main.py path/to/Locked_Statement.pdf --password 9876543210
```

## Contributing & Privacy

This is an open-source project released under the **MIT License**. Contributions, bug reports, and pull requests are always welcome!

> [!IMPORTANT]
> **Data Privacy Warning**: For developers intending to fork and contribute to this repository, please note that your personal PhonePe PDFs are highly sensitive. 
> To protect users, the repository includes a strict `.gitignore` profile which automatically prevents any `.pdf`, `.csv`, `.json`, or `.xlsx` files from being accidentally commited or uploaded to GitHub. 

If you are filing an issue regarding a parsing bug, please provide heavily anonymized sample data instead of your entire extracted JSON/CSV!
