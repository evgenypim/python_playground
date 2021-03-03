#!/usr/bin/env python3

from dataclasses import dataclass


@dataclass
class Person:
    age: int = 1


class MagicList(list):
    """MagicList class.

    List like class that implements a simplified
    list by skipping boundary checks when possible.
    """

    def __init__(self, cls_type=None):
        if (cls_type is not None) and (not callable(cls_type)):
            raise Exception(f"{cls_type} is not callable")
        self.__cls_type__ = cls_type
        super(self.__class__, self).__init__()

    def __setitem__(self, key, value):
        diff = len(self) - key
        if diff < 0:
            raise IndexError("list index out of range")
        elif diff > 0:
            super(self.__class__, self).__setitem__(key, value)
        elif diff == 0:
            self.append(value)

    def __getitem__(self, key):
        diff = len(self) - key
        if diff != 0:
            return super(self.__class__, self).__getitem__(key)
        elif diff == 0:
            if self.__cls_type__ is not None:
                tmp = self.__cls_type__()
                self.append(tmp)
                return tmp
            else:  # what to do in case cls_type not provided?
                raise IndexError("list index out of range")


if __name__ == "__main__":

    print("Simple assign")
    a = MagicList()
    a[0] = 5
    print(a)

    print("Assign w/ default class")
    a = MagicList(cls_type=Person)
    a[0].age = 5
    print(a)

    print("Boundary check")
    a = MagicList(cls_type=Person)
    try:
        a[1].age = 5
    except IndexError as e:
        print(e)
