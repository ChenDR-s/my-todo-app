# 应用图标

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
