import time
# import threading
from abc import ABC, abstractmethod


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

    @abstractmethod
    def init_threads(self):

        # for it in range(self.threads_number):
        #     self.threads.append(threading.Thread())
        # return

        pass

    def is_alive(self):
        return True in [thread.is_alive() for thread in self.threads]

    @abstractmethod
    def run_step(self):
        pass

    @abstractmethod
    def run_interrupt(self):
        pass

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
