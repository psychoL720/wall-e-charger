import pygame
import sys
import time
import math

# -----------------------------
# CONFIGURATION
# -----------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BAR_WIDTH = 500
BAR_HEIGHT = 30
BASE_BAR_HEIGHT = 50  # Bottom bar is thicker than the rest
BAR_SPACING = 18
BACKGROUND_COLOR = (20, 20, 20)
BAR_COLOR = (255, 215, 0)
TEXT_COLOR = (255, 255, 255)
DEBUG_COLOR = (0, 255, 0)

AUDIO_FILE = "/Users/brian/Downloads/MatthewZwartzWall-EDesign/SOUNDS/sfx_solar_charging.mp3"

# Start with rough guesses; refine using debug mode
# Adjust these times while listening to the audio to sync the bars perfectly with the music
# Use the Timestamp feature in the debug overlay to mark exact moments when bars should appear, then update this list accordingly
BAR_TIMES = [1.48, 2.67, 3.35, 3.82, 4.34, 4.90, 5.35, 5.72, 6.09, 6.54]

# -----------------------------
# INITIALIZE
# -----------------------------
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Solar Charge Animation (Dev Mode)")

font = pygame.font.SysFont("Arial", 40)
debug_font = pygame.font.SysFont("Consolas", 20)

# Bars anchored to lower right - x is right-aligned with 40px margin
BAR_X = SCREEN_WIDTH - BAR_WIDTH - 40

# Precompute bar positions (index 0 = bottom/base bar, thicker)
bars = []
# Bottom bar (index 0) starts near the bottom of the screen
start_y = SCREEN_HEIGHT - 60
bars.append(start_y)  # Bottom base bar
for i in range(1, len(BAR_TIMES)):
    y = start_y - BASE_BAR_HEIGHT - BAR_SPACING - (i - 1) * (BAR_HEIGHT + BAR_SPACING)
    bars.append(y)

# -----------------------------
# DRAW FUNCTIONS
# -----------------------------
def draw_background():
    screen.fill(BACKGROUND_COLOR)
    # Title spans full screen width, positioned above the topmost bar
    top_bar_y = bars[-1]  # Topmost bar position
    title = pygame.transform.scale(
        font.render("SOLAR CHARGE LEVEL", True, BAR_COLOR),
        (SCREEN_WIDTH - 40, font.get_height())
    )
    screen.blit(title, (20, top_bar_y - font.get_height() - 30))

def draw_bar(index):
    y = bars[index]
    x = BAR_X
    height = BASE_BAR_HEIGHT if index == 0 else BAR_HEIGHT
    radius = 8  # Subtle rounded corners only
    pygame.draw.rect(screen, BAR_COLOR, (x, y, BAR_WIDTH, height), border_radius=radius)

def draw_sun():
    # Align sun with the topmost bar, to the left of the bars
    top_bar_y = bars[-1]
    sun_x = BAR_X - 140  # Further left to clear the bars
    sun_y = top_bar_y + BAR_HEIGHT + 40  # Lower to clear the title text
    core_radius = 28
    ray_inner = core_radius + 10
    ray_outer = core_radius + 26
    num_rays = 12

    # Draw rays
    for i in range(num_rays):
        angle = math.radians(i * (360 / num_rays))
        x1 = int(sun_x + ray_inner * math.cos(angle))
        y1 = int(sun_y + ray_inner * math.sin(angle))
        x2 = int(sun_x + ray_outer * math.cos(angle))
        y2 = int(sun_y + ray_outer * math.sin(angle))
        pygame.draw.line(screen, BAR_COLOR, (x1, y1), (x2, y2), 7)

    # Draw hollow circle (outline only)
    pygame.draw.circle(screen, BAR_COLOR, (sun_x, sun_y), core_radius, 6)

# -----------------------------
# MAIN LOOP
# -----------------------------
def main():
    pygame.mixer.music.load(AUDIO_FILE)
    pygame.mixer.music.play()

    revealed = 0
    clock = pygame.time.Clock()

    print("=== Debug Mode Active ===")
    print("Press SPACE while listening to mark timestamps.")
    print("Use these timestamps to update BAR_TIMES.\n")

    running = True
    while running:
        audio_time = pygame.mixer.music.get_pos() / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mark timestamps with SPACE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(f"Timestamp marked: {audio_time:.3f}s")

                if event.key == pygame.K_r:
                    print("\nRestarting audio...\n")
                    pygame.mixer.music.stop()
                    pygame.mixer.music.play()
                    revealed = 0

                if event.key == pygame.K_ESCAPE:
                    running = False

        # Reveal bars based on audio timeline
        while revealed < len(BAR_TIMES) and audio_time >= BAR_TIMES[revealed]:
            print(f"Bar {revealed+1} revealed at audio time {audio_time:.3f}s (target {BAR_TIMES[revealed]:.3f}s)")
            revealed += 1

        # Draw everything
        draw_background()
        draw_sun()
        for i in range(revealed):
            draw_bar(i)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

main()
