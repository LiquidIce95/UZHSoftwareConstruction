from unitTesting import main,TestCase
import os
import file_manager

class FileManager(TestCase):
    def setup(self):
        self.f = open('test.txt','w')

    def teardown(self):
        self.f.close()
        self.f = None    
        os.remove('test.txt')

    def test1(self):
        file_manager.create_file('res.txt')

        res = open('res.txt')
        assert(self.f.read()==res.read())







if __name__ == '__main__':
    main(globals().items())