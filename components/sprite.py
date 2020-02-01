from pathlib import Path

from pyglet import resource
from pyglet.graphics import Batch
from pyglet.sprite import Sprite as PygletSprite

from widgets import FormField, ForeignKey

batch = Batch()
PATH_TO_SPRITES = Path('resources')
resource.path.append('@' + str(PATH_TO_SPRITES))


def get_sprite_names():
    return [name for path in PATH_TO_SPRITES.iterdir() if not (name := path.name).startswith('__')]


class Sprite(PygletSprite):

    __form_fields__ = [
        FormField(
            'filename',
            ForeignKey(get_sprite_names())
        )
    ]

    def __init__(self, filename: str):
        texture = resource.texture(filename)
        super().__init__(texture, batch=batch)
