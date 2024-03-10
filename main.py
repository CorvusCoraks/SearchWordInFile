from logic import Logic
from ryarn import YarnRealisation, YarnQueue
from ayarn import AQueuePull, AYarn, Direction, APP_FIN_QUEUE_NAME
from queue import Queue

queues: AQueuePull = YarnQueue()
queues.add_queue('selected', Direction.FROM_THREAD, str)
queues.add_queue(APP_FIN_QUEUE_NAME, Direction.TO_THREAD, bool)

thread: AYarn = YarnRealisation(queues)


if __name__ == '__main__':
    thread.run()

    Logic.run_in_main()

    Logic.view.run_in_main()
    # Your application won't reach here until you exit and the event
    # loop has stopped.

