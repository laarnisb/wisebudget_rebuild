import unittest
from user import register_user, login_user

class TestWiseBudget(unittest.TestCase):

    def test_register_and_login(self):
        username = "testuser"
        password = "secure123"
        register_user(username, password)
        result = login_user(username, password)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()