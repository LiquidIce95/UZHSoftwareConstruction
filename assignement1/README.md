**How to use this framework**


import TestCase, main from unitTesting.py

call main here in your testfile which we refer to as testfile.py.

```python3   
from unitTesting import main,TestCase



if __name__ == "__main__":
    main()
```

now you can create multiple Test series which consist of multiple tests that share setup and teardown functions. You do this by implementing the TestCase interface.


```python3   
from unitTesting import main,TestCase

class TestSuite1(TestCase):
    def test1(self):
        assert(1==2)
    def test2(self):
        assert(0==3/0)
    def testPattern(self):
        assert(1==1)


class TestSuite2(TestCase):
    def setup(self):
        pass
    def teardown(self):
        pass

    def test1(self):
        assert(1==2)
    def test2(self):
        assert(0==3/0)
    def testPattern(self):
        assert(1==1)


if __name__ == "__main__":
    main()

```

When running this file, all Classes which implement 'TestCase' will be run (and their testfunctions).

As you can see you do not need to define setups or teardowns but if you do all functions which start with "setup" will be called in alphabetical order, same for functions wich start with "teardown". This allows you to break up more complex setups and teardown in multiple functions.

a valid testfunction starts with "test". Note that all these prefixed can be overwritten, by implementing a construction in your testclass

```python3   
from unitTesting import main,TestCase

class TestSuite1(TestCase):
    def test1(self):
        assert(1==2)
    def test2(self):
        assert(0==3/0)
    def testPattern(self):
        assert(1==1)


class TestSuite2(TestCase):
    def __init__(self):
        super().__init__()
        self.testprefix = 'foo'
    def setup(self):
        pass
    def teardown(self):
        pass

    def foo1(self):
        assert(1==2)
    def foo2(self):
        assert(0==3/0)
    def fooPattern(self):
        assert(1==1)


if __name__ == "__main__":
    main()

```

you **must** call the super constructor int this case


when you run python3 testfile.py --select Pattern it will only run tests with 'Pattern' in their name, this will be applied to all TestClasses.

It is up to the user to use appropriate assertions within the testfunctions, this framework does not provide any built in assertion mechanisms...

Below you find insights about the process this framework came to be.




**Design insights:**

The goal was to create a minimum viable version of the well-known unittesting framework for python in the context of a software design course. we focused on the following points.

    - Simplicity: It should be straightforward to understand and use. Minimizing the effort to test.
    - Flexibility: It should be adaptable to different use-cases without imposing unnecessary complexity.
    - Real-time Feedback: Users should get immediate feedback on the test progress. Which becomes more needed with bigger test sets, allwoing the user to stop mid test set if he sees errors with certain funcitons. 
    - Structured Reporting: At the end of the tests, a summary should provide clear insights.

**The importet libraris:**

    - "ABC"
    - "inspect"
    - "time"
    - "partial"
    - "sys"

**Why we used those libraries:**

ABC: 
    
    Motivation:
        The decision to make our TestCase class an abstract class is because TestCase is meant to be a generic test case template, and actual test cases should be derived from it, making the testing framwork more flexible to use, given that the user has to make it fit his test set. 
        
        It might reduce simplicity a bit, because this class is meant to be subclassed and should not be instantiated directly, if done so it would lead to an error. But we decided that the benefits of a more flexible, or better said a more cutstomizable, framework would overshadow the minor loss in simplicity. 

        We think that a more custom framework for a certain test set is better because :
            1. a custom implementations based on the abstract class will likely be better aligned with the unique testing needs of each project. This can lead to more effective and efficient testing. 
            2. this helps users focus only on the methods and functionalities they need, rather than getting bogged down by unnecessary features or methods that a more generic, non-abstract framework might offer.
            3. by providing an abstract class, we are ensuring that users of our framework don't just adopt a one-size-fits-all approach. Instead, they have to think about their specific testing requirements and implement methods that are relevant to their context.

    Alternatives:
        Simply provide a base class without marking it as abstract, the base class can have default implementations that subclasses can override which makes the framework easier to use but not as cutom because users could just use the default base. 

inspect: 

    Motivation:
        We use inspect to allow the testing framework to use introspection. This part is covered by the Pred funciton. 

        "inspect" is a standard library for python, which allows everybody that uses the framework to simply use it without any dependencys thus makes the usage of our testing framework easier. 

        By using the inspect module we allow our Pred function to discover which methods, in an existing class or module, fit certain criteria, like having a certain prefix. This way the user can not make the mistake of adding a decorator to a function, which then would make the test framework not work as intended, which would be the case when using alternatives.  

    Alternatives:
        The first version we built used a decorator to automatically add @register_method to a registered_methods list which then would check if a function existed. But this had the possibility of the user forgetting to add the @register_method to a function and then the introspection would not have worked as intended. 

        The benefits of this would have been if we know in advance which methods you want to take action on, then decorators provide a clean and explicit way to do this, but we tried to construct our framework to be as easy to use as possbile which demands to minimize the possiblities for user error. 

