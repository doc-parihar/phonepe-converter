import os
import argparse
from src.parser import extract_text_from_pdf, parse_transactions
from src.exporter import export_transactions

def main():
    parser = argparse.ArgumentParser(description="PhonePe Statement Details Extractor")
    parser.add_argument("input", help="Path to the PhonePe PDF statement")
    parser.add_argument("--output", "-o", help="Output file path (default: output_statement.[format])")
    parser.add_argument("--format", "-f", choices=["csv", "excel", "json"], default="csv", help="Output format (csv, excel, json)")
    parser.add_argument("--password", "-p", help="Password to decrypt the PDF (usually the 10-digit PhonePe registered mobile number)", default=None)

    args = parser.parse_args()

    input_path = args.input
    if not os.path.exists(input_path):
        print(f"Error: Could not find file {input_path}")
        return

    # default output path
    if not args.output:
        if args.format == "excel":
            ext = "xlsx"
        elif args.format == "json":
            ext = "json"
        else:
            ext = "csv"
        args.output = f"output_statement.{ext}"

    print(f"Extracting text from {input_path} ...")
    raw_text = extract_text_from_pdf(input_path, password=args.password)
    
    print("Parsing transactions ...")
    transactions = parse_transactions(raw_text)
    
    if export_transactions(transactions, args.output, args.format):
        total_tx = len(transactions)
        total_credit = sum(tx["Amount (INR)"] for tx in transactions if tx.get("Type") == "Credit")
        total_debit = sum(tx["Amount (INR)"] for tx in transactions if tx.get("Type") == "Debit")

        print("\n" + "="*30)
        print("     STATEMENT SUMMARY")
        print("="*30)
        print(f"Total Transactions : {total_tx}")
        print(f"Total Credited     : INR {total_credit:,.2f}")
        print(f"Total Debited      : INR {total_debit:,.2f}")
        print("="*30 + "\n")
        
        print("Done!")

if __name__ == "__main__":
    main()
