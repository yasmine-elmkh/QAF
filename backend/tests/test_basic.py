import unittest
from main import preprocess

class TestPreprocess(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(preprocess("Hello World!"), "hello world")

if __name__ == "__main__":
    unittest.main()
