# :material-pencil-ruler: Prompts & Memory (`maticlib.prompts` & `maticlib.memory`)

### **Prompts**
Use `BasePromptTemplate` and `PromptRegistry` to manage string formatting systematically. 

```python
from maticlib.prompts.registry import PromptRegistry

prompt = PromptRegistry.get("rag_qa")
formatted = prompt.format(context="Data...", question="What is it?")
```

### **Memory Buffers**
Maintain conversational history cleanly without blowing up context windows.
- **`ConversationBufferMemory`**: Stores all messages sequentially.
- **`WindowBufferMemory`**: A sliding window of the last `k` messages.

```python
from maticlib.memory.buffer import WindowBufferMemory
from maticlib.messages import HumanMessage, AIMessage

memory = WindowBufferMemory(k=10) # Keep last 10 messages
memory.add_message(HumanMessage(content="Hello!"))
memory.add_message(AIMessage(content="Hi there!"))
```
