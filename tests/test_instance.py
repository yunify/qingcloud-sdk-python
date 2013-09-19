import unittest
import env

class TestCase(unittest.TestCase):

    def test_describe_instances(self):
        resp = self.conn.describe_instances(limit=1)
        self.assertEqual(resp['ret_code'], 0)
        self.assertTrue(resp.has_key['instance_set'])

    def test_run_instances(self):
        #resp = self.conn.run_instances('hehe', cpu='a')
        pass

if '__main__' == __name__ :
    unittest.main()
