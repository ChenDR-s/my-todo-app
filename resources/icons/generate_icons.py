"""
生成图标文件的Python脚本
使用Pillow库创建各种尺寸的图标
"""

try:
    from PIL import Image, ImageDraw
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("请先安装Pillow: pip install Pillow")


def create_simple_icon():
    """创建简单的程序化图标"""
    if not HAS_PILLOW:
        print("无法创建图标：Pillow未安装")
        return
    
    # 创建512x512的基础图标
    size = 512
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制背景圆形
    margin = 20
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=(33, 150, 243, 255),  # #2196f3
        outline=(25, 118, 210, 255)  # #1976d2
    )
    
    # 绘制勾选标记
    check_points = [
        (size * 0.35, size * 0.55),  # 起点
        (size * 0.45, size * 0.65),  # 中间点
        (size * 0.65, size * 0.4)    # 终点
    ]
    
    # 绘制粗线
    line_width = int(size * 0.05)
    for i in range(len(check_points) - 1):
        x1, y1 = check_points[i]
        x2, y2 = check_points[i + 1]
        draw.line([x1, y1, x2, y2], fill=(255, 255, 255, 255), width=line_width)
    
    # 保存为PNG
    img.save("resources/icons/icon-512.png", "PNG")
    print("已创建图标: resources/icons/icon-512.png")
    
    # 创建其他尺寸
    sizes = [16, 32, 48, 64, 128, 192, 256]
    for s in sizes:
        resized = img.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(f"resources/icons/icon-{s}.png", "PNG")
        print(f"已创建图标: resources/icons/icon-{s}.png")
    
    print("\n图标创建完成！")
    print("如需ICO格式，请使用在线转换工具或安装icoextract库")


if __name__ == "__main__":
    create_simple_icon()
