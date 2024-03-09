from protocol import PSourceData


class Data(PSourceData):
    def get_source_data(self) -> str:
        return "string"
