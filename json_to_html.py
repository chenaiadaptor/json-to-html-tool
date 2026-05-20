from pathlib import Path
import json
import argparse


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_name}</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
:root {{
  --sidebar-width: 360px;
}}

* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

body {{
  font-family: "Microsoft YaHei", system-ui, sans-serif;
  background: #f5f7fa;
  color: #333;
}}

.wrap {{
  display: flex;
  min-height: 100vh;
}}

.aside {{
  width: var(--sidebar-width);
  background: #fff;
  border-right: 1px solid #eee;
  position: fixed;
  height: 100vh;
  overflow-y: auto;
  padding: 20px 15px;
}}

.resizer {{
  position: absolute;
  top: 0;
  right: 0;
  width: 5px;
  height: 100%;
  cursor: col-resize;
  background-color: transparent;
  transition: background-color 0.2s;
}}

.resizer:hover,
.resizer.resizing {{
  background-color: #2563eb;
}}

.nav-links {{
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}}

.nav-links h3,
.toc-container h3 {{
  font-size: 16px;
  margin-bottom: 12px;
  color: #222;
}}

.nav-links a {{
  display: flex;
  align-items: center;
  padding: 8px 10px;
  margin: 4px 0;
  color: #555;
  text-decoration: none;
  border-radius: 6px;
  font-size: 14px;
  background: #f9fafc;
}}

.nav-links a:hover {{
  background: #eef2ff;
  color: #2563eb;
}}

.toc-item {{
  margin: 2px 0;
}}

.toc-content {{
  display: flex;
  align-items: center;
}}

