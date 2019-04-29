import threading
from threading import Thread

from random import randint
from time import sleep


class myThread (threading.Thread):
    def __init__(self, thread_id=0, thread_name='', name=''):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.threadName = thread_name
        self.name = name
        self.service_name = ""

    def run(self):
        print("execution statrted for %s" % self.threadName)
        self.service_name = print_name(self.name)
        self.llist.append(self.service_name)
        sleep(1)
        print("######")
        print("execution ended for %s" % self.threadName)
        # return self.service_name
        return self.llist


def print_name(name):
    # Sleeps a random 1 to 10 seconds
    # rand_int_var = randint(1, 10)
    # sleep(rand_int_var)

    print("Thread " + str(name) + " slept for " +  " seconds")
    print("*********")
    return name


threads = []


my_list = ['prateek', 'patel', 'mantu', 'chintu','manu','chiru']

global l
l = []




for i in my_list:
    # Instantiates the thread
    # (i) does not make a sequence, so (i,)

    # t = threading.Thread(target=print_name, args=(i,))
    threadName = i + "hello"
    thread = myThread(threadName=threadName, name=i, llist=l)
    threads += [thread]
    thread.start()


for x in threads:
    print("IIIIIIIIIIII")
    print(x.join())
    # t.start()
    # sleep(1)
    # print(threading.active_count())
    # # l.append(t.run())
    # print("i m here")
    # print(t.join())  # prints foo


print(l)

    # Sticks the thread in a list so that it remains accessible

# Starts threads
# for thread in thread_list:
#     thread.start()
#
# # This blocks the calling thread until the thread whose join() method is called is terminated.
# # From http://docs.python.org/2/library/threading.html#thread-objects
# for thread in thread_list:
#     thread.join()
#
# # Demonstrates that the main process waited for threads to complete
# print("Done")
#
# print(l)