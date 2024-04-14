import streamlit as st
from utils import generate_script, generate_xiaohongshu, chat_with_gpt
from langchain.memory import ConversationBufferMemory

st.title("🎬 视频脚本生成器")

with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API秘钥", type="password")
    st.markdown("[若无秘钥，请点此获取](https://api.aigc369.com/register)")

st.divider()

subject = st.text_input("💡 请输入视频脚本主题")

st.divider()

video_video_length = st.number_input("⏱️ 请输入视频长度（单位：分钟）", min_value=0.1,
                                     max_value=10.0, value=5.0, step=0.1)

st.divider()

creativity = st.slider("✨ 请选择创意程度", min_value=0.0, max_value=1.0,
                       value=0.2, step=0.1)

button_script = st.button("🚀 生成脚本", key='key_1')
if button_script:
    if not openai_api_key:
        st.error("请输入OpenAI API秘钥")
        st.stop()
    if not subject:
        st.error("请输入主题")
        st.stop()
    try:
        with st.spinner("⏳ 正在生成脚本..."):
            title, script = generate_script(subject, video_video_length,
                                            creativity, openai_api_key)
            st.subheader("💡 标题：")
            st.write(script)
            st.subheader("💡 视频脚本：")
            st.write(title)
            st.success("✅ 脚本生成成功")
    except Exception as e:
        st.error(f"❌ 脚本生成失败❗️❗️❗")
        st.error(f"错误内容：{e}")

st.divider()

st.title("✨ 爆款小红书 AI 写作助手")

st.divider()

theme = st.text_input("💡 请输入小红书文案主题")
st.divider()
button_xiaohongshu = st.button("🚀 生成文案", key='key_2')
if button_xiaohongshu:
    if not openai_api_key:
        st.error("请输入OpenAI API秘钥")
        st.stop()
    if not theme:
        st.error("请输入主题")
        st.stop()
    try:
        with st.spinner("⏳ 正在生成文案..."):
            result = generate_xiaohongshu(theme, openai_api_key)
            left_column, right_column = st.columns(2)
            with left_column:
                st.markdown("##### 小红书标题1")
                st.write(result.titles[0])
                st.markdown("##### 小红书标题2")
                st.write(result.titles[1])
                st.markdown("##### 小红书标题3")
                st.write(result.titles[2])
                st.markdown("##### 小红书标题4")
                st.write(result.titles[3])
                st.markdown("##### 小红书标题5")
                st.write(result.titles[4])
            with right_column:
                st.markdown("##### 小红书内容正文")
                st.write(result.content)
            st.success("✅ 文案生成成功")
    except Exception as e:
        st.error(f"✖️文案生成失败❗️❗️❗️")
        st.error(f"错误内容：{e}")

st.divider()

st.title("💬 聊天机器人")

# 检查当前会话状态中是否存在名为memory'的键。若不存在，则初始化一个`ConversationBufferMemory`实例，
# 并将其存储在会话状态中，同时设置其`return_messages`参数为True，表示在查询对话记录时返回所有消息。
# 同时初始化一个包含一条AI欢迎消息的字典列表，存储在会话状态的'messages'键下。
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    st.session_state["messages"] = [{"role": "ai",
                                     "content": "我是您的AI聊天助手，请问有什么可以帮您？"}]


# 遍历会话状态中存储的对话消息，为每条消息创建一个对应角色的聊天消息框，并写入消息内容。
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

# 创建一个聊天输入框，用户可在此输入他们的问题或消息。
prompt = st.chat_input("💬 ")
# 新增：定义清空历史问答的按钮及其回调函数
clear_history_button = st.button("清空历史问答", key="key_3")
if clear_history_button:
    st.session_state["messages"] = []
# 检查用户是否输入了内容。若有输入，则继续后续逻辑。
if prompt:
    # 检查是否已提供OpenAI API密钥。若未提供，则显示错误信息并停止程序执行。
    if not openai_api_key:
        st.error("请输入OpenAI API秘钥")
        st.stop()

    # 将用户输入的消息添加到会话状态的'messages'列表中，标记其角色为"human"。
    st.session_state["messages"].append({"role": "human", "content": prompt})

    # 在聊天界面显示用户输入的消息，使用对应的"human"角色。
    st.chat_message("human").write(prompt)

    try:
        with st.spinner("⏳ 正在生成回答..."):
            # 使用提供的`chat_with_gpt`函数与GPT模型进行交互，生成对用户输入的回复。
            # 参数包括用户输入、对话内存对象、以及OpenAI API密钥。
            response = chat_with_gpt(prompt, st.session_state["memory"], openai_api_key)

        # 将生成的回复存储在字典中，标记其角色为"ai"，并添加到会话状态的'messages'列表中。
        msg = {"role": "ai", "content": response}
        # 在聊天界面显示AI生成的回复，使用对应的"ai"角色。
        st.session_state["messages"].append(msg)
        st.chat_message("ai").write(response)
    except Exception as e:
        st.error(f"✖️回答生成失败❗️❗️❗️")
        st.error(f"错误内容：{e}")
