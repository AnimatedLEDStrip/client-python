#  Copyright (c) 2018-2021 AnimatedLEDStrip
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from animatedledstrip.animation_info import AnimationInfo


class NewAnimationGroupInfo:
    """Stores information about a new animation group to create"""

    def __init__(self, group_type: str, group_info: 'AnimationInfo', animation_list: List[str]):
        self.group_type: str = group_type
        self.group_info: 'AnimationInfo' = group_info
        self.animation_list: List[str] = animation_list

    def json_dict(self) -> Dict:
        return {
            "groupType": self.group_type,
            "groupInfo": self.group_info,
            "animationList": self.animation_list,
        }
