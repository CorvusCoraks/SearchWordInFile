from logic import Logic
from abstractyarn import AbstractYarn


if __name__ == '__main__':
    Logic.run_in_main()

    thread: AbstractYarn = AbstractYarn(Logic.queues_pull, Logic.seek_thread_method)
    thread.start()

    Logic.view.run_in_main()
    # Your application won't reach here until you exit and the event
    # loop has stopped.

