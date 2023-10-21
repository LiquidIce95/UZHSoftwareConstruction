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
            assert(res==False)

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

    def test3_NonExistFile(self):
        try:
            res = file_manager.read_file('dontExist.txt')
            assert(res==None)
        except Exception:
            assert(res==False)

class FileManagerWriteFile(TestCase):
    def setup(self):
        self.f = open('test.txt','w+')
    def teardown(self):
        self.f.close()
        self.f = None
        os.remove('test.txt')
    def test1_WriteSomeContent(self):
        text = "Something I want to \ntest!"
        file_manager.write_file("test.txt", text)
        expected = self.f.read()
        assert(expected == text)
    def test2_WriteNonExistFile(self):
        text = "Something I want to \ntest!"
        file_name = "NoSuchFile.txt"
        status = file_manager.write_file(file_name, text)
        if os.path.isfile(file_name):
            status = False
            os.remove(file_name)
        assert(status == True)
    def test3_WriteToExistingText(self):
        self.f.write("This text was already here...\n")
        file_manager.write_file("test.txt", "More text to see here")
        expected = "This text was already here...\nMore text to see here"
        assert(self.f.read() == expected)

class FileManagerDeleteFile(TestCase):
    def setup(self):
        self.f = open('test.txt','w+')
    def teardown(self):
        self.f.close()
        self.f = None
        try:
            os.remove('test.txt')
        except FileNotFoundError:
            pass
    def test1_DeleteAFile(self):
        status = file_manager.delete_file("test.txt")
        if os.path.isfile("test.txt"):
            status = False
            os.remove("test.txt")
        assert(status)
    def test2_DeleteANonExistingFile(self):
        try:
            file_manager.delete_file("NoSuchFile.txt")
        except FileNotFoundError:
            assert(True)
        except Exception:
            assert(False)


if __name__ == '__main__':
    main()