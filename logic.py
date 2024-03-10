import protocol as p
from Legacy.view import PySide6Realisation
from Legacy.data import Data
from Legacy.wanted import WantedString
from Legacy.seeker import Seeker


class Logic:
    data: p.PSourceData = Data()
    wanted: p.PWanted = WantedString()
    seeker: p.PSeeker = Seeker()
    view: p.AView = PySide6Realisation()

    @classmethod
    def seek_trigger(cls) -> None:
        pass
