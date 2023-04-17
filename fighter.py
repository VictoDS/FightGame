import pygame

class Fighter():
    def __init__(self, x, y, data, sprite_sheet, animation_steps) -> None:
        self.size = data[0]
        self.flip = False
        self.rect = pygame.Rect((x,y,80,180))
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []

        for row, animation in enumerate(animation_steps):
            temp_img_list = []

            for step in range(animation):
                temp_img = sprite_sheet.subsurface(step * self.size, row * self.size, self.size, self.size)
                temp_img_list.append(temp_img)

            animation_list.append(temp_img_list)
    
    def draw(self, surface):
        pygame.draw.rect(surface, (255,0,0), self.rect)

    def move(self, screen_width, screen_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        floor = screen_height - (screen_height / 6)
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()

        if not self.attacking:
            if key[pygame.K_a]:
                dx = -SPEED
            if key[pygame.K_d]:
                dx = SPEED
            if key[pygame.K_w] and not self.jump:
                self.vel_y = -30
                self.jump = True
            
            if key[pygame.K_r] or key[pygame.K_t]:
                self.attack(surface, target)

                if key[pygame.K_r]:
                    self.attack_type = 1
                if key[pygame.K_t]:
                    self.attack_type = 2

        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        elif self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        if self.rect.bottom + dy > floor:
            self.vel_y = 0
            self.jump = False
            dy = floor - self.rect.bottom
        
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
        
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10

        pygame.draw.rect(surface, (0,255,0), attacking_rect)