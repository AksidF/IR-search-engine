import numpy as np
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.logger import logger


def split_large_np(filename: str, output_dir: str):
    file_path = os.path.join(os.path.dirname(__file__))

    data: np.ndarray = np.load(f"{file_path}/../../{filename}")
    chunk_size = 300  # around 50mb
    num_chunks = len(data) // chunk_size + (1 if len(data) % chunk_size != 0 else 0)
    for i in range(num_chunks):
        chunk = data[i * chunk_size : (i + 1) * chunk_size]
        np.save(f"{file_path}/../../{output_dir}/chunk_{i}.npy", chunk)
        logger.info(f"Saved chunk_{i}.npy")


# split_large_np("compressed/vect_data.npy", "compressed/chunks")


def load_chunk_np(folder_name: str) -> np.ndarray:
    chunks = []
    i = 0
    while os.path.exists(f"{folder_name}/chunk_{i}.npy"):
        chunk = np.load(f"{folder_name}/chunk_{i}.npy")
        chunks.append(chunk)
        i += 1

    # concat
    full_data: np.ndarray = np.concatenate(chunks, axis=0)
    return full_data
