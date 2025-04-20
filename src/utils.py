from enum import Enum


class AutoName(Enum):
    """Each Enum item has a value that is the same as its name.
    每个 Enum 项的值与它的名称相同。"""
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name
