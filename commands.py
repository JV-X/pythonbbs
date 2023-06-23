from models.post import BoardModel
from exts import db


def init_board():
    board_names = ['python', 'flask', 'django', '自动化测试', '运维', 'web']
    for index, board_name in enumerate(board_names):
        board = BoardModel(name=board_name, priority=len(board_names) - index)
        db.session.add(board)
    db.session.commit()
    print('版块添加成功')
