# This file is part of the LLM CLI.
# The LLM CLI is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# The LLM CLI is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with the LLM CLI. If not, see <https://www.gnu.org/licenses/>.
from enum import Enum


class AutoName(Enum):
    """Each Enum item has a value that is the same as its name.
    每个 Enum 项的值与它的名称相同。"""
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name
