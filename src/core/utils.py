from src.core.settings import *

# Lớp Data quản lý thông tin về xu (coins) và sức khỏe (health) của người chơi
class Data:
    def __init__(self, ui):
        self.ui = ui
        self._coins = 0  # Số lượng xu ban đầu
        self._health = 5  # Số lượng máu ban đầu
        self.ui.create_hearts(self._health)  # Tạo các biểu tượng trái tim trên giao diện người dùng

        self.unlocked_level = 0  # Cấp độ đã mở khóa
        self.current_level = 0  # Cấp độ hiện tại

    # Getter và Setter cho thuộc tính coins
    @property
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, value):
        self._coins = value
        if self.coins >= 100:  # Khi số xu đạt 100
            self.coins -= 100  # Trừ đi 100 xu
            self.health += 1  # Tăng một máu
        self.ui.show_coins(self.coins)  # Hiển thị số xu trên giao diện người dùng

    # Getter và Setter cho thuộc tính health
    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
        self.ui.create_hearts(value)  # Cập nhật biểu tượng trái tim trên giao diện người dùng

# Lớp Timer quản lý thời gian đếm ngược và kích hoạt chức năng khi thời gian kết thúc
class Timer:
    def __init__(self, duration, func=None, repeat=False):
        self.duration = duration  # Thời gian đếm ngược
        self.func = func  # Hàm được gọi khi thời gian kết thúc
        self.start_time = 0  # Thời điểm bắt đầu
        self.active = False  # Trạng thái hoạt động của bộ đếm giờ
        self.repeat = repeat  # Xác định có lặp lại hay không

    # Kích hoạt bộ đếm giờ
    def activate(self):
        self.active = True
        self.start_time = get_ticks()  # Lấy thời gian hiện tại

    # Hủy kích hoạt bộ đếm giờ
    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat:  # Nếu cần lặp lại
            self.activate()  # Kích hoạt lại

    # Cập nhật trạng thái bộ đếm giờ
    def update(self):
        current_time = get_ticks()  # Lấy thời gian hiện tại
        if current_time - self.start_time >= self.duration:  # Nếu thời gian đếm ngược đã kết thúc
            if self.func and self.start_time != 0:
                self.func()  # Gọi hàm đã định nghĩa
            self.deactivate()  # Hủy kích hoạt bộ đếm giờ
