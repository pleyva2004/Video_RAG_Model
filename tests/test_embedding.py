import unittest
from openai import OpenAI
from testing_embedding import embed_chunks

class TestEmbedding(unittest.TestCase):
    def setUp(self):
        self.client = OpenAI()
        self.test_chunks = [
            "Hello, world!",
            "This is a test.",
            "Testing embeddings."
        ]

    def test_embed_chunks_output_format(self):
        """Test that embed_chunks returns a list of embeddings"""
        embeddings = embed_chunks(self.client, self.test_chunks)
        
        # Check if output is a list
        self.assertIsInstance(embeddings, list)
        
        # Check if we got the same number of embeddings as input chunks
        self.assertEqual(len(embeddings), len(self.test_chunks))
        
        # Check if each embedding is a list of floats
        for embedding in embeddings:
            self.assertIsInstance(embedding, list)
            self.assertTrue(all(isinstance(x, float) for x in embedding))

    def test_embed_chunks_empty_input(self):
        """Test embed_chunks with empty input"""
        with self.assertRaises(Exception):
            embed_chunks(self.client, [])

    def test_embed_chunks_single_chunk(self):
        """Test embed_chunks with a single chunk"""
        single_chunk = ["Single test chunk"]
        embeddings = embed_chunks(self.client, single_chunk)
        
        self.assertEqual(len(embeddings), 1)
        self.assertIsInstance(embeddings[0], list)
        self.assertTrue(all(isinstance(x, float) for x in embeddings[0]))

if __name__ == '__main__':
    unittest.main() 