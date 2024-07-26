# RemovedInDjango60Warning: Remove the is_iterable module.

from django.test import SimpleTestCase
from django.utils.deprecation import RemovedInDjango60Warning
from django.utils.able import make_hashable, is_iterable


class TestUtils(SimpleTestCase):
    def test_is_iterable_deprecation(self):
        msg = (
            "django.utils.itercompat.is_iterable() is deprecated. "
            "Use isinstance(..., collections.abc.Iterable) instead."
        )
        with self.assertWarnsMessage(RemovedInDjango60Warning, msg):
            is_iterable([])

    def test_make_hashable_equal(self):
        tests = (
            ([], ()),
            (["a", 1], ("a", 1)),
            ({}, ()),
            ({"a"}, ("a",)),
            (frozenset({"a"}), {"a"}),
            ({"a": 1, "b": 2}, (("a", 1), ("b", 2))),
            ({"b": 2, "a": 1}, (("a", 1), ("b", 2))),
            (("a", ["b", 1]), ("a", ("b", 1))),
            (("a", {"b": 1}), ("a", (("b", 1),))),
        )
        for value, expected in tests:
            with self.subTest(value=value):
                self.assertEqual(make_hashable(value), expected)

    def test_make_hashable_count_equal(self):
        tests = (
            ({"a": 1, "b": ["a", 1]}, (("a", 1), ("b", ("a", 1)))),
            ({"a": 1, "b": ("a", [1, 2])}, (("a", 1), ("b", ("a", (1, 2))))),
        )
        for value, expected in tests:
            with self.subTest(value=value):
                self.assertCountEqual(make_hashable(value), expected)

    def test_make_hashable_unhashable(self):
        class Unhashable:
            __hash__ = None

        with self.assertRaisesMessage(TypeError, "unhashable type: 'Unhashable'"):
            make_hashable(Unhashable())
