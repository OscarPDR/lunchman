
# coding: utf-8

import unittest

from website.utils import fix_meal_name


class TestFixMealName(unittest.TestCase):

    def test_no_fix(self):
        original_value = u'Lorem ipsum'
        desired_value = u'Lorem ipsum'
        self.assertEqual(fix_meal_name(original_value), desired_value)

    def test_fix_trailing_space(self):
        original_value = u'Lorem ipsum '
        desired_value = u'Lorem ipsum'
        self.assertEqual(fix_meal_name(original_value), desired_value)

    def test_fix_leading_space(self):
        original_value = u' Lorem ipsum'
        desired_value = u'Lorem ipsum'
        self.assertEqual(fix_meal_name(original_value), desired_value)

    def test_fix_spaces(self):
        original_value = u' Lorem ipsum '
        desired_value = u'Lorem ipsum'
        self.assertEqual(fix_meal_name(original_value), desired_value)

    def test_fix_normal_slash(self):
        original_value = u'Lorem ipsum / Dolor sit amet'
        desired_value = u'Lorem ipsum'
        self.assertEqual(fix_meal_name(original_value), desired_value)

    def test_fix_attached_slash(self):
        original_value = u'Lorem ipsum/Dolor sit amet '
        desired_value = u'Lorem ipsum'
        self.assertEqual(fix_meal_name(original_value), desired_value)

    def test_fix_with(self):
        original_value = u'Lorem c/ipsum'
        desired_value = u'Lorem con ipsum'
        self.assertEqual(fix_meal_name(original_value), desired_value)

    def test_fix_full(self):
        original_value = u' Lorem c/ipsum / Dolor sit amet '
        desired_value = u'Lorem con ipsum'
        self.assertEqual(fix_meal_name(original_value), desired_value)


if __name__ == '__main__':
    unittest.main()
