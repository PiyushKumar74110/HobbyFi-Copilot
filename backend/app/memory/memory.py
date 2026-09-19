from collections import defaultdict


# In-memory storage
# Key = vendor_id
# Value = conversation messages

conversation_memory = defaultdict(list)



def save_memory(
    vendor_id: int,
    user_message: str,
    assistant_response: str,
):

    conversation_memory[vendor_id].append(
        {
            "role": "user",
            "content": user_message,
        }
    )


    conversation_memory[vendor_id].append(
        {
            "role": "assistant",
            "content": assistant_response,
        }
    )


    # Keep only last 20 messages
    conversation_memory[vendor_id] = (
        conversation_memory[vendor_id][-20:]
    )



def get_memory(
    vendor_id: int,
):

    return conversation_memory.get(
        vendor_id,
        []
    )



def clear_memory(
    vendor_id: int,
):

    if vendor_id in conversation_memory:

        del conversation_memory[vendor_id]