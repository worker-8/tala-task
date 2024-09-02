class Zero:
    def __init__(self):
        self.value = 0

    def __eq__(self, o: object, /) -> bool:
        return isinstance(o, Zero)


class Null:
    def __init__(self):
        self.value = None

    def __eq__(self, o: object, /) -> bool:
        return isinstance(o, Null)


class Empty:
    def __init__(self):
        self.value = ""

    def __eq__(self, o: object, /) -> bool:
        return isinstance(o, Empty)
