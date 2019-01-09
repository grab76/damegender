#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2018  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

import unittest
import numpy as np
import os
from app.dame_gender import Gender

class TddInPythonExample(unittest.TestCase):

    def test_dame_gender_features_method_returns_correct_result(self):
        g = Gender()
        f = g.features("David")
        self.assertEqual(f['has(a)'], True)
        self.assertEqual(f['count(i)'], 1)
        self.assertEqual(f['count(v)'], 1)
        self.assertEqual(f['last_letter'], 'd')
        self.assertEqual(f['first_letter'], 'd')

    def test_sexmachine_features_int_method_returns_correct_result(self):
        g = Gender()
        features_int = g.features_int("David")
        self.assertTrue(features_int["first_letter"] == 100)
        self.assertTrue(features_int["last_letter"] == 100)
        self.assertTrue(features_int["vocals"] == 2)
        self.assertTrue(features_int["consonants"] == 2)
        self.assertTrue(features_int["first_letter_vocal"] == 0)
        self.assertTrue(features_int["last_letter_vocal"] == 0)
        self.assertTrue(features_int["first_letter_consonant"] == 1)
        self.assertTrue(features_int["last_letter_consonant"] == 1)
        #self.assertTrue(features_int["syllables"] == 2)
        self.assertTrue(features_int["last_letter_a"] == 0)
        self.assertTrue(len(features_int) > 0)

    def test_dame_gender_males_list_method_returns_correct_result(self):
        g = Gender()
        m = g.males_list()
        self.assertTrue("Adrian" in m)

    def test_dame_gender_females_list_method_returns_correct_result(self):
        g = Gender()
        f = g.females_list()
        self.assertTrue("Eva" in f)

    def test_dame_gender_guess_method_returns_correct_result(self):
        g = Gender()
        r = g.guess(name="David", binary=True)
        self.assertEqual(r, 1)
        r = g.guess(name="David", binary=False)
        self.assertEqual(r, "male")
        r = g.guess(name="Laura", binary=True)
        self.assertEqual(r, 0)
        r = g.guess(name="Laura", binary=False)
        self.assertEqual(r, "female")
        r = g.guess(name="Andrea", binary=True)
        self.assertEqual(r, 2)

    def test_dame_gender_csv2names_method_returns_correct_result(self):
        g = Gender()
        names = g.csv2names(path='files/partial.csv')
        self.assertTrue(len(names) > 10)

    def test_dame_gender_guess_list_method_returns_correct_result(self):
        g = Gender()
        self.assertEqual(['unknown', 'male', 'male', 'male', 'unknown', 'male', 'female', 'female', 'male', 'male', 'male', 'male', 'male', 'male', 'unknown', 'male', 'male', 'male', 'female', 'male', 'unknown'], g.guess_list(path="files/partial.csv", binary=False))
        self.assertEqual([2, 1, 1, 1, 2, 1, 0, 0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 2], g.guess_list(path="files/partial.csv",binary=True))


    def test_dame_gender_accuracy_method_returns_correct_result(self):
        g = Gender()
        self.assertTrue(g.accuracy(path="files/partial.csv") >= 0.5)

    def test_dame_gender_confusion_matrix_method_returns_correct_result(self):
        g = Gender()
        cm = g.confusion_matrix(path="files/partial.csv")
        print(cm)
        am = np.array([[3, 0, 0],[0, 13, 3],[0, 1, 1]])
        self.assertTrue(np.array_equal(cm,am))

    # def test_gender_guess_list_method_returns_correct_result(self):
    #     g = Gender()
    #     string = g.guess_list(path="files/partial.csv", binary=False)
    #     self.assertEqual('thomas', g.remove_quotes(string))
#        self.assertEqual([1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1], g.guess_list(path="file/partial.csv",binary=True))


    def test_dame_gender_gender_list_method_returns_correct_result(self):
        g = Gender()
        gl = g.gender_list()
        self.assertEqual(gl, [1, 1, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1])
        self.assertEqual(len(gl), 21)
        self.assertEqual(g.females, 3)
        self.assertEqual(g.males, 16)
        self.assertEqual(g.unknown, 2)

    def test_dame_gender_features_list_method_returns_correct_result(self):
        g = Gender()
        fl = g.features_list()
        self.assertTrue(len(fl) > 20)

    def test_dame_gender_features_list_categorical_method_returns_correct_result(self):
        g = Gender()
        flc = g.features_list_categorical('files/partial.csv')
        self.assertEqual(len(flc[0]), 6)
        self.assertEqual(flc[0], ["pierre","paul","grivel","pierre paul grivel","m","zbmath"])

    def test_dame_gender_features_list_no_categorical_method_returns_correct_result(self):
        g = Gender()
        flnc = g.features_list_no_categorical('files/partial.csv')
        self.assertTrue(len(flnc[0]) > 25)
        self.assertTrue(flnc[0], [0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3])

    def test_dame_gender_features_list2csv_method_returns_correct_result(self):
        # TODO: You can write asserts to verify the first line
        g = Gender()
        csv1 = g.features_list2csv()
        csv2 = g.features_list2csv(csv="categorical")
        csv3 = g.features_list2csv(csv="nocategorical")
        self.assertTrue(os.path.isfile("files/features_list.csv"))
        self.assertTrue(os.path.isfile("files/features_list_cat.csv"))
        self.assertTrue(os.path.isfile("files/features_list_no_cat.csv"))

    # def test_gender_remove_accents_method_returns_correct_result(self):
    #     g = Gender()
    #     ra = g.remove_accents("Inés")
    #     self.assertTrue(ra, "Ines")


    # def test_gender_features_list_all_method_returns_correct_result(self):
    #     g = Gender()
    #     fl = g.features_list(path="files/all.csv")
    #     self.assertTrue(len(fl) > 1000)
