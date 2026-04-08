import pdfplumber
import re

def extract_text_from_pdf(pdf_path, password=None):
    """Extracts all text from the PDF pages, joining them cleanly."""
    text = []
    # If the PDF is protected, pdfplumber will try to decrypt it with the provided password
    with pdfplumber.open(pdf_path, password=password) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)

def parse_transactions(text):
    """
    Parses the full text string into a list of transaction dictionaries.
    Uses robust regex to handle wrapped lines and arbitrary column orders.
    """
    # Pattern to match PhonePe Date: e.g. 'Apr 14, 2025'
    date_pattern = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{2},\s+\d{4}"
    
    lines = text.split('\n')
    
    transactions = []
    current_block = []
    
    for line in lines:
        if re.match(date_pattern, line):
            if current_block:
                transactions.append(" ".join(current_block))
            current_block = [line]
        else:
            if current_block:
                current_block.append(line)
                
    if current_block:
        transactions.append(" ".join(current_block))
        
    parsed_data = []
    
    for block in transactions:
        # Check if the block is actually a transaction
        if not ("Transaction ID" in block or "UTR No" in block):
            continue
            
        # 1. Date
        date_match = re.search(r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{2},\s+\d{4})", block)
        date = date_match.group(1) if date_match else "Unknown"
        
        # 2. Type
        type_str = "Debit" if "Debit" in block else "Credit" if "Credit" in block else "Unknown"
        
        # 3. Amount
        amount = None
        # Often amount is directly after INR like: 'INR 500.00'
        amount_match = re.search(r"INR\s*((?:\d+,)*\d+\.\d{2})", block)
        if amount_match:
            amount = amount_match.group(1)
        else:
            # If line wrapped and separated, pick the isolated decimal number
            decimal_matches = re.findall(r"(?:\d+,)*\d+\.\d{2}", block)
            if decimal_matches:
                amount = decimal_matches[-1] # Usually the last floating point number is the amount
                
        # 4. Time
        time_match = re.search(r"(\d{2}:\d{2}\s+(?:AM|PM))", block)
        time_str = time_match.group(1) if time_match else ""
        
        # 5. Transaction ID
        tx_id_match = re.search(r"Transaction ID\s*:\s*([A-Za-z0-9]+)", block)
        tx_id = tx_id_match.group(1) if tx_id_match else ""
        
        # 6. UTR No
        utr_match = re.search(r"UTR No\s*:\s*([A-Za-z0-9]+)", block)
        utr_no = utr_match.group(1) if utr_match else ""
        
        # 7. Description / Details
        details = ""
        # Name is usually between the date and the transaction type keyword
        details_match = re.search(rf"{date}\s+(.*?)\s+(?:Debit|Credit)", block)
        if details_match:
            details = details_match.group(1).strip()
            
        parsed_data.append({
            "Date": date,
            "Time": time_str,
            "Details": details,
            "Type": type_str,
            "Amount (INR)": float(amount.replace(',', '')) if amount else 0.0,
            "Transaction ID": tx_id,
            "UTR No": utr_no
        })
        
    return parsed_data
