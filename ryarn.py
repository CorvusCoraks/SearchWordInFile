from typing import Any
from ayarn import AYarn, AQueuePull, Direction, OneQueue
# import asyncio
from queue import Queue


class YarnQueue(AQueuePull):
    def __init__(self):
        self._queues: dict[str, OneQueue] = {}

    def add_queue(self, queue_name: str, direction: Direction, datatype: type) -> None:
        self._queues[queue_name] = OneQueue(direction=direction, datatype=datatype, queue=Queue())

    def get_queue(self, queue_name: str) -> tuple[Queue, Direction, type]:
        return self._queues[queue_name].queue, self._queues[queue_name].direction, self._queues[queue_name].datatype

    def send(self, queue_name: str, data: Any) -> None:
        if isinstance(data, self._queues[queue_name].datatype):
            self._queues[queue_name].queue.put(data)
        else:
            raise TypeError(f"Type of argument 'data' ({type(data)}) "
                            f"mismatch expected type ({self._queues[queue_name].datatype}) "
                            f"for sending through queue '{queue_name}'.")

    def receive(self, queue_name: str) -> Any:
        return self._queues[queue_name].queue.get()


class YarnRealisation(AYarn):
    async def async_run(self):
        pass
