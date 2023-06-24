import random

from models.post import BoardModel, PostModel
from models.auth import UserModel
from exts import db


def init_board():
    board_names = ['python', 'flask', 'django', '自动化测试', '运维', 'web']
    for index, board_name in enumerate(board_names):
        board = BoardModel(name=board_name, priority=len(board_names) - index)
        db.session.add(board)
    db.session.commit()
    print('版块添加成功')


def create_test_posts():
    boards = list(BoardModel.query.all())
    board_count = len(boards)
    for x in range(99):
        title = f'我是标题{x}'
        content = f'我是内容{x}'
        author = UserModel.query.first()
        index = random.randint(0, board_count - 1)
        board = boards[index]
        post = PostModel(title=title, content=content, author=author, board=board)
        db.session.add(post)
    db.session.commit()
    print('测试帖子创建成功')
