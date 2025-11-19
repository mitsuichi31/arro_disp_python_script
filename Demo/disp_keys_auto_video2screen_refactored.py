"""
Refactored Image and Video Display Application
Displays images across multiple screens with automatic cycling and video playback support.
"""

import pygame
import os
import subprocess
from typing import List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class DisplayMode(Enum):
    """Display mode enumeration"""
    MANUAL = "manual"
    AUTO = "auto"


@dataclass
class DisplayConfig:
    """Configuration for display settings"""
    width: int = 2160
    height: int = 3840
    switch_interval_ms: int = 5000
    required_displays: int = 2
    vlc_path: str = r'C:\Program Files\VideoLAN\VLC\vlc.exe'


@dataclass
class ImagePaths:
    """Container for image file paths"""
    image_files: List[str]
    special_files: List[str]
    auto_files: List[str]
    video_file: str

    @classmethod
    def default(cls):
        """Create default image paths"""
        return cls(
            image_files=[
                "./images/1.png", "./images/start.png", "./images/2.png",
                "./images/3.png", "./images/4.png", "./images/5.png",
                "./images/6.png", "./images/7.png", "./images/8.png",
                "./images/9.png", "./images/10.png", "./images/stop.png"
            ],
            special_files=[
                "./all/1.png", "./all/2.png", "./all/3.png", "./all/4.png",
                "./all/5.png", "./all/6.png", "./all/7.png"
            ],
            auto_files=[
                "./FCT/welcome.png", "./images/1.png", "./images/2.png",
                "./images/3.png", "./images/4.png", "./images/5.png",
                "./images/6.png", "./images/7.png", "./images/8.png",
                "./images/9.png", "./images/10.png"
            ],
            video_file="./FCT/video.mp4"
        )


class VideoPlayer:
    """Handles video playback using VLC"""

    def __init__(self, vlc_path: str):
        self.vlc_path = vlc_path
        self.process: Optional[subprocess.Popen] = None
        self.is_playing = False

    def play(self, video_path: str) -> bool:
        """
        Start video playback

        Args:
            video_path: Path to video file

        Returns:
            True if playback started successfully, False otherwise
        """
        try:
            self.process = subprocess.Popen([
                self.vlc_path,
                video_path,
                '--fullscreen',
                '--play-and-exit'
            ])
            self.is_playing = True
            print(f"Video playback started: {video_path}")
            return True
        except FileNotFoundError:
            print(f"Error: VLC media player not found at {self.vlc_path}")
            return False
        except Exception as e:
            print(f"Error during video playback: {e}")
            return False

    def update(self) -> bool:
        """
        Check if video is still playing

        Returns:
            True if video is still playing, False if finished
        """
        if self.is_playing and self.process:
            if self.process.poll() is not None:
                self.is_playing = False
                self.process = None
                print("Video playback finished")
                return False
        return self.is_playing

    def stop(self):
        """Stop video playback"""
        if self.process:
            self.process.terminate()
            self.process = None
        self.is_playing = False


class ImageManager:
    """Manages image selection and loading"""

    def __init__(self, image_paths: ImagePaths):
        self.paths = image_paths
        self.current_image_index = 0
        self.current_auto_index = 0
        self.current_special_index = 0
        self.special_image_file = ""
        self.welcome_flag = False

    def get_current_image_path(self, mode: DisplayMode) -> str:
        """
        Get the current image path based on display mode

        Args:
            mode: Current display mode

        Returns:
            Path to the image file to display
        """
        if self.special_image_file:
            return self.special_image_file

        if mode == DisplayMode.AUTO:
            self.current_auto_index %= len(self.paths.auto_files)
            return self.paths.auto_files[self.current_auto_index]
        else:
            self.current_image_index %= len(self.paths.image_files)
            return self.paths.image_files[self.current_image_index]

    def advance_image(self, forward: bool = True):
        """Advance to next/previous image"""
        step = 1 if forward else -1
        self.current_image_index = (self.current_image_index + step) % len(self.paths.image_files)
        self.special_image_file = ""

    def advance_auto(self):
        """Advance to next auto image"""
        self.current_auto_index = (self.current_auto_index + 1) % len(self.paths.auto_files)
        self.special_image_file = ""

    def set_special_image(self, image_path: str):
        """Set a special image to display"""
        self.special_image_file = image_path

    def clear_special_image(self):
        """Clear special image"""
        self.special_image_file = ""

    def cycle_special_all(self):
        """Cycle through special 'all' images"""
        self.special_image_file = self.paths.special_files[self.current_special_index]
        self.current_special_index = (self.current_special_index + 1) % len(self.paths.special_files)

    def toggle_welcome(self):
        """Toggle welcome screen"""
        if self.welcome_flag:
            self.special_image_file = ""
            self.welcome_flag = False
        else:
            self.special_image_file = "./welcome/welcome.png"
            self.welcome_flag = True