time: 

    Motivation:
        We needed to return the time the tests took to run, and using the time module allows us to do this.  

    Alternatives:
        When we first thought about how to implement our framework and how to add the time to the final report of the tests, we look into how the time module works in python, because we wanted to create our own funciton that would do this.

        But we discovered that achieving high precision time measurements usually requires interfacing directly with hardware or using low-level system calls, which are typically available via C libraries. Which would make the code alot more complicated than it needed to be. 
        
        Or implementing time operations without relying on underlying libraries means we likely would need to interface directly with the hardware or operating system. This would make our code less portable, as we would need different implementations for different operating systems or hardware platforms. Which would make the framework anything but simple to use!

partial:
    Motivation:
        The primary objective was to create a flexible, yet consistent way to filter methods of a class based on their prefixes like "test", "setup", and "teardown". functools.partial allows us to achieve this by creating specialized versions of a general predicate function (Pred), without having to rewrite multiple similar functions. This ensures that our code does not include repetitions and is easily maintainable.

    Alternatives:
        Initially, when contemplating how to determine methods based on their prefixes, one might consider writing separate functions for each prefix. For instance, one function to check for 'test' prefixed methods, another for 'setup' prefixed methods, and so on.However, this would quickly become cumbersome and lead to code duplication, especially if more prefixes were to be added in the future. We could also consider using lambda functions to achieve a similar result, but this can make the code less readable for those unfamiliar with lambda functions.

        Another approach might involve passing the prefix as an argument to the predicate function every time it's called, but this would involve changing the signature of the predicate function to accept more arguments, thereby complicating the invocation.

sys: 
    Motivation:
        The main goal was to provide users of the testing framework a seamless way to interact and influence its behavior directly from the command line. Using sys.argv offers this ability by giving access to command-line arguments passed during invocation. 
        
        It empowers users to specify particular patterns for test execution, enhancing the framework's flexibility.

    Alternatives:
        At the onset of designing the framework, there were a few methods we contemplated for user input:
        1. Reading from a Configuration File: A dedicated configuration file could be used where users specify the test patterns they wish to run. However, this would require users to maintain and modify an additional file, possibly leading to management overhead.

        2. Interactive Prompts: The framework could prompt users for input interactively each time it's run. This method is user-friendly but might interrupt automated processes or batch executions of tests.
        
        3. Environment Variables: We could use environment variables to control the behavior of the testing framework. While this approach is flexible, it can become complex as the number of parameters grows, and users might overlook or forget to set certain environment variables.

**Why a class based framework:**
    Motivation:
        Utilizing a class as the base in our testing framework delivers structure and encapsulation, we can group related testing functionalities and state (like setup, teardown, and report generation) cohesively, ensuring a clear organization. The object-oriented nature of classes also facilitates inheritance, allowing for extensions or modifications without changing the core framework. This makes it easy to reuse and maintain.

    Alternatives:
        Instead of classes, the framework could rely solely on functions. This would mean passing around states (like test reports) as arguments and return values. While this might simplify the initial implementation, it could become cumbersome and less readable as the framework grows in complexity.



**How the functions work and why we decided that they should work like this:**

__init__:

    How:
        This is of cours just the constructor for the TestCase class. The constructor sets default prefixes for test fuctions, the teardown funciton as well as the setup function. We think that these prefixes are very standard and thus using them makes sense. 

        If a user decides he does not want those exact values he can of course change in the constructor in his subclass making the framework more flexible.

        When the user follows the default conventions set by the framework (e.g., using prefixes like test_, setup_, and teardown_), it enables introspection capabilities within the framework. The introspection with an implementation like this is very straight forward, which can be seen in the Pred funciton. 

    Alternatives:
        No predefined defualt prefixes for the different funcitons. This would, at least in our opinion, the introspection harder and we also do not see a need for this, given that most developers follow certain naming convetions. 

Pred:

    How:
        This funciton is what allows the framework to use introspection. The Pred funciton is a utility for filtering methods of an object based on their name's prefix.
        
        It returns true if member is a method of a class and if the member start with a certain prefix. Otherwise it will return false. 

    Alternatives:
        Manual registration of the test using decorators. This could potentailly lead to user errors thus it is not a good solution.

