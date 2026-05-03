# :material-text-box-multiple-outline: Document Loaders (`maticlib.io`)

Load data from files or websites to process in a RAG pipeline.

### **Available Loaders**
- **`TextLoader`**: Reads standard `.txt` files.
- **`PDFLoader`**: Extracts text from `.pdf` files.
- **`DOCXLoader`**: Extracts text from Word documents.
- **`WebPageLoader`**: Scrapes and cleans text from public URLs.

```python
from maticlib.io import WebPageLoader

loader = WebPageLoader("https://example.com")
documents = loader.load()
```
