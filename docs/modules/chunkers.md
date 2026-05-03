# :material-scissors-cutting: Chunkers (`maticlib.core.text.chunkers`)

Splits large documents into optimal `TextSegment`s for embedding.

### **Available Chunkers**
- **`SeparatorChunker`**: Splits cleanly by characters (e.g., `\n\n`).
- **`TokenBudgetChunker`**: Splits strictly by a max LLM token count using `tiktoken`.
- **`SemanticDifferenceChunker`**: Splits by detecting large shifts in meaning using vector math.
- **`HierarchicalChunker`**: Groups smaller child chunks into larger parent chunks for broad context retrieval.

```python
from maticlib.core.text.chunkers.token_budget import TokenBudgetChunker

chunker = TokenBudgetChunker(max_tokens=500, overlap_tokens=50)
segments = chunker.chunk(documents)
```
