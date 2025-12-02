Tóm tắt dự án Alien Invasion và các chức năng đã hoàn thiện:

1. Giới thiệu dự án

Alien Invasion là game bắn súng không gian sử dụng Python và thư viện pygame.
Người chơi điều khiển tàu vũ trụ, tiêu diệt các alien, vượt qua nhiều level với độ khó tăng dần. 2. Các chức năng chính

Chọn skin: Người chơi có thể chọn skin cho tàu, alien, đạn và background ngay tại menu.
Chọn chế độ chơi: Có 3 chế độ: Classic (cơ bản), Endless (không giới hạn level), Boss Rush (chỉ đấu boss).
Tùy chỉnh điều khiển: Menu cho phép đổi phím di chuyển, bắn, thoát; lưu cấu hình vào file control_config.txt.
Power-up: Alien ngẫu nhiên rơi vật phẩm, nhận vật phẩm sẽ tăng tốc, bắn nhiều đạn, hồi máu.
Bảng xếp hạng: Lưu nhiều người chơi, điểm số vào ranking.txt, hiển thị top 5 ở menu. Khi game over, người chơi nhập tên để lưu điểm.
Hiệu ứng & âm thanh: Có hiệu ứng nổ, âm thanh bắn và nổ.
Hướng dẫn chơi: Menu có mục hướng dẫn chi tiết cách chơi, điều khiển, power-up, bảng xếp hạng.
Level & độ khó: Qua mỗi level, số lượng alien tăng, tốc độ tăng, skin và background thay đổi.
Game over: Hiển thị điểm, high score, cho phép nhập tên, chọn chơi lại hoặc về menu. 3. Cấu trúc file

alien_invasion.py: Toàn bộ logic game, menu, sự kiện, vẽ màn hình, xử lý chức năng.
settings.py: Lưu cấu hình game, tốc độ, phím điều khiển, hàm tăng tốc độ.
powerup.py: Định nghĩa class PowerUp cho vật phẩm rơi.
Các file khác: ship.py, bullet.py, alien.py, hình ảnh, âm thanh, ranking.txt, control_config.txt. 4. Trải nghiệm người chơi

Tùy chỉnh mọi thứ từ menu: skin, chế độ chơi, phím điều khiển.
Chơi nhiều chế độ, thử thách với boss, endless.
Nhận vật phẩm tăng sức mạnh, cạnh tranh điểm số với nhiều người chơi.
Giao diện trực quan, dễ sử dụng, có hướng dẫn chi tiết.

Dưới đây là chi tiết từng chức năng của dự án Alien Invasion:

1. Chọn skin (tàu, alien, đạn, background)
   Tại menu, người chơi có thể chọn skin cho tàu, alien, đạn và hình nền bằng cách click chuột vào hình ảnh tương ứng.
   Skin được áp dụng ngay khi bắt đầu game.
2. Chọn chế độ chơi (Classic, Endless, Boss Rush)
   Menu có mục chọn chế độ chơi bằng phím ← →.
   Classic: Chơi qua từng level, mỗi level tăng độ khó, có boss ở level chia hết cho 5.
   Endless: Alien xuất hiện liên tục, không giới hạn level, không tăng level.
   Boss Rush: Mỗi level chỉ xuất hiện boss, thử thách liên tục.
3. Tùy chỉnh điều khiển
   Menu cho phép đổi phím di chuyển phải/trái, bắn, thoát bằng cách nhấn phím mới (giữ SHIFT/CTRL/ALT để chọn loại phím).
   Cấu hình phím được lưu vào file control_config.txt, tự động tải lại khi khởi động game.
4. Power-up
   Khi tiêu diệt alien, có xác suất rơi vật phẩm (power-up).
   Có 3 loại: tăng tốc tàu (speed), bắn nhiều đạn (multi_bullet), hồi máu (heal).
   Khi nhận vật phẩm, hiệu ứng được áp dụng ngay cho tàu.
5. Bảng xếp hạng
   Khi game over, người chơi nhập tên để lưu điểm.
   Điểm và tên được lưu vào ranking.txt, hiển thị top 5 ở menu.
   Nếu điểm cao hơn high score, sẽ cập nhật high score.
6. Hiệu ứng & âm thanh
   Khi bắn hoặc tiêu diệt alien, có hiệu ứng nổ và âm thanh.
   Âm thanh được load từ thư mục sounds, hiệu ứng nổ là vẽ hình tròn màu cam.
7. Hướng dẫn chơi
   Menu có mục hướng dẫn, hiển thị chi tiết cách chơi, điều khiển, power-up, bảng xếp hạng.
   Người chơi có thể xem hướng dẫn bất cứ lúc nào từ menu.
8. Level & độ khó
   Qua mỗi level, số lượng alien tăng, tốc độ tăng, skin và background thay đổi.
   Level chia hết cho 5 sẽ xuất hiện boss.
9. Game over & nhập tên
   Khi hết mạng, màn hình game over hiển thị điểm, high score, cho phép nhập tên, chọn chơi lại hoặc về menu.
