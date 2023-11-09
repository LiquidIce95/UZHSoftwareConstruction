import os
import file_manager


# is needed for interfaces
from abc import ABC
# is needed for class introspection
import inspect
# is needed for time measurement
import time
# is needed for predicatives
from functools import partial

# used for command line args
import sys

class TestCase(ABC):
    """test data in 2d dictionary whre first key is the name of
     the function and second values are result and time
     these attributes can be changed in the implementation of the tests
     ASSUMPTION: order in which setups , teardown and testfunctions should be executed
     is alphabetically by name of functions"""
    def __init__(self):
        self.report = {}
        self.prefixTests = 'test'
        self.prefixSetup = 'setup'
        self.prefixTearD = 'teardown'
        self.selectPattern = ''    


    # predicates used for member introspection
    def Pred(self,prefix:str, member : object)->bool:
        """
        args:
            prefix: string the specifies with which prefix the tests start
            member: object to check 
        returns the boolean expression needed for inspect.getmembers() 
        """
        return inspect.ismethod(member) and member.__name__.startswith(f"{prefix}")

    # function which is called on each test execution
    def execute(self,name:str,func)->None:
        """
        args: 
            name: is the name of the test function
            func: the actual test function
        
        """
        # init the dict
        self.report[name] = { 'result': 'undef', 'time': 'undef'}
        # use shorted ref to dict
        testd = self.report[name]

        endTime = 0
        startTime = time.time()
        try:
            func()
            endTime = time.time()
            testd['result'] = 'pass'
        except AssertionError:
            endTime = time.time()
            testd['result'] = 'fail'
        except Exception:
            endTime = time.time()
            testd['result'] = 'error'


        timeElapsed = endTime-startTime

        testd['time'] = f'{round(timeElapsed*1000,5)}'

        # give realtime visual feedback
        if testd['result'] == 'pass':
            print("\033[92m⬤\033[0m", end=' ')
        else:
            print("\033[91m⬤\033[0m", end=' ')




    def runtests(self)->None:
        """
        runs all tests within a testclass
        a class which implements TestCase interface
        """
        # get members of instance of this interface
        # partial returns a new function with self.prefixSetup as the prefix argument
        # self and member argumetns are inferred from the predicate
        # tests are in alph.order
        Tests = inspect.getmembers(self,predicate=partial(self.Pred, self.prefixTests))

        if self.selectPattern != '':
            Tests = [(name, func) for name, func in Tests if self.selectPattern.lower() in name.lower()]

        # setUps are the setup function sorted in alph. order
        # tearDs are teardown function sorted in alph. order
        setUps = inspect.getmembers(self,predicate=partial(self.Pred, self.prefixSetup))
        tearDs = inspect.getmembers(self,predicate=partial(self.Pred, self.prefixTearD))

        for (name,func) in Tests:
            # execute all setup functions 
            for (SetupName,Setup) in setUps:
                Setup()
            # execute the function
            self.execute(name,func)

            # execute all teardown functions
            for (TearDName,TearDown) in tearDs:
                TearDown()

    

    def analysis(self)->None:
        """
        generates a test report and prints it
        """
        print("\n")
        print("--TEST REPORT--")
        passes = 0
        fails = 0
        errors = 0
        for test in self.report:
            res = self.report[test]['result']
            time = self.report[test]['time']

            print(f'{test}, status :{res} ,time taken in ms :{time}')

            if res == 'pass':
                passes +=1
            elif res == 'fail':
                fails += 1
            else:
                errors += 1

         
        print(f'total passes {passes} total fails {fails} total errors {errors}')

        print("--END REPORT--")

        self.report = {}


def findItems()->dict:
    """
    returns globals of the current file
    """
    frame = inspect.currentframe()
    try:
        while frame.f_back:
            frame = frame.f_back
        return frame.f_globals.copy().items()
    finally:
        del frame

# creates a list from all the elements that are given after the --select command
# and then runs the tests for all the Keywords
def patternSelect(Test_obj:TestCase)->None:
    if sys.argv[1] == "--select":
        test_pattern = sys.argv[2:]
        for el in test_pattern:
            Test_obj.selectPattern = el
            Test_obj.runtests()
            Test_obj.analysis()
    else:
        raise Warning(f"The command {sys.argv[1]} is not valid. Please use --select")

# use this function to run tests (especially from command line) 
# argument is the testclass
def main(pattern : str ='')->None:
    """
    args: 
        items: globals().items() of your file
        pattern: optional, filter tests to be executed by a string which they must contain
    runs all test classes in your file in alphabetical order
    runs all setup functions in alph. order then test function then all teardown in alph.order
    the tests are run in alph. order
    """
    items = findItems()

    for(name,obj) in items:
        # execute all classes which implemented the interface but not the interface itself
        if name != 'TestCase' and inspect.isclass(obj) and issubclass(obj, TestCase):
            Tests = obj()
            if len(sys.argv) > 1:
                patternSelect(Tests)
            
            else:
                Tests.runtests()
                Tests.analysis()

           

# TESTS START HERE--------------------------------------------------------


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