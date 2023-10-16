from unitTesting import TestCase,main

class TestSuite1(TestCase):
    def test1(self):
        assert(1==2)
    def test2(self):
        assert(0==3/0)
    def testPattern(self):
        assert(1==1)


class TestSuite2(TestCase):
    def test1(self):
        assert(1==2)
    def test2(self):
        assert(0==3/0)
    def testPattern(self):
        assert(1==1)


if __name__ == "__main__":
    # Use introspection to automatically run all classes int test file
    main(globals().items())