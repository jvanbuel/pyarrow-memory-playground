from typing import List
import pyarrow as pa
import tracemalloc
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

NUM_RECORDS = 10_000_000


def log_memory_usage():
    (current, peak) = tracemalloc.get_traced_memory()
    logger.info(
        f"Current memory usage is {current / (1024*1024)}MB; Peak was {peak / (1024*1024)}MB"
    )


def add_to_pa_table(pa_table: pa.Table, my_list: List[str]):
    return (
        pa.concat_tables(
            [pa.Table.from_pydict({"enum_values": my_list}), pyarrow_table]
        )
        if pyarrow_table
        else pa.Table.from_pydict({"enum_values": my_list})
    )


if __name__ == "__main__":
    tracemalloc.start()

    enum_values = ["foo", "bar", "baz"]
    my_list = []
    pyarrow_table = None
    for i in range(NUM_RECORDS):
        my_list.append(enum_values[i % 3])

        if i % 100_000 == 0:
            log_memory_usage()
            pyarrow_table = add_to_pa_table(pyarrow_table, my_list)

            my_list = []

    pyarrow_table = add_to_pa_table(pyarrow_table, my_list)
    log_memory_usage()

    logger.info(f"Number of records: {pyarrow_table.num_rows}")
    logger.info(f"Table size: {pyarrow_table.nbytes/10**6}MB")
