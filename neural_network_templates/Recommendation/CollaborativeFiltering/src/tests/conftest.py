# External libraries
import sys
import pathlib
import pytest

for path in pathlib.Path(__file__).parents:
    x = str(path)
    if x.endswith("src"):
        if x not in sys.path:
            sys.path.insert(0, x)
        break


def pytest_addoption(parser):
    parser.addoption(
        "--validate",
        action="store_true",
        default=False,
        help="validate output resource via live validation service (http)"
    )
