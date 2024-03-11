from logic import Logic
from ryarn import QueuesPull
from abstractyarn import AbstractQueuesPull, AbstractYarn, Direction, APP_FIN_QUEUE_NAME, Abonents


queues: AbstractQueuesPull = QueuesPull()
queues.add_queue('selected', Direction(Abonents.SEEKER, Abonents.VIEW), str)
queues.add_queue(APP_FIN_QUEUE_NAME, Direction(Abonents.VIEW, Abonents.SEEKER), bool)
queues.add_queue('find_it', Direction(Abonents.VIEW, Abonents.SEEKER), str)


if __name__ == '__main__':
    thread: AbstractYarn = AbstractYarn(queues, Logic.seek_thread_method)
    thread.start()

    Logic.run_in_main()

    Logic.view.run_in_main()
    # Your application won't reach here until you exit and the event
    # loop has stopped.

