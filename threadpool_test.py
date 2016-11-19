import unittest
from threadpool import ThreadPool
from threadpool import AlreadyRunningError


class threadpool_test(unittest.TestCase):

    def myfunc(self, **kwargs):
        """
        sums a list of numbers and sets a test number to that amount
        """
        nums = kwargs["num_list"]
        kwargs["results"].append(sum(nums))

    def test_does_work(self):
        """tests to see if the threadpool functions actually do work"""
        sum1 = 0
        sum2 = 0
        sum3 = 0
        nums1 = [1, 2, 3]
        nums2 = [4, 5, 6]
        nums3 = [8, 9, 10]
        tp = ThreadPool(8)
        res1 = []
        res2 = []
        res3 = []
        kwargs1 = {"num_list": nums1, "results": res1}
        kwargs2 = {"num_list": nums2, "results": res2}
        kwargs3 = {"num_list": nums3, "results": res3}
        tp.add_task(self.myfunc, **kwargs1)
        tp.add_task(self.myfunc, **kwargs2)
        tp.add_task(self.myfunc, **kwargs3)
        tp.wait_completion()
        self.assertEqual(sum(nums1), res1[0])
        self.assertEqual(sum(nums2), res2[0])
        self.assertEqual(sum(nums3), res3[0])

        def test_add_task(self):
            sum1 = 0
            sum2 = 0
            sum3 = 0
            nums1 = [1, 2, 3]
            nums2 = [4, 5, 6]
            nums3 = [8, 9, 10]
            tp = ThreadPool(8)
            res1 = []
            res2 = []
            res3 = []
            kwargs1 = {"num_list": nums1, "results": res1}
            kwargs2 = {"num_list": nums2, "results": res2}
            kwargs3 = {"num_list": nums3, "results": res3}
            tp.stop_working()
            tp.add_task((self.myfunc, kwargs1))
            tp.add_task((self.myfunc, kwargs2))
            x = tp.num_tasks
            tp.add_task((self.myfunc, kwargs3))
            y = tp.num_tasks
            self.assertEqual(x + 1, y)

        def test_stop(self):
            tp = ThreadPool(8)
            tp.stop_working()
            assertTrue(tp.stop_flag)

        def test_restart(self):
            tp = ThreadPool(8)
            tp.stop_working()
            tp.restart()
            assertFalse(tp.stop_flag)

        def test_restart_raise_exception(self):
            """
            tests to see if restart raies an Exception
            when the threadpool is already running
            """
            tp = ThreadPool(8)
            assertRaises(AlreadyRunningError, tp.restart)

if __name__ == "__main__":
    unittest.main()
