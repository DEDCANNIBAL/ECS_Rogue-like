#cython: language_level=3
from collections import deque
from queue import PriorityQueue
from typing import Deque, Set

from libcpp.vector cimport vector

from components import Position
from utils.vec2i cimport vec2i
from utils.vec2i import vec2i

cdef int MAX_PATH_LENGTH = 2 ** 32

cdef class PathFinder:
    shifts = (vec2i(1, 0),
              vec2i(0, 1),
              vec2i(-1, 0),
              vec2i(0, -1))

    cdef:
        vector[vector[int]] dist
        vec2i start, finish
        vec2i field_size

    def __init__(self, vec2i field_size):
        self.field_size = field_size
        self.queue = PriorityQueue()

    cpdef clear(self):
        self.dist.assign(self.field_size.x,
                         vector[int](self.field_size.y, MAX_PATH_LENGTH))
        self.dist[self.start.x][self.start.y] = 0
        self.queue = PriorityQueue()

    def find_path(self,
                  start: Position,
                  finish: Position,
                  obstacles: Set[Position]) -> Deque[Position]:
        self.start = start
        self.finish = finish
        self.obstacles = obstacles
        self.clear()
        self.queue.put((0, self.start))
        while not self.queue.empty():
            _, current_pos = self.queue.get()
            if current_pos == finish:
                return self.restore_path()
            self.process_adjacent_positions(current_pos)
        return deque()

    cpdef void process_adjacent_positions(self, vec2i current_pos):
        for shift in self.shifts:
            adjacent_pos = current_pos + shift
            if (self.check_position(adjacent_pos)
                    and self.get_dist_value(adjacent_pos)
                    > self.get_dist_value(current_pos) + 1):
                self.dist[adjacent_pos.x][adjacent_pos.y] = self.get_dist_value(current_pos) + 1
                self.queue.put((
                    self.get_dist_value(adjacent_pos) + self.heuristic(adjacent_pos),
                    adjacent_pos))

    cpdef int heuristic(self, vec2i pos):
        return abs(self.finish.x - pos.x) \
               + abs(self.finish.y - pos.y)

    cpdef int get_dist_value(self, pos: Position):
        return self.dist[pos.x][pos.y]

    cpdef int check_position(self, pos: Position):
        return Position(0, 0) <= pos < self.field_size and pos not in self.obstacles

    def restore_path(self) -> Deque[Position]:
        path = deque()
        path.append(self.finish)
        current_pos = self.finish
        while (current_pos != self.start):
            for shift in self.shifts:
                adjacent_pos = current_pos + shift
                if (self.check_position(adjacent_pos)
                        and self.get_dist_value(adjacent_pos) + 1
                        == self.get_dist_value(current_pos)):
                    current_pos = adjacent_pos
                    path.append(adjacent_pos)
        return path
