# 读取照片
import cv2

path = "design.png"
Pic = cv2.imread(path, cv2.IMREAD_COLOR)
cv2.imshow("image", Pic)
cv2.waitKey(0)
# 显示原有图片,
# 加密图片
# 显示加密图片