class DisplayApplication:
    """Main application class"""

    # Custom event ID for image switching
    IMAGE_SWITCH_EVENT = pygame.USEREVENT + 1

    def __init__(self, config: DisplayConfig, image_paths: ImagePaths):
        self.config = config
        self.image_paths = image_paths
        self.mode = DisplayMode.AUTO
        self.running = False

        # Initialize pygame
        pygame.init()

        # Initialize components
        self.video_player = VideoPlayer(config.vlc_path)
        self.image_manager = ImageManager(image_paths)

        # Setup displays
        self._setup_displays()

    def _setup_displays(self):
        """Initialize and configure displays"""
        num_displays = pygame.display.get_num_displays()

        if num_displays < self.config.required_displays:
            raise RuntimeError(f"At least {self.config.required_displays} displays required")

        # Create main window spanning multiple screens
        width = self.config.width
        height = self.config.height

        self.screen0 = pygame.display.set_mode((width * 3, height))
        self.screen1 = self.screen0.subsurface(pygame.Rect(width, 0, width, height))
        self.screen2 = self.screen0.subsurface(pygame.Rect(width * 2, 0, width, height))

        self.screen_width, self.screen_height = self.screen1.get_size()

        print(f"Displays initialized: {num_displays} displays detected")

    def _start_auto_mode(self):
        """Start automatic image switching"""
        self.mode = DisplayMode.AUTO
        pygame.time.set_timer(self.IMAGE_SWITCH_EVENT, self.config.switch_interval_ms)
        self.image_manager.current_auto_index = 0
        self.image_manager.clear_special_image()
        print("Auto mode enabled")

    def _stop_auto_mode(self):
        """Stop automatic image switching"""
        self.mode = DisplayMode.MANUAL
        pygame.time.set_timer(self.IMAGE_SWITCH_EVENT, 0)
        print("Manual mode enabled")

    def _handle_auto_switch_event(self):
        """Handle automatic image switching event"""
        if self.mode == DisplayMode.AUTO and not self.video_player.is_playing:
            self.image_manager.advance_auto()

    def _handle_keydown(self, key: int):
        """
        Handle keyboard input

        Args:
            key: Pygame key code
        """
        # Ignore input during video playback
        if self.video_player.is_playing:
            return

        # Toggle auto mode (T key)
        if key == pygame.K_t:
            if self.mode == DisplayMode.AUTO:
                self._stop_auto_mode()
            else:
                self._start_auto_mode()
            return

        # Clear special image for non-T keys
        if key != pygame.K_t:
            self.image_manager.clear_special_image()

        # Handle keys only in manual mode
        if self.mode == DisplayMode.MANUAL:
            self._handle_manual_mode_keys(key)

    def _handle_manual_mode_keys(self, key: int):
        """Handle keyboard input in manual mode"""
        if key == pygame.K_SPACE or key == pygame.K_RIGHT:
            self.image_manager.advance_image(forward=True)

        elif key == pygame.K_LEFT:
            self.image_manager.advance_image(forward=False)

        elif key == pygame.K_v:
            self.video_player.play(self.image_paths.video_file)

        elif key == pygame.K_ESCAPE:
            self.running = False

        elif key == pygame.K_s:
            self.image_manager.set_special_image("./zhaodi/start-3.png")

        elif key == pygame.K_e:
            self.image_manager.set_special_image("./zhaodi/stop-3.png")

        elif key == pygame.K_l:
            self.image_manager.set_special_image("./zhaodi/left-3.png")

        elif key == pygame.K_r:
            self.image_manager.set_special_image("./zhaodi/right-3.png")

        elif key == pygame.K_a:
            self.image_manager.cycle_special_all()

        elif key == pygame.K_w:
            self.image_manager.toggle_welcome()

    def _handle_events(self):
        """Process pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == self.IMAGE_SWITCH_EVENT:
                self._handle_auto_switch_event()

            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)

    def _render(self):
        """Render current image to displays"""
        # Get current image path
        image_path = self.image_manager.get_current_image_path(self.mode)

        try:
            # Load and scale image
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (self.screen_width, self.screen_height))

            # Draw to both screens
            self.screen1.blit(image, (0, 0))
            self.screen2.blit(image, (0, 0))

            # Update display
            pygame.display.flip()

        except pygame.error as e:
            print(f"Error loading image {image_path}: {e}")

    def run(self):
        """Main application loop"""
        self.running = True

        # Start in auto mode
        self._start_auto_mode()
        print("Application started in auto mode")

        while self.running:
            # Check video status
            self.video_player.update()

            # Handle events
            self._handle_events()

            # Render current image
            self._render()

        # Cleanup
        self.cleanup()

    def cleanup(self):
        """Cleanup resources"""
        self.video_player.stop()
        pygame.quit()
        print("Application closed")


def main():
    """Application entry point"""
    try:
        config = DisplayConfig()
        image_paths = ImagePaths.default()

        app = DisplayApplication(config, image_paths)
        app.run()

    except Exception as e:
        print(f"Fatal error: {e}")
        pygame.quit()


if __name__ == "__main__":
    main()
