# -*- coding: utf-8
"""
Tests for _nested_subclasses method.
"""
import unittest

from cuttle.model import _nested_subclasses


class NestedSubclassesTestCase(unittest.TestCase):

    def setUp(self):
        class Base(object):
            pass

        class A(Base):
            pass

        class B(A):
            pass

        class C(B):
            pass

        class D(C):
            pass

        class E(B):
            pass

        class F(E):
            pass

        self.Base = Base
        self.cls = A
        self.subclasses = [B, C, D, E, F]

    def test_nested_subclasses(self):
        ns = _nested_subclasses(self.cls)
        for cls in ns:
            self.assertIn(cls, self.subclasses)

        self.assertNotIn(self.cls, ns)
        self.assertNotIn(self.Base, ns)
