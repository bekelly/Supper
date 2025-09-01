from PIL import Image

class Renderer:
    def __init__(self, config):
        self.config = config

    def show_image(self, path):
        img = Image.open(path).rotate(self.config["rotation"], expand=True)
        img.thumbnail((self.config["screen_width"], self.config["screen_height"]), Image.LANCZOS)

        canvas = Image.new("RGB", (self.config["screen_width"], self.config["screen_height"]), (0, 0, 0))
        canvas.paste(img, (0, 0))  # Top-left for now

        def to_rgb565le(r, g, b):
            r5 = (r * 31 + 127) // 255
            g6 = (g * 63 + 127) // 255
            b5 = (b * 31 + 127) // 255
            val = (r5 << 11) | (g6 << 5) | b5
            return val.to_bytes(2, 'little')

        data = bytearray()
        for pixel in canvas.getdata():
            data += to_rgb565le(*pixel)

        with open(self.config["framebuffer"], "wb") as fb:
            fb.write(data)