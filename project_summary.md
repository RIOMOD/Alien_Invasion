# Alien Invasion - Tóm tắt Dự án

## Tổng quan
**Alien Invasion** là một trò chơi bắn súng arcade 2D được phát triển bằng Python sử dụng thư viện `pygame`. Người chơi điều khiển một con tàu ở dưới cùng màn hình và phải bảo vệ chống lại hạm đội người ngoài hành tinh di chuyển từ trên xuống. Mục tiêu là bắn hạ tất cả người ngoài hành tinh trước khi chúng chạm vào người chơi hoặc đáy màn hình.

## Các tính năng chính
- **Điều khiển người chơi**: Di chuyển tàu sang trái và phải bằng các phím mũi tên.
- **Chiến đấu**: Bắn đạn bằng phím Space (Phím cách) để tiêu diệt người ngoài hành tinh.
- **Hạm đội Alien**: Người ngoài hành tinh di chuyển theo đội hình, dịch chuyển xuống và đổi hướng khi chạm vào mép màn hình.
- **Tiến trình**: Tốc độ trò chơi tăng lên mỗi khi một hạm đội bị tiêu diệt, làm cho trò chơi khó dần.
- **Ghi điểm**: Điểm số được cộng khi tiêu diệt người ngoài hành tinh.
- **Mạng chơi**: Người chơi có 3 mạng (tàu). Trò chơi kết thúc khi mất hết mạng.

## Cấu trúc tệp
Dự án bao gồm các tệp Python chính sau:

| Tệp | Mô tả |
|------|-------------|
| `alien_invasion.py` | **Điểm bắt đầu chính**. Chứa lớp `AlienInvasion` quản lý vòng lặp trò chơi, xử lý sự kiện và logic chung. |
| `settings.py` | Chứa lớp `Settings`, lưu trữ tất cả các cấu hình trò chơi (kích thước màn hình, tốc độ, màu sắc, v.v.). |
| `ship.py` | Định nghĩa lớp `Ship`, quản lý di chuyển và hiển thị tàu của người chơi. |
| `alien.py` | Định nghĩa lớp `Alien`, đại diện cho một người ngoài hành tinh trong hạm đội. |
| `bullet.py` | Định nghĩa lớp `Bullet`, quản lý các viên đạn được bắn ra từ tàu. |

## Yêu cầu
- Python 3.x
- Thư viện `pygame`

## Cách chạy
1.  Đảm bảo Python và `pygame` đã được cài đặt.
    ```bash
    pip install pygame
    ```
2.  Chạy tệp trò chơi chính:
    ```bash
    python alien_invasion.py
    ```

## Điều khiển
- **Mũi tên trái**: Di chuyển tàu sang trái
- **Mũi tên phải**: Di chuyển tàu sang phải
- **Space (Phím cách)**: Bắn đạn
- **Q**: Thoát trò chơi
