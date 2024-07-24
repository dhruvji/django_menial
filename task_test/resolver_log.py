import unittest
from unittest.mock import patch

# Import the module(s) that use get_resolver
from django.urls import resolvers  # Adjust this import as needed

class TestGetResolverCalls(unittest.TestCase):

    @patch('django.urls.resolvers.get_resolver')
    def test_get_resolver_calls_in_module1(self, mock_get_resolver):
        # Call a function that uses get_resolver
        resolvers.some_function_that_uses_get_resolver()

        # Check that get_resolver was called with log=True
        mock_get_resolver.assert_called_with(log=True)

    @patch('django.urls.resolvers.get_resolver')
    def test_get_resolver_calls_in_module2(self, mock_get_resolver):
        # Call another function that uses get_resolver
        resolvers.another_function_that_uses_get_resolver()

        # Check all calls to get_resolver
        for call in mock_get_resolver.call_args_list:
            args, kwargs = call
            self.assertTrue(kwargs.get('log', False), f"get_resolver called without log=True: {call}")

    @patch('django.urls.resolvers.get_resolver')
    def test_all_get_resolver_calls_in_module(self, mock_get_resolver):
        # Call multiple functions or run a process that might call get_resolver multiple times
        resolvers.process_that_calls_get_resolver_multiple_times()

        # Check that get_resolver was always called with log=True
        self.assertTrue(all(call[1].get('log', False) for call in mock_get_resolver.call_args_list),
                        "Not all calls to get_resolver had log=True")

if __name__ == '__main__':
    unittest.main()