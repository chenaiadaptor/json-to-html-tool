import streamlit as st
from pathlib import Path
import tempfile

from json_to_html import convert_json_to_html


st.set_page_config(
    page_title="JSON 知识库转 HTML 工具",
    page_icon="📚",
    layout="centered"
)

st.title("📚 JSON 知识库转 HTML 工具")

st.write("上传一个知识库 JSON 文件，系统会自动生成 Markdown 和 HTML 页面。")

uploaded_file = st.file_uploader(
    "请选择 JSON 文件",
    type=["json"]
)

page_type = st.selectbox(
    "请选择页面类型",
    ["general", "character", "event", "relation"],
    format_func=lambda x: {
        "general": "世界设定 general",
        "character": "角色档案 character",
        "event": "剧情事件 event",
        "relation": "关系网 relation"
    }.get(x, x)
)

if uploaded_file is not None:
    st.success(f"已上传文件：{uploaded_file.name}")

    if st.button("开始转换"):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                tmpdir = Path(tmpdir)

                input_path = tmpdir / uploaded_file.name
                html_path = tmpdir / f"{Path(uploaded_file.name).stem}.html"
                md_path = tmpdir / f"{Path(uploaded_file.name).stem}.md"

                input_path.write_bytes(uploaded_file.read())

                convert_json_to_html(
                    json_path=input_path,
                    html_path=html_path,
                    md_path=md_path,
                    page_type=page_type
                )

                html_bytes = html_path.read_bytes()
                md_bytes = md_path.read_bytes()

                st.success("转换成功！")

                st.download_button(
                    label="下载 HTML 文件",
                    data=html_bytes,
                    file_name=html_path.name,
                    mime="text/html"
                )

                st.download_button(
                    label="下载 Markdown 文件",
                    data=md_bytes,
                    file_name=md_path.name,
                    mime="text/markdown"
                )

        except Exception as e:
            st.error(f"转换失败：{e}")