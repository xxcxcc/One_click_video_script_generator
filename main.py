import streamlit as st
from utils import generate_script

st.title("🎬 视频脚本生成器")

with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API秘钥", type="password")
    st.markdown("[若无秘钥，请点此获取](https://api.aigc369.com/register)")

st.divider()

subject = st.text_input("💡 请输入主题")

st.divider()

video_video_length = st.number_input("⏱️ 请输入视频长度（单位：分钟）", min_value=0.1,
                                     max_value=10.0, value=5.0, step=0.1)

st.divider()

creativity = st.slider("✨ 请选择创意程度", min_value=0.0, max_value=1.0,
                       value=0.2, step=0.1)

st.divider()

button = st.button("🚀 生成脚本")
if button:
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
