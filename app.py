import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from json_to_html import convert_json_to_html


class JsonToHtmlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON 知识库转 HTML 工具")
        self.root.geometry("620x320")

        self.json_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.page_type = tk.StringVar(value="general")

        self.build_ui()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="JSON 知识库转 HTML 工具",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=20)

        # JSON 文件选择
        frame_json = tk.Frame(self.root)
        frame_json.pack(fill="x", padx=30, pady=8)

        tk.Label(frame_json, text="JSON 文件：", width=12, anchor="w").pack(side="left")

        tk.Entry(frame_json, textvariable=self.json_path).pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        tk.Button(frame_json, text="选择文件", command=self.select_json).pack(side="left")

        # 输出目录选择
        frame_output = tk.Frame(self.root)
        frame_output.pack(fill="x", padx=30, pady=8)

        tk.Label(frame_output, text="输出目录：", width=12, anchor="w").pack(side="left")

        tk.Entry(frame_output, textvariable=self.output_dir).pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        tk.Button(frame_output, text="选择目录", command=self.select_output_dir).pack(side="left")

        # 页面类型
        frame_type = tk.Frame(self.root)
        frame_type.pack(fill="x", padx=30, pady=8)

        tk.Label(frame_type, text="页面类型：", width=12, anchor="w").pack(side="left")

        options = ["general", "character", "event", "relation"]

        tk.OptionMenu(frame_type, self.page_type, *options).pack(side="left")

        # 转换按钮
        tk.Button(
            self.root,
            text="开始转换",
            font=("Arial", 14),
            width=20,
            height=2,
            command=self.convert
        ).pack(pady=25)

        hint = tk.Label(
            self.root,
            text="转换完成后，会在输出目录生成 .html 和 .md 文件",
            fg="#666"
        )
        hint.pack()

    def select_json(self):
        file_path = filedialog.askopenfilename(
            title="选择 JSON 文件",
            filetypes=[("JSON 文件", "*.json")]
        )

        if file_path:
            self.json_path.set(file_path)

            if not self.output_dir.get():
                self.output_dir.set(str(Path(file_path).parent))

    def select_output_dir(self):
        directory = filedialog.askdirectory(title="选择输出目录")

        if directory:
            self.output_dir.set(directory)

    def convert(self):
        json_file = self.json_path.get()
        output_dir = self.output_dir.get()
        page_type = self.page_type.get()

        if not json_file:
            messagebox.showerror("错误", "请先选择 JSON 文件")
            return

        if not output_dir:
            messagebox.showerror("错误", "请先选择输出目录")
            return

        try:
            input_path = Path(json_file)
            output_path = Path(output_dir)

            html_path = output_path / f"{input_path.stem}.html"
            md_path = output_path / f"{input_path.stem}.md"

            convert_json_to_html(
                json_path=input_path,
                html_path=html_path,
                md_path=md_path,
                page_type=page_type
            )

            messagebox.showinfo(
                "转换成功",
                f"HTML 文件已生成：\n{html_path}\n\nMarkdown 文件已生成：\n{md_path}"
            )

        except Exception as e:
            messagebox.showerror("转换失败", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = JsonToHtmlApp(root)
    root.mainloop()