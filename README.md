# Multiple Threading in Python

## Introduction

This repository show my implementation Python code using `threading` library to speed up downloading process. This motivation comes from my task at my University's Lab project. This task require me to download hundreds of flies from onedrive. Due to the slow speed of the overall progress, i had to find a new solution to speed up this process and finish the task in time.

## Threading's Problems

When using `threading` library, i have encountered some major problems which is:

- Automatically setup multiple threading with **specific number of threads**.
- Understanding how threading works and how to **manage multiple threadings**.
- How to create a **thread's killing mechanism** that triggered when there is a `KeyboardInterrupt` Exception raised.
- How to apply a **saving json mechanism** that automatically saving the download progress.

## My Solution

I had implemented `multiThreads` module having `MultiThreads` abstract class which provide these features:

- Initialize with `threads_number` and `run_sleep`.

  ```Python
  class MultiThreads(ABC):
      def __init__(
          self,
          threads_number: int = 1,
          debug: bool = False,
          run_sleep: float = 0.5
      ) -> None:

          self.threads = []
          self.threads_number = threads_number

          self.is_interrupt = False
          self.debug = debug

          self.run_sleep = run_sleep
  ```

- Abstract method `init_threads()` which can be specify the `thread_func` (target) and store in to `threads` List.

  ```Python
  @abstractmethod
  def init_threads(self):

    # for it in range(self.threads_number):
    #     self.threads.append(threading.Thread())
    # return

    pass
  ```

- Method `is_alive()` return **True** if there is at least one thread in `threads` is running.

  ```Python
  def is_alive(self):
    return True in [thread.is_alive() for thread in self.threads]
  ```

- Method `run()` starts all the threads and waiting them to finish. Inside this method, i apply two things which is `run_step()` and `run_interrupt()`.

  ```Python
  def run(self):
      for thread in self.threads:
          thread.start()

      try:
          # Running
          while self.is_alive():
              self.run_step()  # Run Step
              time.sleep(self.run_sleep)

      except (KeyboardInterrupt, SystemExit) as e:
          self.run_interrupt()  # Run Interrupt

          if self.debug:
              print(e)

          self.is_interrupt = True
  ```

- Abstract method `run_step()` allows me to implement saving json when all threads are running. This method called the **main running process**.
- Abstract method `run_interrupt()` allows me to implement running function running right after `KeyboardInterrupt` Exception hit.

## References

I had used these references to help me build `MultiThreads` classes and overcome Python `Multi-thread` problems:

- [Multithreading in Python](https://www.geeksforgeeks.org/multithreading-python-set-1/)
- [Abstract Class in Python](https://www.geeksforgeeks.org/abstract-classes-in-python/)
- [_Stackoverflow_ - Cannot kill Python script with Ctrl-C](https://stackoverflow.com/questions/11815947/cannot-kill-python-script-with-ctrl-c)
- [_Stackoverflow_ - How to kill a child thread with Ctrl+C?](https://stackoverflow.com/questions/4136632/how-to-kill-a-child-thread-with-ctrlc)
- [_Stackoverflow_ - Terminate a multi-thread python program](https://stackoverflow.com/questions/1635080/terminate-a-multi-thread-python-program/1635084#1635084)
- [_Stackoverflow_ - How to catch multiple exceptions in one line? (in the "except" block)](https://stackoverflow.com/questions/6470428/how-to-catch-multiple-exceptions-in-one-line-in-the-except-block)
- _[Not referenced but cool - Stackoverflow - Python: passing functions as arguments to initialize the methods of an object. Pythonic or not?](https://stackoverflow.com/questions/55413060/python-passing-functions-as-arguments-to-initialize-the-methods-of-an-object-p)_
