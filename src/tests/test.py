import threading
from tqdm import tqdm
import time


def downloadFile(position, file_id, length):
    fi_bar = tqdm(total=1, ncols=80, position=position, leave=False)
    fi_bar.set_description(f"Downloading {file_id}")
    time.sleep(length)
    fi_bar.update()

    fi_bar.set_description(f"Downloaded {file_id}")
    time.sleep(1)
    return


if __name__ == "__main__":
    file_ids = range(40)
    length = 5
    threads = 5

    for index in range(len(file_ids)//threads):
        t = []
        for it in range(threads):
            t.append(threading.Thread(target=downloadFile, args=(
                it, file_ids[index*threads] + it, length + it)))

        for it in range(threads):
            t[it].start()

        for it in range(threads):
            t[it].join()
