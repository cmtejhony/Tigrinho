import pygame
import random
import os
import sys
import time
import config as cfg

pygame.init()
screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
pygame.display.set_caption("Jogo do Tigrinho")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont(cfg.FONT_NAME, cfg.FONT_SIZE)
SMALL_FONT = pygame.font.SysFont(cfg.FONT_NAME, cfg.SMALL_FONT_SIZE)

SYMBOLS = list(cfg.PRIZE_MULTIPLIERS.keys())
IMAGES = {
    sym: pygame.image.load(os.path.join(cfg.IMG_PATH, f"{sym}.png"))
    for sym in SYMBOLS
}

def reset_game():
    global balance, bet, slots, game_over, is_spinning, spin_start_time
    balance = cfg.START_BALANCE
    bet = cfg.DEFAULT_BET
    slots = [random.choice(SYMBOLS) for _ in range(3)]
    game_over = False
    is_spinning = False
    spin_star_time = 0

reset_game()

def draw_text(text, x, y, font, color=cfg.BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_button(text, x, y, w, h, color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=8)
    draw_text(text, x + 10, y + 10, SMALL_FONT)
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        if click[0] == 1 and action:
            pygame.time.delay(200)
            action()

def change_bet(amount):
    global bet
    new_bet = bet + amount
    if cfg.MIN_BET <= new_bet <= cfg.MAX_BET:
        bet = new_bet

def start_spin():
    global is spinning, spin_start_time, balance
    if balance >= bet and not is_spinning:
        balance -= bet
        is_spinning = True
        spin_start_time = time.time()

def finish_spin():
    global slots, balance, is_spinning, game_over
    slots = [random.choice(SYMBOLS) for _ in range(3)]
    if slots.count(slots[0]) == 3:
        prize = bet * cfg.PRIZE_MULTIPLIERS[slots[0]]
        
       

running = True
while running:
    screen.fill(cfg.WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i, sym in enumerate(slots):
        img = pygame.transform.scale(IMAGES[sym], (cfg.SLOT_SIZE, cfg.SLOT_SIZE))
        screen.blit(img, (cfg.SLOT_POS_X + i * cfg.SLOT_GAP, cfg.SLOT_POS_Y))

    draw_text(f"Saldo: R$ {balance}", 50, 30, FONT)
    draw_text(f"Aposta: R$ {bet}", 50, 70, FONT)

    if game_over:
        draw_text("Você perdeu tudo!", 300, 140, FONT, cfg.RED)
        draw_button("REINICIAR", 50, 120, 140, 40, cfg.RED, reset_game)
    else:
        draw_button("GIRAR", 50, 120, 100, 40, cfg.GREEN, spin)
        draw_button("+", 160, 120, 40, 40, cfg.GRAY, lambda: change_bet(10))
        draw_button("-", 210, 120, 40, 40, cfg.GRAY, lambda: change_bet(-10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
