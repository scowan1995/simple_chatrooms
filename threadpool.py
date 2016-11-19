"""
The method of creating a threadpool that has the tasks and ceating a
worker class that extends threads, each of which has access to a
queue of tasks was gotten from
http://code.activestate.com/recipes/577187-python-thread-pool/
released under MIT licence although mine does more stuff.
"""
from queue import Queue
from threading import Thread


class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.stop_flag = False
        self.start()


    def run(self):
        """ this gets run when a thread starts"""
        while True:
            if self.stop_flag:
                break
            else:
                func, kargs = self.tasks.get()
                if func:
                    try:
                        func(**kargs)
                    except Exception as e:
                        print(str(e))
                    self.tasks.task_done()
                else:
                    pass


class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.isStopped = False
        self.tasks = Queue(num_threads)
        for i in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, kargs))

    def num_tasks():
        return self.tasks.qsize()

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()

    def stop_working(self):
        """
        stops the threads from working but you can restart if you wish
        """
        for i in threading.enumerate():
            i.stop_flag = True
        isStopped = True

    def restart(self):
        if isStopped:
            for i in range(num_threads):
                Worker(self.tasks)
            self.isStopped = False
        else:
            raise AlreadyRunningError("AlreadyRunningError: You cannot \
                restart a threadpool that is already running")

    def purge_tasks(self):
        """ deletes all tasks in the task queue """
        for i in self.tasks:
            x = self.tasks.get()
            self.tasks.task_done()

class AlreadyRunningError(Exception):
    """
    Exception raised when you try to restart a threadpool that
    is already running
    """
    def __init__(self, message):
        self.message = str(message)

    def __str__(self):
        return self.message
