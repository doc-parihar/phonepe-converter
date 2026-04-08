import pandas as pd
import json

def export_transactions(data, output_path, export_format='csv'):
    """
    Exports a list of transaction dictionaries to the specified format.
    """
    if not data:
        print("No transactions to export.")
        return False
        
    df = pd.DataFrame(data)
    
    if export_format.lower() == 'excel':
        df.to_excel(output_path, index=False, engine='openpyxl')
        print(f"Successfully exported {len(data)} transactions to {output_path} (Excel)")
    elif export_format.lower() == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Successfully exported {len(data)} transactions to {output_path} (JSON)")
    else:
        df.to_csv(output_path, index=False)
        print(f"Successfully exported {len(data)} transactions to {output_path} (CSV)")
        
    return True
