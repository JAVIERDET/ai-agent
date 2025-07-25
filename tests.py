"""
tests.py
"""

import unittest
from unittest import TestCase

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file


class TestGetFilesInfo(TestCase):
    """
    Test suite for get_files_info function
    """

    def test_get_files_info(self):
        """
        Test for get_files_info function
        """
        w_dir = "calculator"
        cwdir = "."
        print("Result for current directory:")
        print(get_files_info(w_dir, cwdir))

        w_dir = "calculator"
        cwdir = "pkg"
        print(f"Result for {cwdir} directory:")
        print(get_files_info(w_dir, cwdir))

        w_dir = "calculator"
        cwdir = "/bin"
        print(f"Result for {cwdir} directory:")
        print(get_files_info(w_dir, cwdir))

        w_dir = "calculator"
        cwdir = "../"
        print(f"Result for {cwdir} directory:")
        print(get_files_info(w_dir, cwdir))

    def test_get_file_content(self):
        """
        Test for get_file_content function
        """


        w_dir = "calculator"
        file_name = "main.py"
        print(f"Result for {file_name} in {w_dir}:")
        print(get_file_content(w_dir, file_name))
        
        w_dir = "calculator"
        file_name = "pkg/calculator.py"
        print(f"Result for {file_name} in {w_dir}:")
        print(get_file_content(w_dir, file_name))
        
        w_dir = "calculator"
        file_name = "/bin/cat/"
        print(f"Result for {file_name} in {w_dir}:")
        print(get_file_content(w_dir, file_name))

    def test_write_file(self):
        """
        Test for write_file function
        """
        cwdir = "calculator"
        file_name = "lorem.txt"
        content = "wait, this isn't lorem ipsum"
        print(f"Result for {file_name} in {cwdir}")
        print(write_file(cwdir, file_name, content))

        cwdir = "calculator"
        file_name = "pkg/morelorem.txt"
        content = "lorem ipsum dolor sit amet"
        print(f"Result for {file_name} in {cwdir}")
        print(write_file(cwdir, file_name, content))

        cwdir = "calculator"
        file_name = "/tmp/temp.txt"
        content = "this should not be allowed"
        print(f"Result for {file_name} in {cwdir}")
        print(write_file(cwdir, file_name, content))   

    def test_run_python_file(self):
        """
        Test for run_python_file function
        """
        cwdir = "calculator"
        file_name = "main.py"
        print(f"Result for {file_name} in {cwdir}")
        print(run_python_file(cwdir, file_name))

        cwdir = "calculator"
        file_name = "tests.py"
        print(f"Result for {file_name} in {cwdir}")
        print(run_python_file(cwdir, file_name))

        cwdir = "calculator"
        file_name = "../main.py"
        print(f"Result for {file_name} in {cwdir}")
        print(run_python_file(cwdir, file_name))
        
        cwdir = "calculator"
        file_name = "nonexistent.py"
        print(f"Result for {file_name} in {cwdir}")
        print(run_python_file(cwdir, file_name))

if __name__ == "__main__":
    unittest.main()
