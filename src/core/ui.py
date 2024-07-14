from src.core.settings import *
from src.core.utils import Timer
from src.core.sprites import AnimatedSprite

class UI:
    def __init__(self, font, frames):
        # Khởi tạo các thuộc tính cần thiết cho giao diện
        self.display_surface = pygame.display.get_surface()  # Lấy bề mặt hiển thị chính
        self.sprites = pygame.sprite.Group()  # Nhóm chứa các sprite
        self.font = font  # Font chữ sử dụng

        # Kiểm tra khung hình trái tim
        if 'heart' in frames and frames['heart']:
            self.heart_frames = frames['heart']  # Lưu trữ khung hình trái tim
            self.heart_surf_width = self.heart_frames[0].get_width()  # Chiều rộng của khung hình
        else:
            raise ValueError("Khung hình trái tim không tồn tại.")  # Lỗi nếu không có khung hình

        self.heart_padding = 6  # Khoảng cách giữa các trái tim
        self.coin_amount = 0  # Số lượng tiền xu ban đầu
        self.coin_timer = Timer(1000)  # Bộ đếm thời gian cho tiền xu

        # Kiểm tra khung hình tiền xu
        if 'coin' in frames and frames['coin']:
            self.coin_surf = frames['coin']  # Lưu trữ khung hình tiền xu
        else:
            raise ValueError("Khung hình tiền xu không tồn tại.")  # Lỗi nếu không có khung hình

    def create_hearts(self, amount):
        # Tạo các trái tim dựa trên số lượng đã chỉ định
        for sprite in self.sprites:
            sprite.kill()  # Xóa tất cả sprite hiện tại
        for heart in range(amount):
            x = 10 + heart * (self.heart_surf_width + self.heart_padding)  # Tính toán vị trí x
            y = 10  # Vị trí y cố định
            Heart((x, y), self.heart_frames, self.sprites)  # Tạo đối tượng Heart

    def display_text(self):
        # Hiển thị số tiền xu trên màn hình
        if self.coin_timer.active:
            text_surf = self.font.render(str(self.coin_amount), False, '#33323d')  # Tạo bề mặt văn bản
            text_rect = text_surf.get_frect(topleft=(16, 34))  # Vị trí văn bản
            self.display_surface.blit(text_surf, text_rect)  # Vẽ văn bản lên bề mặt

            coin_rect = self.coin_surf.get_frect(center=text_rect.bottomleft).move(0, -6)  # Vị trí tiền xu
            self.display_surface.blit(self.coin_surf, coin_rect)  # Vẽ tiền xu lên bề mặt

    def show_coins(self, amount):
        # Cập nhật số lượng tiền xu và kích hoạt bộ đếm thời gian
        self.coin_amount = amount
        self.coin_timer.activate()  # Kích hoạt bộ đếm thời gian

    def update(self, dt):
        # Cập nhật trạng thái của UI
        self.coin_timer.update()  # Cập nhật bộ đếm thời gian
        for sprite in self.sprites:
            if sprite.active:
                sprite.update(dt)  # Cập nhật các sprite đang hoạt động
        self.sprites.draw(self.display_surface)  # Vẽ tất cả các sprite lên bề mặt
        self.display_text()  # Hiển thị văn bản lên màn hình



class Heart(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)  # Khởi tạo lớp cha
        self.active = False  # Trạng thái trái tim

    def animate(self, dt):
        # Phương thức để thực hiện hoạt ảnh cho trái tim
        self.frame_index += ANIMATION_SPEED * dt  # Cập nhật chỉ số khung hình
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]  # Cập nhật hình ảnh
        else:
            self.active = False  # Đặt trạng thái không hoạt động
            self.frame_index = 0  # Đặt lại chỉ số khung hình

    def update(self, dt):
        # Cập nhật trạng thái trái tim
        if self.active:
            self.animate(dt)  # Nếu trái tim đang hoạt động thì thực hiện hoạt ảnh
        else:
            if randint(0, 2000) == 1:
                self.active = True  # Đôi khi kích hoạt trái tim
