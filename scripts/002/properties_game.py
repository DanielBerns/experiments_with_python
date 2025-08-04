class Alpha:
    def __init__(self, value: int = 0) -> None:
        self._number: int = value

    @property
    def number(self) -> int:
        return self._number

    @number.setter
    def number(self, value: int) -> None:
        self._number = value


def main() -> None:
    instance = Alpha()
    instance._number = 1 # if this is possible, why to implement number.setter?
    print(instance.number * 2)


if __name__ == "__main__":
    test()
