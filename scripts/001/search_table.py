from typing import Any

class SearchTable[T]:
    def __init__(self, identifier: str) -> None:
        self._identifier = identifier
        self._table: dict[str, T] = {}

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def table(self) -> dict[str, T]:
        return self._table

    def search(self, record: dict[str, Any]) -> T | None:
        key = record.get(self.identifier, None)
        value = self.table.get(str(key), None) if key else None
        return value


def main() -> None:
    dict_table = SearchTable[dict]("dictionary")

    dict_table.table["alpha"] = {'a': 1, 'b': 2}
    dict_table.table["bravo"] = {1: 2, 2: 3}

    alpha = dict_table.search({"dictionary": "alpha"})
    if alpha:
        print("alpha")
        for key, value in alpha.items():
            print(key, value)
    else:
        print("unexpected error: alpha is None")
    bravo = dict_table.search({"dictionary": "bravo"})
    if bravo:
        print("bravo")
        for key, value in bravo.items():
            print(key, value)
    else:
        print("unexpected error: bravo is None")
    charlie = dict_table.search({"dictionary": "charlie"})
    if charlie:
        print("unexpected charlie", str(charlie))
    else:
        print("OK: charlie is none")

if __name__ == "__main__":
    main()