execute:

    How:
        The execute function is responsible for running a test, recording its outcome (pass, fail, or error), measuring its execution time, and providing immediate visual feedback on the test result.

        The execute method is designed to execute a given test function and monitor its outcome within a testing framework. 
        
        On initiation, it establishes a dictionary entry in self.report keyed by the test's name, initializing both result and execution time as undefined. 
        
        The test function, func, is then invoked; if it runs without hitches, the result is marked as 'pass', but if it encounters an AssertionError, it's labeled as 'fail', and for other exceptions, it's labeled as 'error'. 
        
        The method captures the start and end times of the test to calculate and store its execution duration in milliseconds. 
        
        Finally, for immediate visual feedback, a green or red circle is printed to the console, representing the test's success or failure respectively.
    
    Alternatvies:

runtests:

    How: 
        The runtests method is a centerpiece of the given testing framework, serving as the conductor that coordinates the execution of test functions within any class that implements the TestCase interface. 
        
        Initially, it identifies all test methods with the designated prefix, by defualt this is "test" from the class, unsing the inspect module combined with  the Pred funciton. If a specific selection pattern has been defined in self.selectPattern, the method further refines this list, focusing only on tests whose names match the pattern. Allowing the testing framework to be more focues if this is a behaviour wanted by the user, thus making it more flexible.

        To establish a controlled environment for each test, the method also identifies "setup" and "teardown" functions using their respective prefixes, by default those are "setup" and "teardown". As tests are executed, each test environment is first primed using the setup functions, followed by the test itself, and subsequently reset or cleaned up using the teardown functions. This implementation ensures a structured and predictable test execution sequence. Every test is encapsulated between setup and teardown, ensuring consistency and isolation.

        The use of method prefixes for test, setup, and teardown functions provides a simple and intuitive way to expand the test suite. Users just need to follow the naming conventions or change the default when creating a subclass.

    Alternatvies:
        As mentioned before instead of using introspection to discover methods based on prefixes, tests could be registered explicitly using decorators or by adding them to a list. But this also means that every new test function added would need to be explicitly registered, adding an extra step in the test creation process and adding an extra possiblity for users of the framework the forget to register them leading to the test being skipped and the user thinking that it worked. 

        We thought about making use of dependency injecitons for the tests, meaning we  would inject mock or stub objects into a class during testing, making it easier to test classes in isolation without invoking their real dependencies. But given that this is simply a framework introducing dependency injection would add a layer of complexity, reducing the simplicity especially when using simple test sets. 

        External configuration files could have been used to define test sequences, dependencies, and other test metadata, but this would also lead to a separation between test logic and test orchestration which would again make it less simpler, by makeing it harder to get a cohesive view of the test's behavior. This would also mean that when chaning the logic of a test it would create the necessity to update the configuration files. 

analysis:
    How:
        The analysis function operates as a reporting mechanism for a collection of test results:

        The function starts by printing two newline characters, ensuring that the report appears visually separated from other console outputs.
        The header "--TEST REPORT--" is then printed, signaling the beginning of the report.

        Three counters, passes, fails, and errors, are initialized to zero. These counters are integral to the summary generation at the function's conclusion.

        The function enters a loop, iterating over each test entry in the self.report dictionary. For each test, it retrieves its result (res) and its execution time (time). The function then prints a line containing the test's name, its result status, and the time taken in milliseconds. Following this, the function examines the test's result to determine which counter to increment. 

        Post iteration, the function prints a summary of the test results. This summary contains the total number of tests that passed, failed, or encountered errors. It provides a quick overview for the user to grasp the overall testing outcome.

        A footer, "--END REPORT--", is printed to signify the end of the report.

        Finally, the function clears the self.report dictionary. This action ensures that any subsequent tests run will start with a clean slate, preventing the mixing of old and new results. By emptying the self.report at the end, the function ensures that old data doesn't persist, preparing the system for fresh tests.

    Alternatives:
        We could have made to output of the function prettier by utailizing a library or module to format the report more beautifully, perhaps with tables, color coding, etc. (like prettytable or tabulate) and not just print statments in the command line. This might have made the test report easier to read or more detailed, but this would introduce external dependencies making it less simple. 

