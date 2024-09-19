import concurrent.futures as cf
import logging
import queue
import threading

# pylint: disable=undefined-variable
from enum import Enum
from typing import Callable, Dict, Generator, Iterable, List, Type

import pydantic


class DefaultConfig(pydantic.BaseModel):
    class Config:
        extra = "forbid"  # No extra fields allowed
        frozen = True  # Immutable
        slots = True  # Memory efficient


class PoolEnum(str, Enum):
    THREAD = "thread"
    PROCESS = "process"


class Step[T, K](pydantic.BaseModel):
    pool_type: PoolEnum
    pool_size: pydantic.PositiveInt
    task_handler: Callable[[T], K]


class Pipeline[T, K]:
    """
    Using the pool class we want to be able to run pipelines of tasks.
    For example, we may want to run:
    1. Download a file with a pool of 5 threads.
    2. As the files are downloaded, perform some transformation on the downloaded files with a pool of 3 processes
    3. As the files are being processed, perform another transformation to the already transformed files with a pool of 2 processes.

    The workflow only supports a linear dependency between steps where the
    output of one step is the input to the next step.
    """

    def __init__(self, definition: List[Step[T, K]]) -> None:
        self.definition = definition

    def _worker(
        self,
        step: Step[T, K],
        input_queue: queue.Queue[T],
        output_queue: queue.Queue[T],
    ) -> None:
        pool_mapping: Dict[str, Type[cf.Executor]] = {
            "thread": cf.ThreadPoolExecutor,
            "process": cf.ProcessPoolExecutor,
        }
        pool_class = pool_mapping.get(step.pool_type)

        with pool_class(max_workers=step.pool_size) as executor:
            while True:
                task = input_queue.get()
                if task is None:
                    output_queue.put(None)
                    break
                future = executor.submit(step.task_handler, task)
                try:
                    result = future.result()
                    output_queue.put(result)
                except Exception as e:
                    # TODO: maybe handle the exception in a better way
                    # returning a queue of exceptions (or task id, index in data iterable) or something like that
                    logging.warning(
                        "Task %s in Step %s generated the exception: %s", task, step, e
                    )
                finally:
                    input_queue.task_done()

    def run(self, data: Iterable[T]) -> Generator[K, None, None]:
        queues = [queue.Queue() for _ in range(len(self.definition) + 1)]
        threads = []

        # Start worker threads
        for i, step in enumerate(self.definition):
            t = threading.Thread(
                target=self._worker, args=(step, queues[i], queues[i + 1])
            )
            t.start()
            threads.append(t)

        # Populate initial queue
        for item in data:
            queues[0].put(item)
        queues[0].put(None)  # Termination signal

        # Yield results
        while True:
            result = queues[-1].get()
            if result is None:
                break
            yield result

        # Wait for all threads to complete
        for t in threads:
            t.join()


# Example usage:
if __name__ == "__main__":

    def download(url: str) -> bytes:
        # Simulated download
        return f"Downloaded content from {url}".encode()

    def process(data: bytes) -> str:
        # Simulated processing
        return data.decode().upper()

    def transform(data: str) -> int:
        # Simulated transformation
        return len(data)

    pipeline = Pipeline(
        [
            Step(pool_type="thread", pool_size=5, task_handler=download),
            Step(pool_type="process", pool_size=3, task_handler=process),
            Step(pool_type="process", pool_size=2, task_handler=transform),
        ]
    )

    for res in pipeline.run(data=["url1", "url2", "url3"]):
        print(res)
