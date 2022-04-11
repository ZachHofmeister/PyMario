import pygame as pg


class AnimationDict:
    def __init__(self, animations_dict, start_key):
        self.animations_dict = animations_dict
        self.start_key = start_key
        self.animation = animations_dict[start_key]

    def switch_to(self, key):
        old_index = self.animation.index
        self.animation = self.animations_dict[key]
        self.animation.index = old_index if old_index < self.animation.frames - 1 else 0

    def has_key(self, key): return key in self.animations_dict
    def keys(self): return self.animations_dict.keys()
    def is_expired(self): return self.animation.is_expired()
    def reset(self): self.animation.reset()
    def image(self): return self.animation.image()


class Animation:
    def __init__(self, frame_list, start_index=0, delay=100, is_loop=True, scale=None):
        self.frame_list = frame_list
        if scale:
            self.scale_all(scale)
        self.start_index = start_index
        self.delay = delay
        self.is_loop = is_loop
        self.last_time_switched = pg.time.get_ticks()
        self.frames = len(frame_list)
        self.index = start_index if start_index < len(frame_list) - 1 else 0

    def next_frame(self):
        # if a one-pass timer that has finished
        if not self.is_loop and self.index == len(self.frame_list) - 1: return
        now = pg.time.get_ticks()

        if now - self.last_time_switched > self.delay:
            self.index += 1
            if self.is_loop: self.index %= self.frames
            self.last_time_switched = now

    def is_expired(self): return not self.is_loop and self.index == len(self.frame_list) - 1
    def reset(self): self.index = self.start_index

    def scale_all(self, size):
        for i, frame in enumerate(self.frame_list):
            self.frame_list[i] = pg.transform.scale(frame, size)

    def image(self):
        self.next_frame()
        return self.frame_list[self.index]
