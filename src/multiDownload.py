import os
import time
import json
import random
import threading
from tqdm import tqdm
from typing import List, Dict
from datetime import datetime
from multiThreads import MultiThreads


def downloadFile(fi_bar, file: Dict, folder: str = 'data'):

    for _ in range(file['length']*10):
        time.sleep(0.1)
        fi_bar.update(1)

    with open(os.path.join(folder, file['name']), "a") as fileHandler:
        fileHandler.write(
            f"Content of {file['name']} file with id = {file['id']}.")

    return


class MultiDownloadFiles(MultiThreads):
    def __init__(self, files_number: int, files: List[Dict], logs: Dict, logs_path: str, threads_number: int = 1, debug: bool = False, run_sleep: float = 0.5) -> None:
        super().__init__(threads_number, debug, run_sleep)

        # Files
        self.files_number = files_number
        self.files = files

        # Logs
        self.logs = logs
        self.logs_path = logs_path

        self.total_bar = tqdm(total=self.files_number,
                              ncols=120, position=0, leave=True)
        self. total_bar.set_description(
            f"[{self.threads_number} threads] - Downloading {self.files_number} Files")

        # Logs saving mechanism - every <logs_run> run_step
        self.logs_step = 0
        self.logs_run = 10

    def dowwloadThread(self, position: int, files: List[Dict], thread_it: int):
        index = 0
        while (self.threads_number * index + thread_it < self.files_number) and (not self.is_interrupt):
            idx = self.threads_number * index + thread_it

            if self.logs[files[idx]['name']] == 'downloaded':
                self.total_bar.update()
                index += 1
                continue

            fi_bar = tqdm(total=files[idx]['length']*10, ncols=115,
                          position=position, leave=False)
            fi_bar.set_description(
                f"  +-[Thread {position}] - Downloading {files[idx]['name']}")

            # Main download func
            downloadFile(fi_bar, files[idx])

            fi_bar.set_description(
                f"  +-[Thread {position}] - Downloaded {files[idx]['name']}")

            self.logs[files[idx]['name']] = 'downloaded'

            self.total_bar.update()
            index += 1
        return

    # overriding abstract method
    def init_threads(self):
        for it in range(self.threads_number):
            self.threads.append(threading.Thread(
                target=self.dowwloadThread,
                args=(it+1, self.files, it),
                daemon=True
            ))
        return

    # overriding abstract method
    def run_step(self):
        if self.logs_step % self.logs_run == 0:
            save_json(self.logs, self.logs_path)
        return

    # overriding abstract method
    def run_interrupt(self):
        os.system('cls')


def generateFiles(min_length, max_length, files_number):
    files = []

    for idx in range(files_number):
        files.append({
            'id': idx,
            'name': f"FI_{idx:04d}.txt",
            'length': random.randint(min_length, max_length)
        })

    return files


def save_json(data, file_name, folder: str = ''):
    # Save json file
    with open(os.path.join(folder, file_name), "w", encoding="utf-8") as output_file:
        json.dump(data, output_file, ensure_ascii=False)


if __name__ == "__main__":
    # Files reading
    files_path = 'data/files.json'

    if not os.path.exists(files_path):
        random.seed(datetime.now().timestamp())
        min_length = 2
        max_length = 6

        files_number = 69
        files = generateFiles(min_length, max_length, files_number)

        if not os.path.exists(os.path.dirname(files_path)):
            os.makedirs(os.path.dirname(files_path))
        save_json(files, files_path)

    files = json.load(open(files_path, encoding="utf-8"))
    files_number = len(files)

    # Logs reading
    logs_path = 'logs/download_log.json'

    if not os.path.exists(logs_path):
        logs = {}
        for file in files:
            logs[file['name']] = 'not download'

        if not os.path.exists(os.path.dirname(logs_path)):
            os.makedirs(os.path.dirname(logs_path))
        save_json(logs, logs_path)

    logs = json.load(open(logs_path, encoding="utf-8"))

    # Multi threading Download files
    multiDownloadFiles = MultiDownloadFiles(
        files_number, files,
        logs, logs_path,
        threads_number=5)

    multiDownloadFiles.init_threads()

    multiDownloadFiles.run()

    # Saving logs the last time
    save_json(logs, logs_path)
