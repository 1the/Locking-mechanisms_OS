# producer and consumer instruction using semaphore
# created by: Alaa Mah-moud
# CSE-55
# like a library shelf, a producer cant but in a full buffer and a consumer cant use an empty shelf
import threading
import time
import random

class Buffer:
    def __init__(self, size):
        # Initialize the buffer size and its elements
        self.size = size
        self.buffer = [None] * size
        # Semaphore to control access to the buffer
        self.mutex = threading.Semaphore(1)
        # Semaphore to track the number of empty positions in the buffer
        self.empty = threading.Semaphore(size)
        # Semaphore to track the number of full positions in the buffer
        self.full = threading.Semaphore(0)
        # Initialize indices for inserting and removing items
        self.next_in = 0
        self.next_out = 0

    def produce(self, item):
        # Acquire empty position
        self.empty.acquire()
        # Acquire mutual exclusion
        self.mutex.acquire()
        # Insert item into the buffer
        self.buffer[self.next_in] = item
        # Update index for the next insertion
        self.next_in = (self.next_in + 1) % self.size
        # Print produced item
        print(f"Produced {item}")
        # Release mutual exclusion
        self.mutex.release()
        # Release full position
        self.full.release()

    def consume(self):
        # Acquire full position
        self.full.acquire()
        # Acquire mutual exclusion
        self.mutex.acquire()
        # Retrieve item from the buffer
        item = self.buffer[self.next_out]
        # Clear the consumed item from the buffer
        self.buffer[self.next_out] = None
        # Update index for the next consumption
        self.next_out = (self.next_out + 1) % self.size
        # Print consumed item
        print(f"Consumed {item}")
        # Release mutual exclusion
        self.mutex.release()
        # Release empty position
        self.empty.release()

class Producer(threading.Thread):
    def __init__(self, buffer, max_iterations):
        super().__init__()
        self.buffer = buffer
        self.max_iterations = max_iterations

    def run(self):
        # Iterate for the specified number of times
        for _ in range(self.max_iterations):
            # Generate a random item
            item = random.randint(1, 100)
            # Produce the item
            self.buffer.produce(item)
            # Sleep for random duration
            time.sleep(random.random())

class Consumer(threading.Thread):
    def __init__(self, buffer, max_iterations):
        super().__init__()
        self.buffer = buffer
        self.max_iterations = max_iterations

    def run(self):
        # Iterate for the specified number of times
        for _ in range(self.max_iterations):
            # Consume an item
            self.buffer.consume()
            # Sleep for random duration
            time.sleep(random.random())

if __name__ == "__main__":
    # Create a buffer with a specified size
    buffer = Buffer(5)  # Adjust buffer size as needed
    # Set the maximum number of iterations for producer and consumer
    max_iterations = 10  # Adjust the maximum number of iterations
    # Create producer and consumer threads
    producer = Producer(buffer, max_iterations)
    consumer = Consumer(buffer, max_iterations)
    # Start producer and consumer threads
    producer.start()
    consumer.start()
    # Wait for threads to finish execution
    producer.join()
    consumer.join()
