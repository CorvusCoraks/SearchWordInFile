from protocol import PSeeker, PWanted, PSourceData


class Seeker(PSeeker):
    def seek(self, wanted: PWanted, data: PSourceData) -> bool:
        return True
