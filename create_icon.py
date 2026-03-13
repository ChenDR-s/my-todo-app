"""
创建应用图标
生成简单的待办事项管理器图标
"""

import os
from pathlib import Path


def create_icon_files():
    """创建图标文件和目录结构"""
    
    # 创建资源目录
    resources_dir = Path("resources")
    icons_dir = resources_dir / "icons"
    
    icons_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建图标说明文件
    icon_readme = icons_dir / "README.md"
    icon_readme_content = """# 应用图标

待办事项管理器的图标文件。

## 图标规格

建议创建以下尺寸的图标：

### Windows (.ico 文件)
- 16x16 像素
- 32x32 像素  
- 48x48 像素
- 64x64 像素
- 128x128 像素
- 256x256 像素

### 网页版 (.png 文件)
- 32x32 像素 (favicon)
- 192x192 像素 (Android Chrome)
- 512x512 像素 (PWA)

## 图标设计建议

1. **颜色**：使用蓝色系 (#2196f3) 或绿色系 (#4caf50)
2. **元素**：勾选标记 ✓ 或待办列表 📝
3. **风格**：简洁、现代、扁平化设计

## 在线图标生成工具

1. **Favicon.io**: https://favicon.io/
2. **RealFaviconGenerator**: https://realfavicongenerator.net/
3. **Canva**: https://www.canva.com/
4. **Figma**: https://www.figma.com/

## 使用现有图标

可以从以下网站下载免费图标：
- **Flaticon**: https://www.flaticon.com/
- **Icons8**: https://icons8.com/
- **Font Awesome**: https://fontawesome.com/

## 图标文件命名

- `app.ico` - Windows桌面应用图标
- `favicon.ico` - 网页版favicon
- `icon-192.png` - PWA图标 (192x192)
- `icon-512.png` - PWA图标 (512x512)

## 使用方法

1. 将生成的图标文件放在此目录
2. 在代码中引用：
   - 桌面应用: `setWindowIcon(QIcon("resources/icons/app.ico"))`
   - 网页版: `<link rel="icon" href="/static/icons/favicon.ico">`
"""
    
    with open(icon_readme, "w", encoding="utf-8") as f:
        f.write(icon_readme_content)
    
    # 创建简单的SVG图标示例
    svg_icon = icons_dir / "icon-template.svg"
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
    <!-- 背景圆形 -->
    <circle cx="256" cy="256" r="240" fill="#2196f3" stroke="#1976d2" stroke-width="8"/>
    
    <!-- 勾选标记 -->
    <path d="M 200 280 L 240 320 L 320 220" 
          fill="none" 
          stroke="white" 
          stroke-width="30" 
          stroke-linecap="round" 
          stroke-linejoin="round"/>
    
    <!-- 待办列表轮廓 -->
    <rect x="140" y="140" width="232" height="232" 
          rx="20" ry="20" 
          fill="none" 
          stroke="white" 
          stroke-width="12" 
          opacity="0.3"/>
    
    <!-- 列表项1 -->
    <line x1="180" y1="180" x2="220" y2="180" 
          stroke="white" 
          stroke-width="12" 
          stroke-linecap="round"/>
    
    <!-- 列表项2 -->
    <line x1="180" y1="220" x2="260" y2="220" 
          stroke="white" 
          stroke-width="12" 
          stroke-linecap="round"/>
    
    <!-- 列表项3 -->
    <line x1="180" y1="260" x2="240" y2="260" 
          stroke="white" 
          stroke-width="12" 
          stroke-linecap="round"/>
</svg>
"""
    
    with open(svg_icon, "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    # 创建图标配置脚本
    icon_config = icons_dir / "generate_icons.py"
    config_content = '''"""
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
    
    print("\\n图标创建完成！")
    print("如需ICO格式，请使用在线转换工具或安装icoextract库")


if __name__ == "__main__":
    create_simple_icon()
'''
    
    with open(icon_config, "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print("=" * 60)
    print("图标资源目录已创建")
    print("=" * 60)
    print("目录结构:")
    print(f"  {icons_dir}/")
    print(f"    README.md          - 图标说明文档")
    print(f"    icon-template.svg  - SVG图标模板")
    print(f"    generate_icons.py  - 图标生成脚本")
    print()
    print("下一步:")
    print("1. 安装Pillow: pip install Pillow")
    print("2. 运行生成脚本: python resources/icons/generate_icons.py")
    print("3. 使用在线工具将PNG转换为ICO格式")
    print("4. 将图标文件重命名为app.ico")
    print("=" * 60)


if __name__ == "__main__":
    create_icon_files()