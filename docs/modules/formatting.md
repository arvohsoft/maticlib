# :material-format-paint: Formatting Utilities (`maticlib.core.formatting`)

Useful helpers for converting complex execution outputs into clean, user-friendly Markdown content.

```python
from maticlib.core.formatting import format_as_markdown_table

columns = ["id", "name", "role"]
rows = [(1, "Alice", "Admin"), (2, "Bob", "Editor")]

table_md = format_as_markdown_table(columns, rows)
print(table_md)
```
