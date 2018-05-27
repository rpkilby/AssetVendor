from unittest import TestCase

from assetvendor import __main__ as main

from .utils import capture_output


class MainTest(TestCase):
    def test_main(self):
        with capture_output() as out:
            main.main()

        stdout, stderr = out
        stdout.seek(0), stderr.seek(0)
        self.assertEqual(stdout.read(), 'hello\n')
        self.assertEqual(stderr.read(), '')
