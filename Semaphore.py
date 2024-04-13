# Semaphore instruction
# created by: Alaa Mah-moud
# CSE-55

import threading        # Importing threading module for managing threads
import time             # Importing time module for time-related operations


class Semaphore:
    def __init__(self):
        self.lock = threading.Lock()        # Creating a lock for thread synchronization
        self.value = 1          # Initializing semaphore value to 1 (available)
        self.waiting = 0        # the count of waiting threads

    def acquire(self):
        with self.lock:
            while self.value == 0:      # Using lock for thread safety
                self.waiting += 1       # Increment count of waiting threads
                self.lock.release()     # Release the lock temporarily
                time.sleep(0.1)     # Sleep briefly to allow other threads to proceed
                self.lock.acquire()     # Re-acquire the lock
                self.waiting -= 1       # Decrement count of waiting threads
            self.value = 0              # Mark semaphore as acquired

    def release(self):
        with self.lock:
            if self.waiting > 0:        # If there are waiting threads
                self.value = 1          # Mark semaphore as acquired
            else:
                self.value = 0          # Mark semaphore as available


def worker(semaphore, num):
    print(f"Worker {num} is waiting to acquire semaphore.")
    semaphore.acquire()
    print(f"Worker {num} acquired semaphore.")
    time.sleep(2)  # Simulate some work
    print(f"Worker {num} releasing semaphore.")
    semaphore.release()


def main():
    semaphore = Semaphore()         # Creating an instance

    # Create and start worker threads
    threads = []
    num_threads = 5
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(semaphore, i))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
