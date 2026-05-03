from maticlib.memory.buffer import WindowBufferMemory
from maticlib.messages import HumanMessage, AIMessage


def test_window_buffer_memory():
    mem = WindowBufferMemory(k=2)
    mem.add_message(HumanMessage(content="Hello"))
    mem.add_message(AIMessage(content="Hi"))
    mem.add_message(HumanMessage(content="How are you?"))

    msgs = mem.get_messages()
    assert len(msgs) == 2
    assert msgs[0].content == "Hi"
    assert msgs[1].content == "How are you?"

    # Check token counting heuristic
    # "Hi" = 2 chars, "How are you?" = 12 chars. Total = 14 chars. 14 // 4 = 3 tokens.
    assert mem.token_count == 3
