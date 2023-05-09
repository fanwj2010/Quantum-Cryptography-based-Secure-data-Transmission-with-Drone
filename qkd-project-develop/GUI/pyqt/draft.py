import sys

from PyQt5.QtWidgets import QApplication, QTreeView, QDirModel

app = QApplication(sys.argv)
model = QDirModel()
tree = QTreeView()
tree.setModel(model)
# 重新定义窗口的大小
tree.resize(600, 400)
tree.show()
sys.exit(app.exec_())