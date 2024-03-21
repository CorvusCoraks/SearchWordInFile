from typing import Any
from abstractyarn import AbstractYarn
from queues import Direction, QueueInPull, AbstractQueuesPull, QueueName, QueuesDataType
# import asyncio
from queue import Queue


class QueuesPull(AbstractQueuesPull):
    def __init__(self):
        self._queues: dict[str, QueueInPull] = {}

    def add_queue(self, queue_name: str, direction: Direction, datatype: type(QueuesDataType)) -> None:
        self._queues[queue_name] = QueueInPull(direction=direction, datatype=datatype, queue=Queue())

    # def get_queue(self, queue_name: str) -> tuple[Queue, Direction, type]:
    #     return self._queues[queue_name].queue, self._queues[queue_name].direction, self._queues[queue_name].datatype

    def send(self, queue_name: str, data: QueuesDataType) -> None:
        if isinstance(data, self._queues[queue_name].datatype):
            self._queues[queue_name].queue.put(data)
        else:
            raise TypeError(f"Type of argument 'data' ({type(data)}) "
                            f"mismatch expected type ({self._queues[queue_name].datatype}) "
                            f"for sending through queue '{queue_name}'.")

    def receive(self, queue_name: str) -> QueuesDataType:
        return self._queues[queue_name].queue.get()

    def is_empty(self, queue_name: str) -> bool:
        return self._queues[queue_name].queue.empty()

    def is_app_fin(self) -> bool:
        return not self.is_empty(QueueName.APP_FIN)

# class YarnRealisation(AbstractYarn):
#     async def async_run(self):
#         for i in range(5):
#             print('async_run')


