import pygame
import os


class MusicPlayer:
    def __init__(self, music_dir):
        pygame.mixer.init()
        self.tracks = []
        self.current = 0
        self.playing = False
        self.load_tracks(music_dir)
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 18)

    def load_tracks(self, music_dir):
        if not os.path.exists(music_dir):
            os.makedirs(music_dir)
            return
        for f in sorted(os.listdir(music_dir)):
            if f.endswith(('.mp3', '.wav', '.ogg')):
                self.tracks.append(os.path.join(music_dir, f))

    def play(self):
        if not self.tracks:
            return
        pygame.mixer.music.load(self.tracks[self.current])
        pygame.mixer.music.play()
        self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def next_track(self):
        if not self.tracks:
            return
        self.current = (self.current + 1) % len(self.tracks)
        if self.playing:
            self.play()

    def prev_track(self):
        if not self.tracks:
            return
        self.current = (self.current - 1) % len(self.tracks)
        if self.playing:
            self.play()

    def get_track_name(self):
        if not self.tracks:
            return "No tracks in music/"
        return os.path.basename(self.tracks[self.current])

    def draw(self, screen):
        screen.fill((30, 30, 30))

        title = self.font.render("Music Player", True, (255, 255, 255))
        screen.blit(title, (20, 20))

        track = self.font.render(self.get_track_name(), True, (100, 200, 255))
        screen.blit(track, (20, 80))

        if self.tracks:
            info = self.small_font.render(
                f"Track {self.current + 1}/{len(self.tracks)}", True, (150, 150, 150))
            screen.blit(info, (20, 115))

        status = "Playing" if self.playing else "Stopped"
        color = (0, 255, 0) if self.playing else (255, 80, 80)
        screen.blit(self.font.render(status, True, color), (20, 160))

        controls = ["P - Play", "S - Stop", "N - Next", "B - Previous", "Q - Quit"]
        y = 230
        for line in controls:
            text = self.small_font.render(line, True, (180, 180, 180))
            screen.blit(text, (20, y))
            y += 28
