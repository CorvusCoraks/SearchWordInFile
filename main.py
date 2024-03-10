from logic import Logic

if __name__ == '__main__':

    pass

    Logic.view.set_seek_method(Logic.seek_trigger)

    Logic.view.run_in_main()
    # Your application won't reach here until you exit and the event
    # loop has stopped.
