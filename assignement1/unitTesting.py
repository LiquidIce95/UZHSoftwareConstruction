# is needed for interfaces
from abc import ABC, abstractmethod
# is needed for class introspection
import inspect
# is needed for time measurement
import time
# is needed for predicatives
from functools import partial

# used for command line args
import sys

class TestCase(ABC):
    # test data in 2d dictionary whre first key is the name of
    # the function and second values are result and time
    # these attributes can be changed in the implementation of the tests
    # ASSUMPTION: order in which setups , teardown and testfunctions should be executed
    # is alphabetically by name of functions
    report = {}
    prefixTests = 'test'
    prefixSetup = 'setup'
    prefixTearD = 'teardown'
    selectPattern = ''    

    # predicates used for member introspection
    def Pred(self,prefix, member):
        return inspect.ismethod(member) and member.__name__.startswith(f"{prefix}")

    # function which is called on each test execution
    def execute(self,name:str,func):
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




    def runtests(self):
        # get members of instance of this interface
        Tests = inspect.getmembers(self,predicate=partial(self.Pred, self.prefixTests))

        if self.selectPattern != '':
            Tests = [(name, func) for name, func in Tests if self.selectPattern in name]

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

    

    def analysis(self):
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


# use this function to run tests (especially from command line) 
# argument is the testclass
def main(pattern='')->None:

    selectPattern = None
    for(name,obj) in globals().items():
        if 'TestCase' in name:
            Tests = obj()

            if len(sys.argv) == 2 and sys.argv[1].startswith("--"):
                selectPattern = sys.argv[1][2:]
                Tests.selectPattern = selectPattern
                Tests.runtests()
                Tests.analysis()
            
            else:
                Tests.runtests()
                Tests.analysis()

           

