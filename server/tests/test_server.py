import unittest

from server import create_server


class TestStringMethods(unittest.TestCase):

    def test_urls(self):
        self.assertEqual(create_server.check_file_type("/"), True)
        self.assertEqual(create_server.check_file_type("/foo"), True)
        self.assertEqual(create_server.check_file_type("foo"), False)
        self.assertEqual(create_server.check_file_type("foo/"), False)
        self.assertEqual(create_server.check_file_type(""), False)
        self.assertEqual(create_server.check_file_type("/."), False)
        self.assertEqual(create_server.check_file_type("./"), False)
        self.assertEqual(create_server.check_file_type("/./"), False)
        self.assertEqual(create_server.check_file_type("/../"), False)
        self.assertEqual(create_server.check_file_type("/.."), False)
        self.assertEqual(create_server.check_file_type("//"), False)
        self.assertEqual(create_server.check_file_type("/f"), True)
        self.assertEqual(create_server.check_file_type("/"), True)
        self.assertEqual(create_server.check_file_type("/f./"), False)
        self.assertEqual(create_server.check_file_type("/f.f"), False)
        self.assertEqual(create_server.check_file_type("/f.f/"), False)
        self.assertEqual(create_server.check_file_type("/f../"), False)
        self.assertEqual(create_server.check_file_type("/f.txt/"), False)
        self.assertEqual(create_server.check_file_type("/f.htm/"), False)
        self.assertEqual(create_server.check_file_type("/f.html/"), False)
        self.assertEqual(create_server.check_file_type("/f.txt"), True)
        self.assertEqual(create_server.check_file_type("/f.htm"), True)
        self.assertEqual(create_server.check_file_type("/f.html"), True)
        self.assertEqual(create_server.check_file_type("/f.jpg/"), False)
        self.assertEqual(create_server.check_file_type("/f.jpg"), False)


if __name__ == '__main__':
    unittest.main()
