# AutoCaptureUpload

基于兰空图床的视频自动截图并上传截图至图床的工具

## 需求

- [ ] 开放API的[lsky-pro](https://github.com/lsky-org/lsky-pro)图床
- [ ] FFmpeg

## 使用

1、编辑config.yml

```yaml
#图床地址
endpoint: https://xxxx/api/v1/upload
#填写你的api
authorization: Bearer xxxx
#截图数量
num_screenshots: 4
#截图保存地址
output_dir:
```

2、运行py文件即可
