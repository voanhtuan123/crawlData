set = ['* Xylocaine jelly được chỉ định để gây tê bề mặt và bôi trơn:',
 '- Niệu đạo nam giới và nữ giới trong soi bàng quang, đặt catheter, thăm dò bằng ống thông và các thủ thuật khác ở niệu đạo.',
 '- Khoang mũi và họng trong các thủ thuật nội soi như soi dạ dày và soi phế quản.',
 '- Trong soi hậu môn và trực tràng.',
 '- Đặt nội khí quản.',
 '* Điều trị triệu chứng đau do viêm bàng quang và viêm niệu đạo. Giảm đau sau khi cắt bao quy đầu ở trẻ em.']


# def clean_text(set):
#     full_text = []
#     for i in set:
#         parts = i.strip('-')
#         print(parts)
#         full_text.append(parts)
        
#         return full_text

# print(clean_text(set))

# for i in set:
#     parts = i.strip('-')
#     full_text = '\n'.join(parts)
# print(full_text)

def clean_text(items):
        if not items:
            return None
        cleaned = [text.strip() for text in items if text.strip()]
        return "\n".join(cleaned) if cleaned else None

print(clean_text(set))