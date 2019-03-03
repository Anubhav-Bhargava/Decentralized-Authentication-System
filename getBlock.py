def find_records(form, blockchain):
    for block in blockchain:
        print(block.data)
        condition = (block.data[0] == form.get("username"))
        if condition:
            return block.data
    return -1
