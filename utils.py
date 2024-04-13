from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import textwrap
# from langchain_community.utilities import wikipediaAPIWrapper


def generate_script(subject, video_length,
                    creativity, api_key):
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")
        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """你是一位短视频频道博主，根据以下标题和相关信息，为短视频频道
             写一个视频脚本。
             视频标题：{title}，视频时长：{duration}，生成的脚本长度尽量
             遵循视频时长的要求。
             要求开头抓住眼球，中间提供干货内容，结尾有惊喜，脚本格式也请按照
             【开头、中间、结尾】分隔。
             整体内容的表达方式尽量要轻松有趣，吸引年轻人。
             请确保所有输入内容均为中文。
             开头、中间、结尾均分段，如：
                '''
                【开头】...
                【中间】...
                【结尾】...
                '''
             """)
        ]
    )

    model = ChatOpenAI(temperature=creativity,
                       model_name="gpt-3.5-turbo",
                       openai_api_key=api_key,
                       openai_api_base="https://api.aigc369.com/v1")

    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({"subject": subject}).content

    # search = wikipediaAPIWrapper(lang="zh", api_key=api_key)
    # search_result = search.run(subject)

    script = script_chain.invoke({"title": title, "duration": video_length}).content

    return script, title

#
# script, title = generate_script("说点什么好呢", 5, 0.5, "sk-cEEMuWBgiFCWokdv6e828850D186460dAbBf0fCf367fE4C1")
#
# # 使用 textwrap.fill() 对脚本内容进行自动换行
# wrapped_script = textwrap.fill(script, width=50)  # 示例中设定每行最大宽度为80字符
#
# print("Title:", title)
# print("\nScript:")
# print(wrapped_script)