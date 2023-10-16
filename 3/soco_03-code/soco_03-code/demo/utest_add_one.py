import unittest
from func import add_one

class TestAddOneFunction(unittest.TestCase):

    def test_add_one(self):
        # Test that 1 becomes 2
        self.assertEqual(add_one(1), 2)

        # Test that 0 becomes 1
        self.assertEqual(add_one(0), 1)

        # Test that -1 becomes 0
        self.assertEqual(add_one(0), 0)
    
    def test_add_one_(self):
        self.assertEqual(add_one(5), 6)


if __name__ == "__main__":
    unittest.main()

