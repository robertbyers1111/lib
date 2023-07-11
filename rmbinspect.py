#!/bin/env python3
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
My library to perform a very basic inspection of an object's properties and methods.

Example..

    import rmbinspect as insp

    insp.show_callables(int)
    insp.show_noncallables(int)

    callables = insp.callables(int)
    noncallables = insp.noncallables(int)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


def everything(obj):
    return (sorted([x for x in dir(obj)]))


def callables(obj):
    return(sorted([x for x in dir(obj) if callable(getattr(obj,x))]))


def noncallables(obj):
    return(sorted(set(everything(obj)) - set(callables(obj))))


def show_callables(obj):
    print("\ncallables...")
    for x in callables(obj):
        print(f"    {x}")


def show_noncallables(obj):
    print("\nnon-callables...")
    for x in noncallables(obj):
        y = getattr(obj,x)
        print(f"    {x}: {y}")


def show_docstring(obj):
    for line in obj.__doc__.split('\n'):
        print(line)


if __name__ == '__main__':
    show_callables(str)
    show_noncallables(str)

