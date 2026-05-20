# 前端编译与同步指南

## 概述
本文档说明如何将前端编译后的文件同步到后端，确保前后端访问的页面相同。

## 方法一：使用自动化脚本（推荐）

项目根目录下提供了自动化脚本 `sync_frontend_to_backend.sh`，可以一键完成前端编译和同步。

```bash
# 在项目根目录执行
./sync_frontend_to_backend.sh
```

该脚本会自动完成以下步骤：
1. 编译 admin 应用
2. 编译 chat 应用
3. 清理后端静态目录
4. 复制编译后的文件到后端

## 方法二：手动执行

### 1. 编译前端

进入 ui 目录：
```bash
cd ui
```

编译 admin 应用：
```bash
npm run build-only
```

编译 chat 应用：
```bash
npm run build-only-chat
```

### 2. 同步到后端

编译完成后，前端文件会生成在：
- `ui/dist/admin/` - admin 应用
- `ui/dist/chat/` - chat 应用

将这些文件复制到后端静态目录：
```bash
# 回到项目根目录
cd ..

# 清理后端静态目录
rm -rf backend/src/main/resources/static/admin/*
rm -rf backend/src/main/resources/static/chat/*

# 复制 admin 文件
cp -r ui/dist/admin/* backend/src/main/resources/static/admin/

# 复制 chat 文件
cp -r ui/dist/chat/* backend/src/main/resources/static/chat/
```

## 目录结构

```
backend/src/main/resources/static/
├── admin/          # 管理后台静态文件
│   ├── index.html
│   ├── assets/
│   ├── theme/
│   └── tool/
└── chat/           # 聊天界面静态文件
    ├── index.html
    ├── assets/
    ├── theme/
    └── tool/
```

## 验证

同步完成后，可以通过以下方式验证：

1. 检查文件数量：
```bash
ls backend/src/main/resources/static/admin/assets/ | wc -l
ls backend/src/main/resources/static/chat/assets/ | wc -l
```

2. 启动后端服务，访问：
   - Admin: `http://localhost:8080/admin/`
   - Chat: `http://localhost:8080/chat/`

## 注意事项

- 确保已安装 Node.js 和 npm
- 首次编译前需要运行 `npm install` 安装依赖
- 编译过程可能需要几分钟时间
- 同步前会清空后端静态目录，请确保已提交重要更改