finditems:

    How:
        The findItems function leverages introspection to retrieve global variables and their associated values from the script's origin or starting point.

        The function begins by using inspect.currentframe() to acquire the current stack frame. This frame corresponds to the environment in which findItems was called.

        Utilizing a while loop, the function navigates backward through the execution call stack. It does this by continuously accessing the f_back attribute of the current frame. The loop halts when it reaches the outermost frame, signifying the script's entry point.

        The outermost frame's global variables and their respective values are fetched using f_globals.items(), which retrieves them as key-value pairs.

        In a finally block, the frame variable is explicitly deleted to break potential reference cycles, ensuring smoother garbage collection.

        By navigating through the call stack, the function guarantees that it fetches globals from the script's starting point, not just the immediate environment.

        The function can be called from any depth within the script or its imported modules, and it will still retrieve the originating script's globals. 

    Alternatives:
        We could have called globals() directly, but this would only have fetched the globals from the scope in which globals() was called, not necessarily from the script's start point.

        At the beginning of a script, we could store the result of globals() in a specific variable to be referenced later. It would require manual setup in each script and might not capture all globals if new ones are declared after the initial storage.

        Instead of introspecting the runtime environment, we could have passed required global variables as arguments to functions or store them in a configuration object. This approach could have potentailly been less flexible and would require a more manual, structured setup. It could also lead to cumbersome function signatures if many globals are involved.

patternSelect:
    How:
        The patternSelect function is tailored to filter and execute tests from a given TestCase object based on patterns provided as command-line arguments. Subsequently, it generates an analysis report for the tests executed.

        The function accesses the sys.argv list, which holds the command-line arguments passed to a script. The script name is sys.argv[0], with subsequent arguments starting from sys.argv[1]. By using command-line arguments, users can dynamically choose which tests to run without altering the scrip, making the framework more flexibl.

        The function checks if the first argument (sys.argv[1]) is --select. If --select is present, it regards the subsequent arguments (sys.argv[2:]) as test patterns. For each pattern:
            a. The pattern is assigned to the selectPattern attribute of the Test_obj.
            b. The runtests method of Test_obj is invoked to run tests matching the pattern.
            c. The analysis method of Test_obj generates a report for the executed tests.

        If the user does not provide --select as the first argument, a warning is raised, suggesting the appropriate usage.
    
    Alternatvies:
        As mentioned before: Instead of using command-line arguments, tests can be selected using configuration files. The user specifies the desired test patterns in the file, and the function reads from it. This approach can be less dynamic, as changing test patterns requires modifying and saving the configuration file. It also introduces potential complexities related to file parsing and handling.

        The function could interactively prompt users to input their desired test patterns. is might slow down automated test runs, as it requires user interaction for every test session.

        Rather than simple string matching, the function could support regular expressions for more intricate pattern matching. But we thought that it is very standard to use naming convetions for tests. And it could be complex and might introduce an overhead for simple test selections. Users unfamiliar with regex might find it challenging to use and thus reducing the simplicity of the framwork.

main:
    How:
        The main function serves as the primary entry point for executing the testing framework

        The main function begins its operations by calling the findItems function. This function navigates the call stack to its origin, and fetches all the global items from that frame, which in essence means it retrieves all global variables, functions, and classes defined in the script where main is invoked. This approach automatically detects all the globally defined items, eliminating the need for manual registration or declaration of test classes. For small to medium-sized scripts or testing modules, this method is straightforward and requires minimal setup from the user's end. 

        Once all global items are fetched, the function filters to find classes derived from the TestCase interface. This ensures that only relevant test classes are executed. By identifying classes that inherit from TestCase, the framework ensures that only valid test cases are executed, avoiding potential errors or irrelevant function calls and as more test classes are added to the script, they will be automatically included in the testing without any changes needed in the main function.

        The presence of command-line arguments (stored in sys.argv) determines the mode of test execution. If arguments are provided, the patternSelect function is called to execute tests matching the given patterns. Without arguments, all tests in the identified test classes are executed thus users of our framework have the option to either run specific tests (using patterns) or all tests, making it adaptable to different testing scenarios and allowing developers to get quick feedback on specific areas of the codebase or the code in total.

        In essence, the current design of our the main function and its associated methods offers a blend of automation and flexibility, providing a simple yet effective platform for unit testing. It's particularly advantageous for scenarios where quick setup and iterative testing are prioritized and thus this is our submission!

    Alternatvies:
        As mentioned before but given that the main functions is the entry point for the execution of our framework here again:

        Instead of solely relying on command-line arguments, the function could read from a configuration file or environmental variables to determine which tests to run. This would allow the user of our framework to define test patterns or configurations beforehand, without needing to provide them each time the script is run. But as mentioned above we decided against this apporach for the above mentioned arguemnts. 

        We also thought about loggin the results: instead of direct print statements for test outcomes, a logging system could be integrated. This would offer more flexibility in terms of logging levels (debug, info, warning, error) and output formats (console, file, etc.).

        And the automatic discovery of tests could also be omitted for a manual registraition.


