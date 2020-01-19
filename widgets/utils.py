from contextlib import contextmanager

import imgui


@contextmanager
def indent(width):
    imgui.indent(width)
    try:
        yield
    finally:
        imgui.unindent(width)
