#!/usr/bin/env python3
import math

LAYER_WIDTH = 25
LAYER_HEIGHT = 6


class Layer:

    def __init__(self):
        self.rows = []

    def add_row(self, row):
        self.rows.append(row)

    def count(self, num):
        count = 0
        for row in self.rows:
            count += row.count(num)
        return count


class Picture:

    def __init__(self):
        self.layers = []
        self.pixels = []

        for h in range(0, LAYER_HEIGHT):
            self.pixels.append([])
            for w in range(0, LAYER_WIDTH):
                self.pixels[h].append('*')

    def add_layer(self, layer):
        self.layers.append(layer)

    def set_pixel(self, h, w):
        for layer in self.layers:
            candidate = layer.rows[h][w]
            if candidate == 0:
                self.pixels[h][w] = ' '
                return
            elif candidate == 1:
                self.pixels[h][w] = '*'
                return

    def set_visible_pixels(self):
        found_current = False
        for h in range(0, LAYER_HEIGHT):
            for w in range(0, LAYER_WIDTH):
                self.set_pixel(h, w)


def read_from_file(filename="input.txt"):
    with open("./{}".format(filename), "r+") as f:
        return [val for val in f.read()]


def parse_data_into_layers(pixels):
    pixels_itr = iter(pixels)
    picture = Picture()
    for i in range(0, int(len(pixels) / (LAYER_HEIGHT * LAYER_WIDTH))):
        layer = Layer()
        for h in range(0, LAYER_HEIGHT):
            row = []
            for w in range(0, LAYER_WIDTH):
                row.append(int(next(pixels_itr)))
            layer.add_row(row)
        picture.add_layer(layer)
    return picture


def main():
    pixels = read_from_file()
    picture = parse_data_into_layers(pixels)

    lowest_zeroes = (None, math.inf)

    for layer in picture.layers:
        count = layer.count(0)
        if count < lowest_zeroes[1]:
            lowest_zeroes = (layer, count)

    print("Answer to Part A: {}".format(lowest_zeroes[0].count(1) * lowest_zeroes[0].count(2)))

    picture.set_visible_pixels()

    print("Answer to Part B: ")
    for i in range(0, 6):
        picture.pixels[i] = ''.join(picture.pixels[i])
    print(picture.pixels)


if __name__ == '__main__':
    main()
