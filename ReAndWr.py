# Readers and Writers instruction using semaphore
# creadted by: Alaa Mah-moud
# CSE-55
# a reader cant read while a writer writes, two writers cant write concurrently, a writer cant write if he didnt request for it
import threading
import time

class AirlineReservationSystem:
    def __init__(self):
        # Number of readers and writers
        self.R1 = 0  # Number of readers who have requested a resource and have not yet released it
        self.R2 = 0  # Number of readers who are using a resource and have not yet released it
        self.W1 = 0  # Number of writers who have requested a resource and have not yet released it
        self.W2 = 0  # Number of writers who are using a resource and have not yet released it

        # Semaphores for controlling access
        self.readers_mutex = threading.Semaphore(1)       # Mutex for readers count
        self.writers_mutex = threading.Semaphore(1)       # Mutex for writers count
        self.resource_mutex = threading.Semaphore(1)      # Mutex for resource access
        self.resource_available = threading.Semaphore(1)  # Semaphore indicating resource availability

    def reader(self):
        # Check if a writer has requested a resource or is currently using it
        self.readers_mutex.acquire()  # Acquire readers mutex
        if self.W1 + self.W2 > 0:  # If there are writers, block readers
            self.readers_mutex.release()  # Release readers mutex
            self.resource_available.acquire()  # Acquire resource available semaphore
            self.resource_available.release()  # Release resource available semaphore
            self.readers_mutex.acquire()  # Acquire readers mutex again
        self.R1 += 1  # Increment the count of readers
        self.readers_mutex.release()  # Release readers mutex

        # Read the resource
        print("Reader reading...")  # Indicate that reader is reading
        # Simulate reading process
        print("Resource read.")  # Indicate that reading is finished

        # Release the resource
        self.readers_mutex.acquire()  # Acquire readers mutex
        self.R1 -= 1  # Decrement the count of readers
        self.R2 += 1  # Increment the count of readers who are using the resource
        if self.R1 == 0:  # If no readers, release resource for writers
            self.resource_available.release()  # Release resource available semaphore
        self.readers_mutex.release()  # Release readers mutex

    def writer(self):
        # Check if any readers are using the resource
        self.writers_mutex.acquire()  # Acquire writers mutex
        if self.R1 + self.R2 > 0:  # If there are readers, block writers
            self.writers_mutex.release()  # Release writers mutex
            self.resource_available.acquire()  # Acquire resource available semaphore
        else:
            self.W1 += 1  # Increment the count of writers
            self.writers_mutex.release()  # Release writers mutex

        # Write to the resource
        self.resource_mutex.acquire()  # Acquire resource mutex
        print("Writer writing...")  # Indicate that writer is writing
        # Simulate writing process
        time.sleep(1)
        print("Resource written to.")  # Indicate that writing is finished
        self.resource_mutex.release()  # Release resource mutex

        # Release the resource
        self.writers_mutex.acquire()  # Acquire writers mutex
        self.W1 -= 1  # Decrement the count of writers
        self.W2 += 1  # Increment the count of writers who are using the resource
        if self.W1 == 0:  # If no writers, release resource for readers
            self.resource_available.release()  # Release resource available semaphore
        self.writers_mutex.release()  # Release writers mutex

if __name__ == "__main__":
    system = AirlineReservationSystem()  # Create an instance of AirlineReservationSystem
    threads = []  # List to hold thread instances
    writer_active = False  # Flag to track if a writer is currently active

    while True:  # Infinite loop for user interaction
        print("\nPress:")  # Print options for the user
        print("1: Acquire reader")
        print("2: Read")
        print("3: Acquire writer")
        print("4: Write")
        print("5: Quit")

        choice = input("Enter your choice: ")  # Prompt the user for input

        if choice == "1":  # If the user chooses to acquire reader
            if not writer_active:  # Check if a writer is currently active
                thread = threading.Thread(target=system.reader)  # Create a thread for reader
                thread.start()  # Start the thread
                threads.append(thread)  # Add the thread to the list of threads
            else:
                print("Resource locked by writer. Cannot read.")  # Notify user that reading is not possible
        elif choice == "2":  # If the user chooses to read
            if not writer_active:  # Check if a writer is currently active
                print("Reader reading...")  # Simulate reader reading
                time.sleep(1)
                print("Reader finished reading.")  # Indicate that reading is finished
            else:
                print("Resource locked by writer. Cannot read.")  # Notify user that reading is not possible
        elif choice == "3":  # If the user chooses to acquire writer
            system.writer()  # Execute writer function
            writer_active = True  # Set writer active flag
        elif choice == "4":  # If the user chooses to write
            if writer_active:  # Check if a writer is currently active
                print("Writer writing...")  # Simulate writer writing
                time.sleep(1)
                print("Writer finished writing.")  # Indicate that writing is finished
                writer_active = False  # Reset writer active flag
            else:
                print("No writer is currently active. Cannot write.")  # Notify user that writing is not possible
        elif choice == "5":  # If the user chooses to quit
            break  # Exit the loop
        else:
            print("Invalid choice. Please enter again.")  # Notify user of invalid choice

    # Join all threads
    for thread in threads:
        thread.join()  # Wait for all threads to finish
