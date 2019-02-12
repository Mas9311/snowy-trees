import numpy as np


class Tree:
    def __init__(self, config):
        widths = {'t': 151, 'w': 271}  # tall or wide
        speeds = {'u': 0.1, 'a': 0.465000, 'b': 0.7265000, 'c': 0.9810000}
        densities = {'a': 512, 'b': 128, 'c': 36}  # 51.2%, 12.8%, 3.6% chance of snow_char
        tiers = [x for x in range(13, 68, 4)]  # tiers range from [1, 13] (tier * index + 9)

        self.star_char = '★'
        self.leaf_char = '❇'  # ❇ #
        self.snow_char = '*'  # * ❇
        self.base_char = '║'  # │ ║
        self.ornaments = ['●', 'x', '♦']  # ● ♦ x ○ * ★ ⍟ ❤
        if not config[3]:
            self.ornaments = []
        self.tree_tiers = 4  # how many triangles to print on the tree
        self.tree_width = tiers[self.tree_tiers]
        self.screen_width = widths[config[0]]
        self.sleep_time = speeds[config[1]]
        self.max_snow = densities[config[2]]

    def gen_snow(self, snow_len):
        output = ''
        for _ in range(snow_len):
            rand_snow = int(np.random.random_sample() * 1000)
            output += (' ', self.snow_char)[0 <= rand_snow <= 0 + self.max_snow]
        return output

    def tree_topper(self):
        output = self.star_line()
        for leaves_width in range(1, 10, 2):  # 1, 3, 5, 7, 9
            output += self.tree_line(leaves_width)
        return self.gen_snow(self.screen_width) + '\n' + output + self.tree_line(13)

    def tree_shape(self):
        output = ''
        neck = 7
        for _ in range(self.tree_tiers - 1):
            for curr in range(4):
                w = neck + (curr * 4)
                if curr is 0:
                    output += self.tree_line(w, 8)
                elif curr is 1:
                    output += self.tree_line(w, 4)
                else:
                    output += self.tree_line(w)
            neck += 4
        return output

    def tree_base(self):
        output = ''
        base_width = 1 + ((self.tree_tiers // 2) * 2)
        base_width = (base_width, 9)[base_width > 9]
        base_height = (self.tree_tiers - 1, 1)[self.tree_tiers is 1]
        base_height = (base_height, 6)[base_height > 6]
        for _ in range(base_height):
            output += self.make_base(base_width)
        return output + self.gen_snow(self.screen_width)

    def star_line(self):
        spaces_len = ((self.screen_width - 3) // 2)
        return self.gen_snow(spaces_len) + ' ' + self.star_char + ' ' + self.gen_snow(spaces_len) + '\n'

    def tree_line(self, leaves, buffer_len=2):
        buffer = ' ' * (buffer_len // 2)
        leaves_str = self.gen_leaf(leaves)
        spaces_len = (self.screen_width - (buffer_len + leaves)) // 2
        return self.gen_snow(spaces_len) + buffer + leaves_str + buffer + self.gen_snow(spaces_len) + '\n'

    def gen_leaf(self, leaves):
        output = ''
        for _ in range(leaves):
            r = int(np.random.random_sample() * 1000)
            if 500 <= r < 550 and len(self.ornaments) >= 1:     # 5.0% chance of first ornament
                output += self.ornaments[0]
            elif 600 <= r < 635 and len(self.ornaments) >= 2:   # 3.5% chance of second ornament
                output += self.ornaments[1]
            elif 700 <= r < 725 and len(self.ornaments) >= 3:   # 2.5% chance of third ornament
                output += self.ornaments[2]
            elif 800 <= r < 820 and len(self.ornaments) >= 4:   # 2.0% chance of fourth ornament
                output += self.ornaments[3]
            elif 900 <= r < 915 and len(self.ornaments) >= 5:   # 1.5% chance of fifth ornament
                output += self.ornaments[4]
            else:
                output += self.leaf_char
        return output

    def make_base(self, width):
        buffer = ' ' * ((self.tree_width - width - 2) // 2)
        base_str = self.base_char * width
        spaces = (self.screen_width - self.tree_width + 2) // 2
        return self.gen_snow(spaces) + buffer + base_str + buffer + self.gen_snow(spaces) + '\n'

    def __str__(self):
        return (f'{self.tree_topper()}'
                f'{self.tree_shape()}'
                f'{self.tree_base()}')
