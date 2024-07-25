import unittest
import ast
import os

class TestAdaptMethodMode(unittest.TestCase):

    def test_function_definition(self):
        # Path to the utils.py file containing adapt_method_mode
        file_path = '/data/dhruv_gautam/django_menial/django/core/handlers/handler_utils.py'  # Adjust this path to the actual location of your utils.py

        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'adapt_method_mode':
                # Check if the function has the correct arguments
                args = [arg.arg for arg in node.args.args]
                self.assertIn('is_async', args, "Missing 'is_async' parameter")
                self.assertIn('method', args, "Missing 'method' parameter")
                
                # Check for optional parameters
                optional_args = {'method_is_async', 'debug', 'name'}
                self.assertTrue(optional_args.issubset(args), "Missing one or more optional parameters")
                
                # Check the function body for async/sync adaptation logic
                has_async_sync_adaptation = any(
                    isinstance(stmt, ast.If) and 
                    any(
                        isinstance(cond, ast.Compare) and isinstance(cond.left, ast.Name) and cond.left.id == 'is_async'
                        for cond in ast.walk(stmt.test)
                    )
                    for stmt in node.body
                )
                self.assertTrue(has_async_sync_adaptation, "Missing async/sync adaptation logic in function body")
                
                return  # We found and checked the function, so we can stop here

        self.fail("adapt_method_mode function not found in the file")

    def test_import_in_base_handler(self):
        # Path to the base.py file
        file_path = '/data/dhruv_gautam/django_menial/django/core/handlers/base.py'  # Adjust this path to the actual location of your base.py

        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())

        # Check if adapt_method_mode is imported
        import_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == 'handler_utils':
                for alias in node.names:
                    if alias.name == 'adapt_method_mode':
                        import_found = True
                        break

        self.assertTrue(import_found, "adapt_method_mode not imported from utils in base.py")

if __name__ == '__main__':
    unittest.main()
