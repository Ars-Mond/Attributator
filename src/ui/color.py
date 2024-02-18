
class Color:
    # hex: int
    def __init__(self, hex_value: str | int):
        if isinstance(hex_value, str):
            hex_value = hex_value.replace('#', '')
            if len(hex_value) <= 3:
                v = int(hex_value, 16)

                r = v >> (2 * 4) & 0xf
                g = v >> (1 * 4) & 0xf
                b = v >> (0 * 4) & 0xf

                r = ((r << 4) + r) << (3 * 8)
                g = ((g << 4) + g) << (2 * 8)
                b = ((b << 4) + b) << (1 * 8)
                a = 0xff

                self._hex = r + g + b + a

            elif len(hex_value) <= 6:
                self._hex = (int(hex_value, 16) << 8) + 0xff
            elif len(hex_value) <= 8:
                self._hex = int(hex_value, 16)
            else:
                raise Exception()

        elif isinstance(hex_value, int):
            self._hex = hex_value

        else:
            raise Exception()

    def get_RGBA(self) -> tuple[int, int, int, int]:
        r = self._hex >> (3 * 8) & 0xff
        g = self._hex >> (2 * 8) & 0xff
        b = self._hex >> (1 * 8) & 0xff
        a = self._hex >> (0 * 8) & 0xff
        return r, g, b, a

    def get_RGB(self) -> tuple[int, int, int]:
        r, g, b, a = self.get_RGBA()
        return r, g, b

    def get_normalize_RGBA(self) -> tuple[float, float, float, float]:
        r, g, b, a = self.get_RGBA()
        r = Color.clamp(r / 0xff, 0.0, 1.0)
        g = Color.clamp(g / 0xff, 0.0, 1.0)
        b = Color.clamp(b / 0xff, 0.0, 1.0)
        a = Color.clamp(a / 0xff, 0.0, 1.0)
        return r, g, b, a

    def get_normalize_RGB(self) -> tuple[float, float, float]:
        r, g, b, a = self.get_normalize_RGBA()
        return r, g, b

    def __get_HSV(self) -> tuple[int, int, int]:
        r, g, b = self.get_normalize_RGB()
        max_color = max(r, g, b)
        min_color = min(r, g, b)

        v = max_color

        if max_color == min_color:
            return 0, 0, v

        s = (max_color - min_color) / max_color

        if max_color == r:
            h = (g - b) / (max_color - min_color)
        elif max_color == g:
            h = 2 + (b - r) / (max_color - min_color)
        else:
            h = 4 + (r - g) / (max_color - min_color)

        h *= 60
        s *= 100
        v *= 100

        if h < 0:
            h += 360

        return h, s, v

    def get_HSV(self):
        h, s, v = self.__get_HSV()
        h = round(h)
        s = round(s)
        v = round(v)
        return h, s, v

    def get_normalize_HSV(self) -> tuple[float, float, float]:
        h, s, v = self.__get_HSV()
        h = h / 360
        s = s / 100
        v = v / 100
        return h, s, v

    def set_RGBA(self, color: tuple[int, int, int, int] | list[int, int, int, int]) -> None:
        if len(color) < 4:
            raise Exception()

        r = color[0] << (3 * 8)
        g = color[1] << (2 * 8)
        b = color[2] << (1 * 8)
        a = color[3] << (0 * 8)

        self._hex = r + g + b + a

    def set_RGB(self, color:  tuple[int, int, int] | list[int, int, int]) -> None:
        if len(color) < 3:
            raise Exception()

        new_color = [color[0], color[1], color[2], 0xff]
        self.set_RGBA(new_color)

    @staticmethod
    def clamp(value, min_val, max_val):
        return max(min_val, min(value, max_val))