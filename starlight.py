import streamlit as st
from pathlib import Path
import os
import configparser
import json


# ---------------------- 自定义样式：微光主题+马到成功立体风格 ----------------------
def add_success_style():
    st.markdown("""
    <style>
    /* 全局样式：微光渐变背景+层次感 */
    .main {
        background: linear-gradient(135deg, #fdf2f8 0%, #fff8e8 50%, #fcf1f7 100%);
        background-attachment: fixed;
    }
    /* 主标题：微光发光效果+3D立体 */
    .title {
        color: #c41e3a;
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        text-shadow: 
            0 2px 4px #ffd700,
            0 4px 8px #ffc107,
            0 8px 16px rgba(255, 215, 0, 0.4),
            0 16px 32px rgba(196, 30, 58, 0.2);
        margin-bottom: 10px;
        position: relative;
    }
    /* 微光主题装饰文字：动态发光动画 */
    .glimmer-text {
        color: #fff;
        font-size: 28px;
        font-weight: 600;
        text-align: center;
        margin: 15px 0;
        background: linear-gradient(90deg, #d68910, #ffd700, #c41e3a, #ffd700, #d68910);
        background-size: 200% 100%;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glimmer 3s linear infinite;
    }
    @keyframes glimmer {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    /* 副标题/励志标语：立体阴影 */
    .motivational {
        color: #d68910;
        font-size: 24px;
        font-weight: 600;
        text-align: center;
        margin: 10px 0;
        text-shadow: 1px 1px 2px #c41e3a80;
    }
    /* 选择框美化：立体边框+hover效果 */
    div[data-testid="stSelectbox"] {
        background-color: #fff;
        border: 2px solid #c41e3a;
        border-radius: 12px;
        padding: 8px;
        box-shadow: 0 4px 6px rgba(196, 30, 58, 0.1);
        transition: all 0.3s ease;
    }
    div[data-testid="stSelectbox"]:hover {
        box-shadow: 0 6px 12px rgba(196, 30, 58, 0.2);
        border-color: #d68910;
    }
    /* 信息提示框美化：立体边框+渐变背景 */
    .stInfo {
        border-left: 6px solid #ffd700;
        background: linear-gradient(90deg, #fff9e6 0%, #fffdf0 100%) !important;
        box-shadow: 0 3px 8px rgba(255, 215, 0, 0.15);
        border-radius: 8px;
    }
    /* 成功提示框美化：立体边框+渐变背景 */
    .stSuccess {
        border-left: 6px solid #c41e3a;
        background: linear-gradient(90deg, #fff0f5 0%, #fff5f8 100%) !important;
        box-shadow: 0 3px 8px rgba(196, 30, 58, 0.15);
        border-radius: 8px;
    }
    /* 分割线样式：微光渐变+立体 */
    hr {
        border: none;
        height: 3px;
        background: linear-gradient(to right, 
            transparent, 
            #c41e3a, 
            #ffd700, 
            #c41e3a, 
            transparent);
        margin: 25px 0;
        box-shadow: 0 2px 4px rgba(255, 215, 0, 0.2);
    }
    /* 底部励志语：微光效果 */
    .footer {
        color: #c41e3a;
        font-size: 18px;
        font-weight: 500;
        text-align: center;
        margin-top: 30px;
        padding: 15px;
        border-top: 3px solid #ffd700;
        background: linear-gradient(180deg, transparent, #fff8e8);
        border-radius: 8px;
        box-shadow: 0 -2px 8px rgba(196, 30, 58, 0.05);
    }
    /* 微光装饰点 */
    .glimmer-dot {
        text-align: center;
        margin: 10px 0;
        font-size: 16px;
        color: #d68910;
    }
    /* 登录框美化 - 优化宽度和内部布局 */
    .login-box {
        max-width: 400px;
        margin: 50px auto;
        padding: 30px;
        background: linear-gradient(135deg, #fff0f5 0%, #fff8e8 100%);
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(196, 30, 58, 0.15);
        border: 2px solid #ffd700;
    }
    .login-title {
        color: #c41e3a;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 0 2px 4px rgba(255, 215, 0, 0.3);
    }
    /* 登录输入框样式优化 - 缩短长度，高亮显示 */
    .login-input {
        max-width: 280px; /* 缩短输入框宽度 */
        margin: 0 auto 15px auto;
    }
    .login-input input {
        border: 2px solid #ffd700; /* 默认高亮边框 */
        border-radius: 8px;
        padding: 12px 15px;
        font-size: 16px;
        transition: all 0.3s ease;
        background-color: #fff9e6; /* 浅高亮背景 */
    }
    .login-input input:focus {
        border-color: #c41e3a; /* 聚焦时更深的高亮 */
        box-shadow: 0 0 12px rgba(255, 215, 0, 0.4); /* 强化高亮阴影 */
        outline: none;
        background-color: #fff; /* 聚焦时纯白背景对比 */
    }
    /* 登录按钮容器样式 - 确保完全居中 */
    .login-buttons {
        max-width: 280px; /* 与输入框宽度一致 */
        margin: 20px auto 0 auto;
        display: flex;
        justify-content: center; /* 水平居中 */
        align-items: center; /* 垂直居中 */
    }
    /* 小巧精致的登录按钮样式 */
    .login-btn {
        width: auto !important;
        padding: 8px 25px !important;
        font-size: 14px !important;
        border-radius: 20px !important;
        background: linear-gradient(135deg, #c41e3a 0%, #d68910 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 3px 6px rgba(196, 30, 58, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    .login-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 12px rgba(196, 30, 58, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ---------------------- 配置文件管理 ----------------------
def load_config():
    """加载配置文件，支持JSON格式的多用户配置"""
    # 配置文件路径
    config_path = Path("config.json")

    # 如果配置文件不存在，创建默认配置
    if not config_path.exists():
        default_config = {
            "users": [
                {"username": "admin", "password": "123456", "role": "admin"},
                {"username": "user1", "password": "user123", "role": "user"},
                {"username": "user2", "password": "user456", "role": "user"}
            ],
            "pdf_files": {
                "文档1": "./pdfs/test1.pdf",
                "文档2": "./pdfs/test2.pdf"
            }
        }
        # 写入默认配置
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=4)
        st.info("✅ 配置文件不存在，已创建默认配置文件 config.json")
        return default_config

    # 读取配置文件
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        # 验证配置结构
        if "users" not in config or not isinstance(config["users"], list):
            st.error("❌ 配置文件格式错误：users 字段必须是数组")
            return None
        if "pdf_files" not in config or not isinstance(config["pdf_files"], dict):
            st.error("❌ 配置文件格式错误：pdf_files 字段必须是对象")
            return None
        return config
    except json.JSONDecodeError:
        st.error("❌ 配置文件格式错误：不是有效的JSON格式")
        return None
    except Exception as e:
        st.error(f"❌ 加载配置文件失败：{str(e)}")
        return None


def validate_user(username, password, config):
    """验证用户凭据，返回用户信息或None"""
    if not config or "users" not in config:
        return None
    for user in config["users"]:
        if user.get("username") == username and user.get("password") == password:
            return user
    return None


# ---------------------- 基础配置 ----------------------
st.set_page_config(
    page_title="微光助力 | 马到成功",
    page_icon="✨",
    layout="wide"
)

# 初始化Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# 加载配置
config = load_config()
if not config:
    st.stop()

# 从配置中获取PDF文件列表
PDF_FILES = config["pdf_files"]


# ---------------------- 工具函数：校验PDF文件 ----------------------
def check_pdf_file(pdf_path):
    """校验PDF文件是否存在且格式合法"""
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        st.error(f"❌ PDF文件不存在：{pdf_file.absolute()}")
        return False
    if pdf_file.suffix.lower() != ".pdf":
        st.error(f"❌ 文件不是PDF格式：{pdf_file.name}")
        return False
    return True


# ---------------------- 增强版PDF展示（支持分页/缩放/下载） ----------------------
def show_pdf_advanced(pdf_path):
    st.subheader("📖 上岸备考PDF | 支持分页/缩放/下载 📥", help="✨ 微光助力，备考无忧 ✨")
    try:
        from streamlit_pdf_viewer import pdf_viewer
        pdf_viewer(pdf_path, width=1200)
        st.success("✅ PDF加载成功！微光汇聚，终成星海 💪")
    except ImportError:
        st.error("❌ 未安装streamlit-pdf-viewer，请执行：pip install streamlit-pdf-viewer")
    except Exception as e:
        st.error(f"❌ 增强版展示失败：{str(e)}")


# ---------------------- 登录验证函数 ----------------------
def login_form():
    """显示登录表单并验证"""
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔐 微光助力 · 登录验证</div>', unsafe_allow_html=True)

    # 优化输入框宽度，添加自定义类名
    st.markdown('<div class="login-input">', unsafe_allow_html=True)
    username = st.text_input("用户名", placeholder="请输入登录用户名", key="username", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="login-input">', unsafe_allow_html=True)
    password = st.text_input("密码", placeholder="请输入登录密码", type="password", key="password",
                             label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # 优化按钮容器宽度，确保登录按钮居中
    st.markdown('<div class="login-buttons">', unsafe_allow_html=True)
    # 小巧精致的登录按钮
    if st.button("登录", use_container_width=False, key="login_btn", help="点击登录系统",
                type="primary", disabled=False):
        user = validate_user(username, password, config)
        if user:
            st.session_state.logged_in = True
            st.session_state.current_user = user
            st.success(f"✅ 欢迎 {user['username']}！微光为你照亮上岸路 🚀")
            st.rerun()  # 重新运行页面，加载文档内容
        else:
            st.error("❌ 用户名或密码错误，请重试！")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------- 文档展示主逻辑 ----------------------
def show_document_content():
    """登录成功后显示文档内容"""
    current_user = st.session_state.current_user

    # 励志标题区 + 微光主题元素
    st.markdown('<div class="title">🐴 马到成功 · 今年必上岸 🚀</div>', unsafe_allow_html=True)
    # 核心微光主题文字（动态发光）
    st.markdown('<div class="glimmer-text">✨ 微光也是光 · 点点汇聚成希望 ✨</div>', unsafe_allow_html=True)
    # 显示当前登录用户
    st.markdown(
        f'<div class="motivational">👤 当前用户：{current_user["username"]}（{current_user["role"]}） | 📚 备考刷题不迷路 | 金榜题名在今朝 🏆</div>',
        unsafe_allow_html=True)
    # 微光装饰点
    st.markdown('<div class="glimmer-dot">🌟 每一份努力都是微光，终将照亮上岸的路 🌟</div>', unsafe_allow_html=True)
    st.divider()

    # 1. 添加PDF文件选择框
    st.markdown("### 📝 选择你的上岸备考文档：", help="✨ 微光助力，精准刷题 ✨")
    selected_doc = st.selectbox(
        "请选择要查看的PDF文档",
        options=list(PDF_FILES.keys()),
        index=0,
        help="选择后将加载对应的备考PDF文件 📄 | 微光陪你备考"
    )

    # 获取选中文档的路径
    selected_pdf_path = PDF_FILES[selected_doc]

    # 2. 校验选中的PDF文件
    if not check_pdf_file(selected_pdf_path):
        return

    # 3. 显示选中文件的信息（新增微光文案）
    pdf_file = Path(selected_pdf_path)
    file_size = round(pdf_file.stat().st_size / 1024 / 1024, 2)
    st.info(
        f"📄 备考资料：{selected_doc} | 文件名：{pdf_file.name} | 大小：{file_size} MB | 路径：{pdf_file.absolute()}\n✨ 微光文档，助力上岸 ✨")

    st.divider()
    # 4. 展示选中的PDF
    show_pdf_advanced(selected_pdf_path)

    # 退出登录按钮
    col1, col2 = st.columns([10, 1])
    with col2:
        if st.button("🚪 退出登录", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()

    # 底部励志语（融入微光主题）
    st.markdown('<div class="footer">💖 星光不负赶路人 · 微光不负追梦人 · 今年必定成功上岸 💖</div>',
                unsafe_allow_html=True)


# ---------------------- 主函数 ----------------------
def main():
    # 加载自定义样式
    add_success_style()

    # 判断登录状态，显示不同内容
    if not st.session_state.logged_in:
        # 未登录：显示登录界面
        st.markdown('<div class="title">✨ 微光助力上岸 · 请先登录 ✨</div>', unsafe_allow_html=True)
        login_form()
    else:
        # 已登录：显示文档内容
        show_document_content()


if __name__ == "__main__":
    main()