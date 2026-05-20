from modelscope.hub.snapshot_download import snapshot_download

# 下载 text2vec-base-chinese 模型
# local_dir 指定为你配置中的路径
model_dir = snapshot_download('Jerry0/text2vec-base-chinese',
                              local_dir='/opt/maxkb-app/model/base')

print(f"模型已成功下载至: {model_dir}")