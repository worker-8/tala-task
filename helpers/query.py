class _Base:
    def __init__(self):
        self.value = ""

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    def __eq__(self, o: object) -> bool:
        return self.value == str(o)


class Limit(_Base):
    def __call__(self, records: int) -> None:
        if records:
            self.value = f"LIMIT {records}"


class Offset(_Base):
    def __call__(self, offset: int) -> None:
        if offset:
            self.value = f"OFFSET {offset}"
