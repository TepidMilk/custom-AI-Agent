import unittest
from functions.get_file_content import run_python_file

class TestGetFilesInfo(unittest.TestCase):
    def test_current_directory(self):
        print("Result for current directory:")
        print(run_python_file("calculator", "main.py"))
    
    def test_pkg(self):
        print("Result for 'pkg' directory:")
        print(run_python_file(working_directory="calculator", file_path="main.py", args=["3 + 5"]))

    def test_outside_wd(self):
        print("Result for '/bin' directory:")
        print(run_python_file("calculator", "tests.py"))

    def test_error(self):
        print("Result for test error 1")
        print(run_python_file("calculator", "../main.py"))

    def test_error_2(self):
        print("Result for test error 2")
        print(run_python_file("calculator", "nonexistent.py"))

if __name__ == "__main__":
    unittest.main()