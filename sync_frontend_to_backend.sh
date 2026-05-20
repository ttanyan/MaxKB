#!/bin/bash

# 前端编译并同步到后端静态目录的脚本

set -e  # 遇到错误立即退出

echo "======================================"
echo "开始编译前端并同步到后端..."
echo "======================================"

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
UI_DIR="$PROJECT_ROOT/ui"
BACKEND_STATIC_DIR="$PROJECT_ROOT/backend/src/main/resources/static"

# 检查ui目录是否存在
if [ ! -d "$UI_DIR" ]; then
    echo "错误: ui目录不存在: $UI_DIR"
    exit 1
fi

# 进入ui目录
cd "$UI_DIR"

echo ""
echo "步骤1: 编译admin应用..."
echo "--------------------------------------"
npm run build-only
echo "✓ admin应用编译完成"

echo ""
echo "步骤2: 编译chat应用..."
echo "--------------------------------------"
npm run build-only-chat
echo "✓ chat应用编译完成"

echo ""
echo "步骤3: 清理后端静态目录..."
echo "--------------------------------------"
rm -rf "$BACKEND_STATIC_DIR/admin"/*
rm -rf "$BACKEND_STATIC_DIR/chat"/*
echo "✓ 清理完成"

echo ""
echo "步骤4: 复制编译文件到后端..."
echo "--------------------------------------"
cp -r "$UI_DIR/dist/admin/"* "$BACKEND_STATIC_DIR/admin/"
echo "✓ admin文件已复制"

cp -r "$UI_DIR/dist/chat/"* "$BACKEND_STATIC_DIR/chat/"
echo "✓ chat文件已复制"

echo ""
echo "======================================"
echo "✓ 前端编译和同步完成！"
echo "======================================"
echo ""
echo "Admin静态文件位置: $BACKEND_STATIC_DIR/admin/"
echo "Chat静态文件位置: $BACKEND_STATIC_DIR/chat/"
echo ""
