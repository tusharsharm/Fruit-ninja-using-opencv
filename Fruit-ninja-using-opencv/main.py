import cv2
import pygame
import random
import numpy as np
import os
from hand_detector import HandDetector
from fruit import Fruit, FruitHalf

# === Constants ===
WIDTH, HEIGHT = 1200, 1000
MAX_MISSES = 3
SPAWN_DELAY = 30
FINGERTIPS = [8, 12, 16, 20]
COMBO_WINDOW = 800  # ms

# === Init ===
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Ninja - Webcam Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 48)

# === Load Assets ===
background = pygame.image.load("./assets/background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT)) # Scale the background
bomb_img = pygame.image.load("./assets/bomb.png")
slice_sound = pygame.mixer.Sound("./sounds/slice.mp3")
bomb_sound = pygame.mixer.Sound("./sounds/explode.mp3")
pygame.mixer.music.load("./sounds/start.mp3")
pygame.mixer.music.play(-1)

# Load fruits dynamically
def load_fruit_assets():
    fruit_names = ["apple", "banana", "peach", "strawberry", "watermelon"]
    fruits = []
    halves = {}
    for name in fruit_names:
        try:
            full = pygame.image.load(f"./assets/{name}.png")
            left = pygame.image.load(f"./assets/{name}-1.png")
            right = pygame.image.load(f"./assets/{name}-2.png")
            fruits.append((name, full))
            halves[name] = (left, right)
        except:
            print(f"⚠️ Skipping fruit '{name}': missing files")
    return fruits, halves

fruits_list, fruit_halves_lookup = load_fruit_assets()

# === Camera ===
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
detector = HandDetector()

# === Game State ===
def reset_game():
    global fruits, score, missed, game_over, paused, menu
    global finger_history, recent_slices, fruit_halves, combo_popup
    fruits = []
    fruit_halves = []
    score = 0
    missed = 0
    game_over = False
    paused = False
    menu = True
    finger_history = []
    recent_slices = []
    combo_popup = None

reset_game()
spawn_timer = 0
trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# === Game Loop ===
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if menu and event.key == pygame.K_SPACE:
                menu = False
            if game_over and event.key == pygame.K_r:
                reset_game()
            if event.key == pygame.K_p:
                paused = not paused

    if menu:
        screen.fill((0, 0, 0))
        title = font.render("Fruit Ninja: Webcam Edition", True, (255, 255, 0))
        tip = font.render("Press SPACE to Start", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - 250, HEIGHT//2 - 50))
        screen.blit(tip, (WIDTH//2 - 200, HEIGHT//2 + 10))
        pygame.display.update()
        continue

    if paused:
        pause_text = font.render("Paused - Press P to Resume", True, (255, 255, 255))
        screen.blit(pause_text, (WIDTH//2 - 250, HEIGHT//2))
        pygame.display.update()
        continue

    # === Webcam ===
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    cv2.imshow("Webcam View", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    hand_landmarks = detector.find_hand(frame, draw=False)
    fingers = [hand_landmarks[i] for i in FINGERTIPS if i < len(hand_landmarks)]

    current_time = pygame.time.get_ticks()
    screen.blit(background, (0, 0))
    trail_surface.fill((0, 0, 0, 25))

    if game_over:
        over_text = font.render("GAME OVER - Press R to Restart", True, (255, 0, 0))
        final_score = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(over_text, (WIDTH//2 - 300, HEIGHT//2 - 50))
        screen.blit(final_score, (WIDTH//2 - 70, HEIGHT//2 + 10))
    else:
        spawn_timer += 1
        if spawn_timer > SPAWN_DELAY:
            spawn_timer = 0
            x = random.randint(100, WIDTH - 100)
            speed = random.randint(6, 12)
            if random.random() < 0.1:
                fruits.append(Fruit(bomb_img, x, -50, speed, is_bomb=True))
            else:
                name, img = random.choice(fruits_list)
                fruits.append(Fruit(img, x, -50, speed))

        for fruit in fruits:
            fruit.update()
            for finger in fingers:
                result = fruit.check_collision(finger)
                if result == 'fruit':
                    score += 1
                    slice_sound.play()
                    recent_slices.append(current_time)
                    if name in fruit_halves_lookup: # Use the 'name' variable directly
                        left_img, right_img = fruit_halves_lookup[name]
                        fruit_halves.append(FruitHalf(left_img, fruit.rect.centerx - 20, fruit.rect.centery, -4, -6, -5))
                        fruit_halves.append(FruitHalf(right_img, fruit.rect.centerx + 20, fruit.rect.centery, 4, -6, 5))
                elif result == 'bomb':
                    bomb_sound.play()
                    game_over = True
            if fruit.rect.y > HEIGHT and fruit.active:
                fruit.active = False
                if not fruit.is_bomb:
                    missed += 1
                    if missed >= MAX_MISSES:
                        game_over = True
            fruit.draw(screen)

        fruits = [f for f in fruits if f.active]
        recent_slices = [t for t in recent_slices if current_time - t < COMBO_WINDOW]
        if len(recent_slices) >= 2:
            score += 3
            combo_popup = current_time
            recent_slices.clear()

        if combo_popup and current_time - combo_popup < 1000:
            combo_text = font.render("+3 COMBO!", True, (255, 0, 255))
            screen.blit(combo_text, (WIDTH//2 - 100, HEIGHT//2 - 150))

        for half in fruit_halves:
            half.update()
            half.draw(screen)
        fruit_halves = [h for h in fruit_halves if h.active]

        for finger in fingers:
            pygame.draw.circle(trail_surface, (0, 255, 0, 180), finger, 12)
        screen.blit(trail_surface, (0, 0))

  # === Webcam Frame ===
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    hand_landmarks = detector.find_hand(frame, draw=True)  # draw=True shows landmarks
    fingers = [hand_landmarks[i] for i in FINGERTIPS if i < len(hand_landmarks)]
    current_time = pygame.time.get_ticks()

    screen.blit(background, (0, 0))
    trail_surface.fill((0, 0, 0, 25))

    if game_over:
        over_text = font.render("GAME OVER - Press R to Restart", True, (255, 0, 0))
        final_score = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(over_text, (WIDTH//2 - 300, HEIGHT//2 - 50))
        screen.blit(final_score, (WIDTH//2 - 70, HEIGHT//2 + 10))
    else:
        spawn_timer += 1
        if spawn_timer > SPAWN_DELAY:
            spawn_timer = 0
            x = random.randint(100, WIDTH - 100)
            speed = random.randint(6, 12)
            if random.random() < 0.1:
                fruits.append(Fruit(bomb_img, x, -50, speed, is_bomb=True))
            else:
                name, img = random.choice(fruits_list)
                fruits.append(Fruit(img, x, -50, speed, name=name))

        for fruit in fruits:
            fruit.update()
            for finger in fingers:
                result = fruit.check_collision(finger)
                if result == 'fruit':
                    score += 1
                    slice_sound.play()
                    recent_slices.append(current_time)
                    if fruit.name in fruit_halves_lookup:
                        left_img, right_img = fruit_halves_lookup[fruit.name]
                        fruit_halves.append(FruitHalf(left_img, fruit.rect.centerx - 20, fruit.rect.centery, -4, -6, -5))
                        fruit_halves.append(FruitHalf(right_img, fruit.rect.centerx + 20, fruit.rect.centery, 4, -6, 5))
                elif result == 'bomb':
                    bomb_sound.play()
                    game_over = True
            if fruit.rect.y > HEIGHT and fruit.active:
                fruit.active = False
                if not fruit.is_bomb:
                    missed += 1
                    if missed >= MAX_MISSES:
                        game_over = True
            fruit.draw(screen)

        fruits = [f for f in fruits if f.active]
        recent_slices = [t for t in recent_slices if current_time - t < COMBO_WINDOW]
        if len(recent_slices) >= 2:
            score += 3
            combo_popup = current_time
            recent_slices.clear()

        if combo_popup and current_time - combo_popup < 1000:
            combo_text = font.render("+3 COMBO!", True, (255, 0, 255))
            screen.blit(combo_text, (WIDTH//2 - 100, HEIGHT//2 - 150))

        for half in fruit_halves:
            half.update()
            half.draw(screen)
        fruit_halves = [h for h in fruit_halves if h.active]

        for finger in fingers:
            pygame.draw.circle(trail_surface, (0, 255, 0, 180), finger, 12)
        screen.blit(trail_surface, (0, 0))

        # === Webcam preview HUD ===
        frame_small = cv2.resize(frame, (300, 225))
        frame_rgb = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))
        screen.blit(frame_surface, (WIDTH - 320, 20))
        pygame.draw.rect(screen, (255, 255, 255), (WIDTH - 320, 20, 300, 225), 2)
        screen.blit(font.render("You", True, (255, 255, 255)), (WIDTH - 320, 250))

        text = font.render(f"Score: {score}  Missed: {missed}/{MAX_MISSES}", True, (255, 255, 255))
        screen.blit(text, (20, 20))

    pygame.display.update()
    clock.tick(30)


cap.release()
pygame.quit()
