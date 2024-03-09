import protocol as p
from Legacy.view import PySide6Realisation
from Legacy.data import Data
from Legacy.wanted import WantedString
from Legacy.seeker import Seeker


def seek_trigger() -> None:
    pass


if __name__ == '__main__':
    data: p.PSourceData = Data()
    wanted: p.PWanted = WantedString()
    seeker: p.PSeeker = Seeker()
    view: p.AView = PySide6Realisation()

    pass

    view.set_seek_method(seek_trigger)

    view.run_in_main()
    # Your application won't reach here until you exit and the event
    # loop has stopped.
