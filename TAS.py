# Test and Set instruction
# created by: Alaa Mah-moud
# CSE-55
# busy wait problem, starvation
import threading
import time

waiting = []   # to figure out the rest waiting

class SharedResource:
    def __init__(self):
        self.lock = threading.Lock()  # Create a lock object for synchronization
        self.resource_taken = False  # Flag to indicate if the resource is taken , default is free

    def test_and_set(self):
        with self.lock:  # Acquire the lock
            if self.resource_taken:  # If resource is already taken,true
                return False  # Return False to indicate resource is busy, true is busy but false for thread is busy
            self.resource_taken = True  # Set resource as taken because it was free,false
            return True  # Return True to indicate successful acquisition of resource because it was false

    def release_resource(self):
        with self.lock:  # Acquire the lock
            self.resource_taken = False  # Set resource as free to be released

    def use_resource(self, thread_name):
        entered = False  # Define entered variable before use
        if not self.test_and_set():  # wait until resource is successfully acquired
            print(f"{thread_name} is waiting for the resource...")
            waiting.append(thread_name)
        else:
            entered = True  # Indicate thread entered critical section
            print(f"{thread_name} is awake.")
            print(f"{thread_name} entered the critical section.")

        # Do some work with the resource
        if thread_name == "Thread 2" or thread_name == "Thread 4":
            time.sleep(4)

        if entered:     # only who entered critical can release
            self.release_resource()  # Release the resource
            print(f"{thread_name} released the resource.")

# Create a shared resource object
resource = SharedResource()

# Create multiple threads to use the resource concurrently
threads = []
for i in range(5):  # Example with 5 threads
    thread = threading.Thread(target=resource.use_resource, args=(f"Thread {i+1}",))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# check for the waiting list
for w in waiting:
    resource.use_resource(w)
