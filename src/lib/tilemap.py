import pygame
import pytmx

class TiledMap:
    """A class to load and render a Tiled map."""

    def __init__(self, filename: str):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tile_width = tm.tilewidth
        self.tile_height = tm.tileheight
        self.tmxdata = tm

    def render(self, surface: pygame.Surface):
        """Render the map to the surface."""
        for layer in self.tmxdata.layers:
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    pos = x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight
                    if surf:
                        surface.blit(surf, pos)

    def get_rects_in_layer(self, layer: str):
        """Get a list of rects for a given layer."""
        rects = []
        for x, y, surf in self.tmxdata.get_layer_by_name(layer).tiles():
            pos = x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight
            if surf:
                rects.append(pygame.Rect(pos, surf.get_size()))
        return rects