.toc-content a {{
  flex: 1;
  padding: 6px 8px;
  color: #555;
  text-decoration: none;
  border-radius: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}

.toc-content a:hover {{
  background: #f0f4f9;
  color: #2563eb;
}}

.toc-content a.active {{
  background: #2563eb;
  color: #fff;
}}

.toc-toggle {{
  width: 20px;
  text-align: center;
  cursor: pointer;
  user-select: none;
  color: #888;
  font-size: 12px;
}}

.toc-dot {{
  cursor: default;
  font-size: 16px;
  transform: translateY(-2px);
}}

.toc-children {{
  padding-left: 18px;
}}

.main {{
  flex: 1;
  margin-left: var(--sidebar-width);
  padding: 30px 50px;
  max-width: 1000px;
}}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4,
.markdown-body h5 {{
  margin: 1.5em 0 0.8em;
  scroll-margin-top: 20px;
}}

.markdown-body p {{
  margin: 1em 0;
  line-height: 1.8;
}}

.markdown-body pre {{
  background: #222;
  color: #eee;
  padding: 16px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 1em 0;
}}

.markdown-body code {{
  background: #e5e7eb;
  padding: 2px 5px;
  border-radius: 3px;
}}

.markdown-body ul,
.markdown-body ol {{
  padding-left: 2em;
  margin: 1em 0;
}}

.markdown-body blockquote {{
  margin: 1em 0;
  padding: 12px 16px;
  border-left: 4px solid #2563eb;
  background-color: #f0f4f9;
  color: #444;
  border-radius: 0 6px 6px 0;
}}

@media (max-width: 768px) {{
  .aside {{
    display: none;
  }}

  .main {{
    margin-left: 0;
    padding: 20px;
  }}
}}
</style>
</head>

<body>
<div class="wrap">
  <div class="aside" id="sidebar">
    <div class="resizer" id="drag-resizer"></div>

    <div class="nav-links">
      <h3>📚 IP知识库</h3>
      <a href="general.html">🌍 世界设定</a>
      <a href="character.html">👥 角色档案</a>
      <a href="event.html">🎬 剧情事件</a>
      <a href="relation.html">🕸️ 关系网</a>
    </div>

    <div class="toc-container">
      <h3>📑 文档目录</h3>
      <div id="toc"></div>
    </div>
  </div>

  <div class="main">
    <div id="content" class="markdown-body"></div>
  </div>
</div>

<script>
const mdContent = {markdown_json};

const contentDom = document.getElementById('content');
contentDom.innerHTML = marked.parse(mdContent);

// ========== 拖拽调整侧边栏宽度 ==========
const resizer = document.getElementById('drag-resizer');
let isResizing = false;

resizer.addEventListener('mousedown', () => {{
  isResizing = true;
  resizer.classList.add('resizing');
  document.body.style.userSelect = 'none';
  document.body.style.cursor = 'col-resize';
}});

document.addEventListener('mousemove', (e) => {{
  if (!isResizing) return;

  let newWidth = e.clientX;
  if (newWidth < 220) newWidth = 220;
  if (newWidth > 600) newWidth = 600;

  document.documentElement.style.setProperty('--sidebar-width', newWidth + 'px');
}});

document.addEventListener('mouseup', () => {{
  if (isResizing) {{
    isResizing = false;
    resizer.classList.remove('resizing');
    document.body.style.userSelect = '';
    document.body.style.cursor = '';
  }}
}});

// ========== 自动生成目录 ==========
function buildToc() {{
  const tocDom = document.getElementById('toc');
  const headers = contentDom.querySelectorAll('{show_headers}');

  const nodes = [];

  headers.forEach((el, idx) => {{
    const id = `heading-${{idx}}`;
    el.id = id;

    const level = parseInt(el.tagName.substring(1));
    nodes.push({{
      id,
      level,
      text: el.textContent,
      el
    }});
  }});

  nodes.forEach((node, i) => {{
    node.hasChild = i + 1 < nodes.length && nodes[i + 1].level > node.level;
  }});

  const rootContainer = document.createElement('div');
  const stack = [{{ level: 0, container: rootContainer }}];

  nodes.forEach(node => {{
    while (stack[stack.length - 1].level >= node.level) {{
      stack.pop();
    }}

    const parent = stack[stack.length - 1];

    const itemDiv = document.createElement('div');
    itemDiv.className = 'toc-item';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'toc-content';

    const a = document.createElement('a');
    a.href = `#${{node.id}}`;
    a.textContent = node.text;

    const toggleSpan = document.createElement('span');
    toggleSpan.className = 'toc-toggle';

    if (node.hasChild) {{
      const isCollapsed = node.level > 1;
      toggleSpan.textContent = isCollapsed ? '▶' : '▼';
      toggleSpan.classList.add(isCollapsed ? 'collapsed' : 'expanded');

      const childrenContainer = document.createElement('div');
      childrenContainer.className = 'toc-children';

      if (isCollapsed) {{
        childrenContainer.style.display = 'none';
      }}

      toggleSpan.onclick = (e) => {{
        e.stopPropagation();

        if (childrenContainer.style.display === 'none') {{
          childrenContainer.style.display = 'block';
          toggleSpan.textContent = '▼';
          toggleSpan.classList.replace('collapsed', 'expanded');
        }} else {{
          childrenContainer.style.display = 'none';
          toggleSpan.textContent = '▶';
          toggleSpan.classList.replace('expanded', 'collapsed');
        }}
      }};

      contentDiv.appendChild(toggleSpan);
      contentDiv.appendChild(a);
      itemDiv.appendChild(contentDiv);
      itemDiv.appendChild(childrenContainer);

      parent.container.appendChild(itemDiv);
      stack.push({{ level: node.level, container: childrenContainer }});
    }} else {{
      toggleSpan.textContent = '•';
      toggleSpan.classList.add('toc-dot');

      contentDiv.appendChild(toggleSpan);
      contentDiv.appendChild(a);
      itemDiv.appendChild(contentDiv);

      parent.container.appendChild(itemDiv);
    }}
  }});

  tocDom.appendChild(rootContainer);
}}

buildToc();

// ========== 滚动时高亮当前目录 ==========
const headers = contentDom.querySelectorAll('{show_headers}');

window.addEventListener('scroll', () => {{
  let curId = '';

  headers.forEach(h => {{
    const top = h.getBoundingClientRect().top;
    if (top <= 80) curId = h.id;
  }});

  document.querySelectorAll('#toc a.active').forEach(link => {{
    link.classList.remove('active');
  }});

  if (curId) {{
    const activeLink = document.querySelector(`#toc a[href="#${{curId}}"]`);

    if (activeLink) {{
      activeLink.classList.add('active');

      let parent = activeLink.closest('.toc-children');

      while (parent) {{
        if (parent.style.display === 'none') {{
          parent.style.display = 'block';

          const toggle = parent.previousElementSibling.querySelector('.toc-toggle');

          if (toggle && toggle.classList.contains('collapsed')) {{
            toggle.textContent = '▼';
            toggle.classList.replace('collapsed', 'expanded');
          }}
        }}

        parent = parent.parentElement.closest('.toc-children');
      }}
    }}
  }}
}});
</script>
</body>
</html>
"""


SHOW_HEADERS = {
    "general": "h1,h2,h3,h4,h5",
    "character": "h1,h2,h3",
    "event": "h1,h2,h3,h4",
    "relation": "h1,h2,h3,h4",
}


def verify_node(obj):
    """
    简单校验 JSON 节点结构。
    你的原代码里用了 from format import verify_node。
    这里我直接写一个简化版，方便单文件运行。
    """
    required_keys = ["name", "level", "hint", "data", "is_standard"]

    if not isinstance(obj, dict):
        raise ValueError("节点必须是 dict 类型")

    for key in required_keys:
        if key not in obj:
            raise ValueError(f"节点缺少必要字段: {key}")

    hint = obj["hint"]

    if hint not in ["str", "list", "dict", "node"]:
        raise ValueError(f"不支持的 hint 类型: {hint}")

    if hint == "str":
        if not isinstance(obj["data"], dict) or "value" not in obj["data"]:
            raise ValueError(f"str 节点的 data 必须包含 value 字段: {obj['name']}")

    elif hint in ["list", "dict", "node"]:
        if not isinstance(obj["data"], list):
            raise ValueError(f"{hint} 节点的 data 必须是 list: {obj['name']}")

        for child in obj["data"]:
            verify_node(child)


def json2markdown(obj, depth=1, index=""):
    """
    把结构化 JSON 节点递归转换成 Markdown。
    """

    if not isinstance(obj, dict):
        raise TypeError(f"obj 必须是 dict，当前是: {type(obj)}")

    if depth > 5:
        raise ValueError("层级过多，最多支持 5 层标题")

    name = obj["name"]
    level = obj["level"]
    is_standard = obj["is_standard"]
    data = obj["data"]
    hint = obj["hint"]

    prefix = "#" * depth

    if index:
        prefix += f" {index}"

    lvl = f" ({level})" if level else ""

    if is_standard:
        title = f"{prefix} {name}{lvl}"
    else:
        title = f"{prefix} `{name}{lvl}`"

    if hint == "str":
        value = data.get("value", "")
        return [title, f"`{value}`"]

    elif hint == "list":
        lines = [title]

        for item in data:
            if isinstance(item, dict):
                value = item.get("value", "")
            else:
                value = str(item)

            lines.append(f"* `{value}`")

        return lines

    elif hint == "dict":
        lines = [title]

        for node in data:
            key = node["name"]
            value = node["data"].get("value", "")
            node_level = node.get("level", "")
            node_level_text = f" ({node_level})" if node_level else ""

            if node.get("is_standard", False):
                lines.append(f"{key}{node_level_text}: `{value}`")
            else:
                lines.append(f"`{key}{node_level_text}`: `{value}`")

        return lines

    elif hint == "node":
        lines = [title]

        for i, node in enumerate(data):
            child_index = f"{index}{i + 1}."
            lines.extend(json2markdown(node, depth=depth + 1, index=child_index))

        return lines

    else:
        raise ValueError(f"无效 hint: {hint}")


def convert_json_to_markdown(json_path, md_path=None):
    json_path = Path(json_path)

    obj = json.loads(json_path.read_text(encoding="utf-8"))
    verify_node(obj)

    md_lines = json2markdown(obj)
    markdown = "\n\n".join(md_lines)

    if md_path:
        md_path = Path(md_path)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(markdown, encoding="utf-8")

    return markdown, obj


def convert_json_to_html(json_path, html_path, md_path=None, page_type="general"):
    markdown, obj = convert_json_to_markdown(json_path, md_path)

    show_headers = SHOW_HEADERS.get(page_type, "h1,h2,h3,h4,h5")

    html = HTML_TEMPLATE.format(
        page_name=obj.get("name", "知识库页面"),
        markdown_json=json.dumps(markdown, ensure_ascii=False),
        show_headers=show_headers,
    )

    html_path = Path(html_path)
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html, encoding="utf-8")

    return html_path


def main():
    parser = argparse.ArgumentParser(description="把知识库 JSON 转换为 HTML 页面")
    parser.add_argument("--input", "-i", required=True, help="输入 JSON 文件路径")
    parser.add_argument("--output", "-o", required=True, help="输出 HTML 文件路径")
    parser.add_argument("--markdown", "-m", default=None, help="可选：输出 Markdown 文件路径")
    parser.add_argument(
        "--type",
        "-t",
        default="general",
        choices=["general", "character", "event", "relation"],
        help="页面类型，用于控制目录显示层级",
    )

    args = parser.parse_args()

    html_path = convert_json_to_html(
        json_path=args.input,
        html_path=args.output,
        md_path=args.markdown,
        page_type=args.type,
    )

    print(f"转换完成: {html_path}")


if __name__ == "__main__":
    main()