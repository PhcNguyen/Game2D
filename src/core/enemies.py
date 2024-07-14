from src.core.settings import *
from src.core.utils import Timer



# Lớp Tooth kế thừa từ pygame.sprite.Sprite, đại diện cho nhân vật răng di chuyển và va chạm
class Tooth(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = Z_LAYERS['main']

        self.direction = choice((-1, 1))  # Hướng di chuyển ban đầu, có thể là -1 hoặc 1
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.speed = 200  # Tốc độ di chuyển

        self.hit_timer = Timer(250)  # Bộ đếm giờ cho va chạm

    def reverse(self):
        if not self.hit_timer.active:
            self.direction *= -1  # Đảo ngược hướng di chuyển
            self.hit_timer.activate()

    def update(self, dt):
        self.hit_timer.update()

        # Hoạt ảnh
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image

        # Di chuyển
        self.rect.x += self.direction * self.speed * dt

        # Đảo ngược hướng nếu va chạm
        floor_rect_right = pygame.Rect(self.rect.bottomright, (1, 1))
        floor_rect_left = pygame.Rect(self.rect.bottomleft, (-1, 1))
        wall_rect = pygame.Rect(self.rect.topleft + vector(-1, 0), (self.rect.width + 2, 1))

        if (floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0) or \
           (floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0) or \
           (wall_rect.collidelist(self.collision_rects) != -1):
            self.direction *= -1

# Lớp Shell kế thừa từ pygame.sprite.Sprite, đại diện cho nhân vật vỏ sò bắn ngọc trai
class Shell(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, reverse, player, create_pearl):
        super().__init__(groups)

        if reverse:
            self.frames = {}
            for key, surfs in frames.items():
                self.frames[key] = [pygame.transform.flip(surf, True, False) for surf in surfs]
            self.bullet_direction = -1
        else:
            self.frames = frames
            self.bullet_direction = 1

        self.frame_index = 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = Z_LAYERS['main']
        self.player = player
        self.shoot_timer = Timer(3000)  # Bộ đếm giờ cho bắn
        self.has_fired = False
        self.create_pearl = create_pearl

    def state_management(self):
        player_pos, shell_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
        player_near = shell_pos.distance_to(player_pos) < 500  # Kiểm tra khoảng cách đến người chơi
        player_front = shell_pos.x < player_pos.x if self.bullet_direction > 0 else shell_pos.x > player_pos.x
        player_level = abs(shell_pos.y - player_pos.y) < 30

        if player_near and player_front and player_level and not self.shoot_timer.active:
            self.state = 'fire'  # Chuyển trạng thái bắn
            self.frame_index = 0
            self.shoot_timer.activate()

    def update(self, dt):
        self.shoot_timer.update()
        self.state_management()

        # Hoạt ảnh / tấn công
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames[self.state]):
            self.image = self.frames[self.state][int(self.frame_index)]

            # Bắn ngọc trai
            if self.state == 'fire' and int(self.frame_index) == 3 and not self.has_fired:
                self.create_pearl(self.rect.center, self.bullet_direction)
                self.has_fired = True

        else:
            self.frame_index = 0
            if self.state == 'fire':
                self.state = 'idle'
                self.has_fired = False

# Lớp Pearl kế thừa từ pygame.sprite.Sprite, đại diện cho ngọc trai được bắn ra từ vỏ sò
class Pearl(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surf, direction, speed):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos + vector(50 * direction, 0))
        self.direction = direction
        self.speed = speed
        self.z = Z_LAYERS['main']
        self.timers = {'lifetime': Timer(5000), 'reverse': Timer(250)}  # Bộ đếm giờ cho thời gian sống và đảo hướng
        self.timers['lifetime'].activate()

    def reverse(self):
        if not self.timers['reverse'].active:
            self.direction *= -1  # Đảo ngược hướng
            self.timers['reverse'].activate()

    def update(self, dt):
        for timer in self.timers.values():
            timer.update()

        self.rect.x += self.direction * self.speed * dt
        if not self.timers['lifetime'].active:
            self.kill()  # Xóa đối tượng ngọc trai khi hết thời gian sống