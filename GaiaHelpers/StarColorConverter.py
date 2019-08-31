import bisect


class StarColorConverter:

    def __init__(self):
        self.colors = []
        self.temp_values = []
        self.generate_colors()

    @staticmethod
    def hex_to_floats(h):
        return [int(h[i:i + 2], 16) / 255. for i in (1, 3, 5)]  # skip '#'

    @staticmethod
    def floats_to_hex(rgb):
        return f'#{int(rgb[0] * 255):02x}{int(rgb[1] * 255):02x}{int(rgb[2] * 255):02x}'

    def generate_colors(self):
        self.colors = sorted([
            (0, "#0000FF"),
            (999999999999, "#FF0000"),
            (113017, '#9bb2ff'),
            (7483, '#eeefff'),
            (5052, '#ffe8ce'),
            (3892, '#ffd29c'),
            (56701, '#9eb5ff'),
            (7218, '#f3f2ff'),
            (4948, '#ffe6ca'),
            (3779, '#ffd096'),
            (33605, '#a3b9ff'),
            (6967, '#f8f6ff'),
            (4849, '#ffe5c6'),
            (3640, '#ffcc8f'),
            (22695, '#aabfff'),
            (6728, '#fef9ff'),
            (4755, '#ffe3c3'),
            (3463, '#ffc885'),
            (16954, '#b2c5ff'),
            (6500, '#fff9fb'),
            (4664, '#ffe2bf'),
            (3234, '#ffc178'),
            (13674, '#bbccff'),
            (6285, '#fff7f5'),
            (4576, '#ffe0bb'),
            (2942, '#ffb765'),
            (11677, '#c4d2ff'),
            (6082, '#fff5ef'),
            (4489, '#ffdfb8'),
            (2579, '#ffa94b'),
            (10395, '#ccd8ff'),
            (5895, '#fff3ea'),
            (4405, '#ffddb4'),
            (2150, '#ff9523'),
            (9531, '#d3ddff'),
            (5722, '#fff1e5'),
            (4322, '#ffdbb0'),
            (1675, '#ff7b00'),
            (8917, '#dae2ff'),
            (5563, '#ffefe0'),
            (4241, '#ffdaad'),
            (1195, '#ff5200'),
            (8455, '#dfe5ff'),
            (5418, '#ffeddb'),
            (4159, '#ffd8a9'),
            (8084, '#e4e9ff'),
            (5286, '#ffebd6'),
            (4076, '#ffd6a5'),
            (7767, '#e9ecff'),
            (5164, '#ffe9d2'),
            (3989, '#ffd5a1'),
        ], key=lambda x: x[0])

        global temp_values
        temp_values, _ = zip(*self.colors)

    def get_color(self, val):
        if len(self.colors) == 0:
            self.generate_colors()

        idx = bisect.bisect(temp_values, val)
        first_color = StarColorConverter.hex_to_floats(self.colors[idx][1])
        if idx + 1 < len(self.colors):
            second_color = StarColorConverter.hex_to_floats(self.colors[idx + 1][1])
        else:
            second_color = first_color

        avg_color = [(first_color[i] + second_color[i]) / 2 for i in range(3)]

        return StarColorConverter.floats_to_hex(avg_color)
