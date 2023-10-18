from unitTesting import main,TestCase
import os
import file_manager

class FileManagerCreateFile(TestCase):
    def setup(self):
        self.f = open('test.txt','w+')        
    def teardown(self):
        self.f.close()
        self.f = None    
        os.remove('test.txt')
        os.remove('res.txt')

    def test1_Name_and_Empty_content(self):
        file_manager.create_file('res.txt')

        res = open('res.txt')
        content = res.read()
        res.close()

        expected = self.f.read()
        assert(expected==content)

    def test2_fileContent(self):
        teststring = 'blabla\nbla'

        file_manager.create_file('res.txt',teststring)

        res = open('res.txt','r')
        contentRes = res.read()
        res.close()

        self.f.write(teststring)

        assert(self.f.read()==contentRes)


class FileManagerReadFile(TestCase):
    def setup(self):
        self.f = open('test.txt','w+')        
    def teardown(self):
        self.f.close()
        self.f = None    
        os.remove('test.txt')

    def test1_ReadEmptyContent(self):
        result = file_manager.read_file('test.txt')
        expected = self.f.read()

        assert(expected==result)

    def test2_ReadSomeCont(self):
        self.f.write('this is some text\n with a new line')
        result = file_manager.read_file('test.txt')
        expected = self.f.read()

        assert(expected==result)




if __name__ == '__main__':
    main(globals().items())