import unittest
import ast
import os

class TestGetResolverLogging(unittest.TestCase):

    def test_function_definition(self):
        # Path to the file containing get_resolver
        file_path = '/data/dhruv_gautam/django_menial/django/urls/resolvers.py'  

        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'get_resolver':
                # Check if the function has the correct arguments
                args = [arg.arg for arg in node.args.args]
                self.assertIn('urlconf', args, "Missing 'urlconf' parameter")
                
                # Check for the log parameter
                log_param = next((kw for kw in node.args.defaults if isinstance(kw, ast.NameConstant) and kw.value is False), None)
                self.assertIsNotNone(log_param, "log parameter with default False is missing")
                
                # Check the function body for log-related code
                log_check = any(
                    isinstance(stmt, ast.If) and 
                    isinstance(stmt.test, ast.Name) and 
                    stmt.test.id == 'log'
                    for stmt in node.body
                )
                self.assertTrue(log_check, "Missing log check in function body")
                
                return  # We found and checked the function, so we can stop here

        self.fail("get_resolver function not found in the file")

    def test_usages_have_log_true(self):
        # List of files to check
        files_to_check = [
            '/data/dhruv_gautam/django_menial/django/urls/base.py',
            '/data/dhruv_gautam/django_menial/django/conf/urls/i18n.py',
            '/data/dhruv_gautam/django_menial/django/core/checks/urls.py',
            '/data/dhruv_gautam/django_menial/django/core/handlers/exception.py',
            '/data/dhruv_gautam/django_menial/django/utils/autoreload.py',
            '/data/dhruv_gautam/django_menial/django/contrib/admindocs/views.py',
            '/data/dhruv_gautam/django_menial/django/core/handlers/base.py',
            '/data/dhruv_gautam/django_menial/tests/urlpatterns/test_resolvers.py',
            '/data/dhruv_gautam/django_menial/tests/urlpatterns_reverse/tests.py',
            '/data/dhruv_gautam/django_menial/tests/view_tests/views.py',
        ]

        for file_path in files_to_check:
            with open(file_path, 'r') as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    if node.func.attr == 'get_resolver':
                        if isinstance(node.func.value, ast.Name) and node.func.value.id in ['resolver', 'self', 'url_resolver']:
                            log_arg = next((kw for kw in node.keywords if kw.arg == 'log'), None)
                            self.assertIsNotNone(log_arg, f"log parameter missing in {file_path}")
                            self.assertTrue(
                                isinstance(log_arg.value, ast.NameConstant) and log_arg.value.value is True,
                                f"log is not True in {file_path}"
                            )

if __name__ == '__main__':
    unittest.main()
