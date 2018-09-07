# -*- coding: utf-8 -*-
import unittest
import os

# 用例路径
case_path = os.path.join(os.getcwd(), "TestCase")
# 报告存放路径
report_path = os.path.join(os.getcwd(), "Reports")


def all_case():
    discover = unittest.defaultTestLoader.discover(case_path, pattern="test_*.py", top_level_dir=None)
    # suite = unittest.TestSuite()
    # suite.addTest(discover)
    #
    # print(discover)
    return discover


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(all_case())
