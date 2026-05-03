from typing import List, Tuple, Any

def format_as_markdown_table(columns: List[str], rows: List[Tuple]) -> str:
    """
    Converts database columns and rows into a beautifully formatted Markdown table.
    
    Args:
        columns: A list of column names.
        rows: A list of tuple rows returned by the database.
        
    Returns:
        A valid Markdown table string.
    """
    if not columns:
        return ""
        
    # Header row
    header = "| " + " | ".join(str(c) for c in columns) + " |"
    # Separator row
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    
    # Data rows
    data_lines = []
    for r in rows:
        row_str = "| " + " | ".join(str(v) if v is not None else "NULL" for v in r) + " |"
        data_lines.append(row_str)
        
    return "\n".join([header, separator] + data_lines)
