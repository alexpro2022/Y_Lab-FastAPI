from typing import Any
from deepdiff import DeepDiff


def compare(left: Any, right: Any) -> None:
    assert isinstance(left, type(right))
    diff = DeepDiff(left, right, exclude_paths='_sa_instance_state')
    assert not diff, diff


def compare_lists(left: list | None, right: list | None) -> None:
    assert left and isinstance(left, list)
    assert right and isinstance(right, list)
    assert len(left) == len(right)
    for i in range(len(left)):
        compare(left[i], right[i])


'''def compare(left, right) -> None:
    def clean(item) -> dict:
        wanted = '_sa_instance_state'
        d = vars(item).copy()
        if wanted in d:
            d.pop(wanted)
        return d

    assert isinstance(left, type(right))
    assert clean(left) == clean(right)
    # diff = DeepDiff(clean(left), clean(right), ignore_order=True)
    # assert not diff, diff '''
