# Wait and Signal instruction
# created by: Alaa Mah-moud
# CSE-55
# no busy wait, but starvation
import threading

class SharedResource:
    def __init__(self):
        self.lock = threading.Lock()  # Create a lock object for synchronization
        self.resource_taken = False  # Flag to indicate if the resource is taken , default is free

    def wait(self):
        with self.lock:  # Acquire the lock
            if self.resource_taken:  # If resource is already taken,true
                return True  # Return True to indicate resource is busy
            self.resource_taken = True  # Set resource as taken because it was free,false
            return False  # Return False to indicate successful acquisition of resource

    def release_resource(self):
        with self.lock:  # Acquire the lock
            self.resource_taken = False  # Set resource as free to be released

    def signal(self, thread_name):
        if not self.wait():  #resource is successfully acquired
            print(f"{thread_name} entered the critical section.")

        self.release_resource()  # Release the resource
        print(f"{thread_name} released the resource.")

# Create a shared resource object
resource = SharedResource()

# Create multiple threads to use the resource concurrently
threads = []
for i in range(5):  # Example with 5 threads
    thread = threading.Thread(target=resource.signal, args=(f"Thread {i+1}",))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

