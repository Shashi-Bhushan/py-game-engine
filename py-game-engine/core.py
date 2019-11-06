#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Shashi Bhushan (sbhushan1 @ outlook dot com)'

import abc
from concurrent.futures import ThreadPoolExecutor
import numpy as np


class GameGrid(object):
    """Game Grid Signifies the playable area of the Game.
    It should consist of methods on how to render the playable area and how to update it.
    There should be only one instance of Game Grid in the game.
    """
    def __init__(self, *dimensions, border: bool = True):
        self.row, self.column = dimensions
        self.border = border

        self.game_grid = np.array([[' '] * self.column] * self.row)

        if self.border:
            side_border = [['|'] * 1] * self.row
            vertical_border = ['-'] * (self.column + 2)

            temp_game_grid = np.hstack((side_border, self.game_grid, side_border))
            self.game_grid = np.hstack((vertical_border, temp_game_grid, vertical_border))


class GameEngine(abc.ABC):
    """Game Engine signifies the game loop code.
    It should call the handler object, which would call render and update on all Game object.
    """
    def __init__(self, game_grid_size: int = 2, max_workers: int = 1):
        self.executors = ThreadPoolExecutor(max_workers=max_workers)
        self.game_grid_size = game_grid_size

        self.running = False
        self.game_finished = False

        game_grid = GameGrid(self.game_grid_size)

    def start(self) -> None:
        self.running = True
        self.executors.submit(self.run)

    def run(self):
        """Implements Game Loop"""
        while self.running:
            self.update()
            self.render()

            if self.game_finished:
                break

    @abc.abstractmethod
    def update(self):
        raise NotImplementedError('Please implement update method')

    @abc.abstractmethod
    def render(self):
        raise NotImplementedError('Please implement render method')


if __name__ == '__main__':
    GameEngine()