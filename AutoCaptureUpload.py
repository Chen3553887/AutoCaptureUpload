import os
import subprocess
import random
import requests
import yaml


def capture_screenshots(video_path, num_screenshots=3, output_dir=None):
    # 生成随机的截图时间点
    video_duration = get_video_duration(video_path)
    screenshot_times = random.sample(range(1, video_duration), num_screenshots)

    # 创建一个文件夹存储截图
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    screenshots_dir = os.path.join(output_dir, video_name)
    os.makedirs(screenshots_dir, exist_ok=True)

    # 使用ffmpeg截取视频截图
    for i, timepoint in enumerate(screenshot_times):
        output_file = f'{screenshots_dir}/{video_name}_{i+1}.jpg'
        ffmpeg_command = ['ffmpeg', '-ss', str(timepoint), '-i', video_path, '-vframes', '1', '-q:v', '2', output_file]
        subprocess.run(ffmpeg_command)


def get_video_duration(video_path):
    # 使用ffprobe获取视频时长
    ffprobe_command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
    result = subprocess.run(ffprobe_command, capture_output=True, text=True)
    return int(float(result.stdout))


def upload_to_image_hosting(image_path):
    # 读取配置文件
    with open("config.yml", "r") as file:
        config = yaml.safe_load(file)

    endpoint = config.get("endpoint")
    authorization = config.get("authorization")

    # 打开图像文件并读取二进制数据
    files = {"file": open(image_path, 'rb')}
    params = {"strategy_id": 2}

    # 发送POST请求
    head = {'Authorization': authorization, 'Accept': 'application/json'}
    response = requests.post(endpoint, headers=head, data=params, files=files)

    # 检查响应状态码
    if response.status_code == 200:
        print("图片上传成功！")
        return response.json()
    else:
        print("图片上传失败。错误信息：", response.text)
        return None


# 获取拖入的视频文件路径
video_path = input("请拖入视频文件：").strip('"')

# 读取配置文件中的输出路径
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)
output_dir = config.get("output_dir")

# 截取截图并保存到指定路径
capture_screenshots(video_path, config.get("num_screenshots"), output_dir)

# 遍历文件夹找到图片文件并上传到图床
video_name = os.path.splitext(os.path.basename(video_path))[0]
screenshots_dir = os.path.join(output_dir, video_name)
bbcode_collection = []
for filename in os.listdir(screenshots_dir):
    if filename.endswith(".jpg"):
        image_path = os.path.join(screenshots_dir, filename)
        result = upload_to_image_hosting(image_path)
        if result and "data" in result:
            bbcode = result["data"]["links"]["bbcode"]
            bbcode_collection.append(bbcode)

print("所有图片返回的bbcode数据合集：\n")
for bbcode in bbcode_collection:
    print(bbcode+"\n")
input("按任意键关闭窗口...")
