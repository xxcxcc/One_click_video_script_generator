from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field


class Xiaohongshu(BaseModel):
    """
    小红书内容模型，用于定义小红书发布的内容结构。

    属性:
    - titles: 包含小红书五个标题的列表。每个标题应为字符串，且列表长度必须为5。
    - content: 小红书的内容，为字符串。应进行适当的处理以避免过长或包含特殊字符。
    """
    titles: List[str] = Field(description="小红书的五个标题",
                              min_items=5, max_items=5)
    content: str = Field(description="小红书的内容")

    # 在模型实例化时进行数据验证
    def __init__(self, titles: List[str], content: str):
        super().__init__(titles=titles, content=content)
        # 额外的内容长度验证，这里假设最大长度为1000字符
        if len(self.content) > 1000:
            raise ValueError("内容长度超过限制。")


# 示例使用
try:
    # 假设这是用户输入的数据
    data = {
        "titles": ["title1", "title2", "title3", "title4", "title5"],
        "content": "这是小红书的内容"
    }
    xiaohongshu = Xiaohongshu(**data)
    print(f"数据验证通过：{xiaohongshu}")
except ValueError as e:
    # 自定义的错误处理
    print(f"数据错误：{e}")
