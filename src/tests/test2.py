import threading
from tqdm import tqdm
import time
import random
from datetime import datetime

is_interrupt = False


def downloadFile(total_bar, position, file_id, length):
    fi_bar = tqdm(total=length*10, ncols=95,
                  position=position, leave=False)
    fi_bar.set_description(
        f"  +-[Thread {position}] - Downloading file {file_id}")

    for _ in range(length*10):
        time.sleep(0.1)
        fi_bar.update(1)

    fi_bar.set_description(
        f"  +-[Thread {position}] - Downloaded file {file_id}")
    time.sleep(1)

    total_bar.update()
    return


def dowwloadThread(total_bar, position, file, thread_it, thread_total, total_file):
    min_length = 1
    max_length = 5
    index = 0
    while (thread_total * index + thread_it < total_file) and (not is_interrupt):
        idx = thread_total * index + thread_it
        downloadFile(total_bar, position, file[idx], random.randint(
            min_length, max_length) + thread_it)
        index += 1
    return


def is_any_thread_alive(threads):
    return True in [t.is_alive() for t in threads]


if __name__ == "__main__":
    random.seed(datetime.now().timestamp())
    total_file = 23
    file_ids = range(total_file)

    thread_total = 4
    file_cnt = 0

    total_bar = tqdm(total=total_file, ncols=100, position=0, leave=True)
    total_bar.set_description(
        f"[{thread_total} threads] - Downloading {total_file} Files")

    t = []
    for it in range(thread_total):
        t.append(threading.Thread(target=dowwloadThread, args=(
            total_bar, it+1, file_ids, it, thread_total, total_file
        ), daemon=True))

    for it in range(thread_total):
        t[it].start()

    try:
        while is_any_thread_alive(t):
            time.sleep(1)

        # for it in range(thread_total):
        #     t[it].join()

    except KeyboardInterrupt:
        is_interrupt = True
        print("\nInterrupted")
