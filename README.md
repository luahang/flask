本项目实现一个简单的flask图书小程序具体步骤如下：
1. 配置数据库
  a. 导入SQLAlchemy扩展
  b. 创建db对象，并配置参数
  c. 终端创建数据库
2. 添加书籍和作者模型
  a. 模型继承db.Modle
  b. __tablename__:表名
  c. db.Column: 字段
  d. db.relationship: 关系的引用
3. 添加数据
4. 使用模板显示数据库查询出来的数据
  a. 查询所有作者信息，发给模板显示
  b. 模板按照格式，使用for循环作者和书籍（作者获取书籍，用得上关系引用）
5. 使用WTF显示表单
  a. 自定义表单类
  b. 模板中的显示
  c. secret_key / 编码 / form.csrf_token
6. 实现相关的删除逻辑
  a. 删除书籍
  b. 删除作者
  c. url_for的使用 和 for else 的使用/ 页面重定向的使用 redirect
