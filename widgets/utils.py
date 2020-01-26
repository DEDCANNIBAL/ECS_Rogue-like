from contextlib import contextmanager

import imgui


@contextmanager
def indent(width):
    try:
        yield imgui.indent(width)
    finally:
        imgui.unindent(width)
