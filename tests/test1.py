#! /usr/bin/python3
# -*- encoding: utf-8 -*-

import json
import unittest

import example_files
import homeconnect_2_telegraf_main

__author__ = 'Markus Pabst'
__since__ = '2025-03-17'
__credits__ = [""]
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = ""
__status__ = ""
__copyright__ = "Copyright 2025"


class MyTestCase(unittest.TestCase):
    def test_speed(self):
        speed: int = homeconnect_2_telegraf_main.get_washer_programs_active_spin_speed(
            example_files.get_programs_active_info_test_file())
        self.assertEqual(speed, 1000)

    def test_programs_active_name(self):
        program_name: str = homeconnect_2_telegraf_main.get_washer_programs_active_name(
            example_files.get_programs_active_info_test_file())
        self.assertEqual(program_name, 'Cotton.Eco4060')

    def test_programs_active_process_phase(self):
        program_name: str = homeconnect_2_telegraf_main.get_washer_programs_active_process_phase(
            example_files.get_programs_active_info_test_file())
        self.assertEqual(program_name, 'Washing')

    def test_program_progress(self):
        progress: int = homeconnect_2_telegraf_main.get_washer_programs_active_program_progress(
            example_files.get_programs_active_info_test_file())
        self.assertEqual(progress, 29)

    def testAll(self):
        homeconnect_2_telegraf_main.test_intern = True
        washers_json = homeconnect_2_telegraf_main.get_washers_json()
        print(washers_json)
        di_arr = json.loads(washers_json)
        self.assertEqual(len(di_arr), 1)
        self.assertEqual(di_arr[0]['name'], "KEKSE01")
        v: dict = di_arr[0]['v']
        self.assertEqual(v['is_connected'], True)
        self.assertEqual(v['programs_active_name'], 'Cotton.Eco4060')
        self.assertEqual(v['programs_active_process_phase'], 'Washing')
        self.assertEqual(v['programs_active_program_progress'], 29)
        self.assertEqual(v['programs_active_spin_speed'], 1000)

    # from io import StringIO
    # from unittest.mock import patch
    # @patch('sys.stdout', new_callable=StringIO)  # Mock stdout to capture help output
    # @patch('sys.argv', ['homeconnect_2_telegraf_main.py', '-h'])  # Mock command line arguments for help
    # def test_help(self, mock_stdout):
    #     with self.assertRaises(SystemExit):  # argparse raises SystemExit on help
    #         pass
    #     #     main.main('value1', 'value2')
    #     output = mock_stdout.getvalue()
    #     print(output)
    #     self.assertIn("usage:", output)  # Check if 'usage:' is in the help output
    #     self.assertIn("positional arguments:", output)  # Check for positional arguments section


if __name__ == '__main__':
    unittest.main()
