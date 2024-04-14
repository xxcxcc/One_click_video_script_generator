import streamlit as st
from utils import generate_script, generate_xiaohongshu

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

st.divider()

button_script = st.button("🚀 生成脚本", key='key_1')
if button_script:
    if not openai_api_key:
        st.error("请输入OpenAI API秘钥")
        st.stop()
    if not subject:
        st.error("请输入主题")
        st.stop()
    else:
        with st.spinner("⏳ 正在生成脚本..."):
            title, script = generate_script(subject, video_video_length,
                                            creativity, openai_api_key)
            st.subheader("💡 标题：")
            st.write(script)
            st.subheader("💡 视频脚本：")
            st.write(title)
            st.success("✅ 脚本生成成功")

st.divider()

st.header("✨ 爆款小红书AI写作助手")

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
    else:
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
