"""
Chatroom unit tests
"""
import unittest
from chatroom import Chatroom


class Chatroom_Test(unittest.TestCase):

    def test_create_room(self):
        CR = Chatroom("test room")
        self.assertEqual(CR.get_name(), "test room")

    def test_subscribe(self):
        CR = Chatroom("test")
        CR.subscribe("test user", "test ip", "test port")
        self.assertTrue("test user" in CR.subscribers)
        self.assertEqual(CR.subscribers["test user"], ("test ip", "test port"))
        self.assertFalse("not in" in CR.subscribers)

    def test_unsubscribe(self):
        CR = Chatroom("test")
        CR.subscribe("test user 1", "test ip 1", "test port 1")
        CR.subscribe("test user 2", "test ip 2", "test port 2")
        CR.unsubscribe("test user 1")
        self.assertFalse("test user 1" in CR.subscribers)
        self.assertTrue("test user 2" in CR.subscribers)

    def test_get_publish_list(self):
        CR = Chatroom("test")
        CR.subscribe("test user 1", "test ip 1", "test port 1")
        CR.subscribe("test user 2", "test ip 2", "test port 2")
        CR.subscribe("test user 3", "test ip 3", "test port 3 ")
        publish_list = CR.get_publish_list("test user 3")
        self.assertTrue(("test ip 1", "test port 1") in publish_list)
        self.assertTrue(("test ip 2", "test port 2") in publish_list)
        self.assertFalse(("test ip 3", "test port 3") in publish_list)

if __name__ == "__main__":
    unittest.main()
