def fix_end_of_chunk(chunk, text):
    if not chunk:  # Handle empty string case
        return chunk
        
    # If chunk doesn't end with a space, we're in the middle of a word
    # Find the next space to complete the word
    if chunk[-1] != " ":
        # Find the next space in the text after our current position
        next_space = text.find(" ", len(chunk))
        if next_space != -1:  # If we found a space
            # Take everything up to and including the space
            chunk = text[:next_space + 1]
        else:
            # If no space found, take the whole text
            chunk = text
            
    return chunk
def test_fix_end_of_chunk():
    text = "Hello world"
    
    # Test 1: Normal case - chunk ends at word boundary
    chunk = "Hello "
    assert fix_end_of_chunk(chunk, text) == chunk, "Should keep chunk ending at word boundary"
    
    # Test 2: Chunk cuts word in half
    chunk = "Hello wo"
    assert fix_end_of_chunk(chunk, text) == "Hello world", "Should complete the word"
    
    # Test 3: Empty chunk
    chunk = ""
    assert fix_end_of_chunk(chunk, text) == "", "Empty chunk should return empty string"

if __name__ == "__main__":
    print("Running simplified tests...")
    test_fix_end_of_chunk()
    print("All tests passed!")