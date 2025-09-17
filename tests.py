import unittest
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    def test_current_directory(self):
        print("Result for current directory:")
        print(get_files_info("calculator", "."))
    
    def test_pkg(self):
        print("Result for 'pkg' directory:")
        print(get_files_info("calculator", "pkg"))

    def test_outside_wd(self):
        print("Result for '/bin' directory:")
        print(get_files_info("calculator", "/bin"))
    
    def test_abs_path(self):
        print("Result for '../' directory")
        print(get_files_info("calculator", "../"))

if __name__ == "__main__":
    unittest.main()