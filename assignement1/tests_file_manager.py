from unitTesting import main,TestCase
import os
import file_manager

class FileManagerCreateFile(TestCase):
    def setup(self):
        self.f = open('test.txt','w+')        
    def teardown(self):
        self.f.close()
        self.f = None    
        try:
            os.remove('test.txt')
            os.remove('res.txt')
        except Exception:
            pass

    def test1_NameAndCreation(self):
        res = file_manager.create_file('res.txt')

        try:
            res = open('res.txt')
            assert(res==True)

        except Exception:
            assert(True==False)

    def test2_emptyContent(self):
        res = file_manager.create_file('res.txt')

        file = open('res.txt')
        content = file.read()

        assert(content=='')


    def test3_nonEmptyfileContent(self):
        teststring = 'blabla\nbla'

        file_manager.create_file('res.txt',teststring)

        res = open('res.txt','r')
        contentRes = res.read()
        res.close()

        self.f.write(teststring)

        assert(self.f.read()==contentRes)

    def test4_invalidFileName(self):
        res = file_manager.create_file('\0<>|')

        assert(res==False)


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
    main()