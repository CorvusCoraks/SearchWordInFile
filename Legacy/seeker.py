from protocol import PSeeker, PWanted, PSourceData


class Seeker(PSeeker):
    def seek(self, wanted: PWanted, data: PSourceData) -> bool:
        if data.get_source_data.find(wanted) > 0:
            return True
        else:
            return False
