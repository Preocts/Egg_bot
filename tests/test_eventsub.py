# -*- coding: utf-8 -*-
""" Unit Tests

Author  : Preocts, preocts@preocts.com
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import unittest

from eggbot.eventsub import EventSubs
from eggbot.models.eventtype import EventType


class TestEventSub(unittest.TestCase):
    """ Test Suite """

    def test_create_and_get_events(self):
        """ Manual add and get """
        events_client = EventSubs()
        mockclass = MockClass()

        events_client.add(EventType.MEMBERJOIN, mockclass.method01)
        events_client.add(EventType.DISCONNECT, mockclass.method02)
        events_client.add(EventType.MESSAGE, mockfunc)

        self.assertEqual(
            type(events_client.get(EventType.MEMBERJOIN)[0]), type(mockclass.method01)
        )
        self.assertEqual(
            type(events_client.get(EventType.DISCONNECT)[0]), type(mockclass.method02)
        )
        self.assertEqual(type(events_client.get(EventType.MESSAGE)[0]), type(mockfunc))


class MockClass:
    """ Mock class for mock test """

    def __init__(self) -> None:
        """ Mock """
        self.ran = False

    def method01(self) -> None:
        """ Mock """
        self.ran = True

    def method02(self, arg1: str, arg2: dict) -> bool:
        """ Mock """
        self.ran = True
        return arg1 in arg2


def mockfunc(arg1: str, arg2: dict) -> bool:
    """ Mock """
    return arg1 not in arg2
