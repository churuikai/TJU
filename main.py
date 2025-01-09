import time
import requests
import yaml
import logging
from datetime import datetime
from typing import List, Dict

# 设置日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("course_selection.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)


def load_yaml(config_path: str) -> Dict:
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"加载配置文件失败: {e}")
        raise

def wait_until(target_time: datetime):
    i = 0
    while datetime.now() < target_time:
        time.sleep(0.1)
        i+=1
        if i % 10 == 0:
            logging.info(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logging.info(f"目标时间: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")

def load_course_codes(file_path: str) -> List[str]:
    """
    从文件中加载课程代码
    """
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            lines = f.readlines()
        if not lines:
            raise ValueError("配置文件为空。")
        return lines[0].strip(), [line.split()[0] for line in lines[1:] if line.strip()]
    except Exception as e:
        logging.error(f"加载课程代码失败: {e}")
        raise


def select_course(session: requests.Session, url: str, headers: Dict, course_code: str) -> bool:
    """
    尝试选课
    """
    data = {'optype': 'true', 'operator0': f'{course_code}:true:0'}
    try:
        response = session.post(url, headers=headers, data=data, timeout=10)
        if response.status_code == 200 and '成功' in response.text:
            logging.info(f"课程 {course_code} 选课成功。")
            return True
        logging.warning(f"课程 {course_code} 选课失败，响应内容: {response.text}")
        return False
    except requests.RequestException as e:
        logging.error(f"课程 {course_code} 请求异常: {e}")
        return False


def main():
    config = load_yaml("config.yaml")
    schedule = config.get('schedule', {})
    request_config = config.get('request', {})
    courses = config.get('courses', [])

    if not all([schedule, request_config, courses]):
        logging.error("配置文件缺少必要的信息。")
        return

    target_time = datetime.now().replace(hour=schedule['hour'], minute=schedule['minute'], second=0, microsecond=0)
    wait_until(target_time)

    session = requests.Session()
    headers = request_config.get('headers', {})

    remaining_courses = courses.copy()
    i = 0
    while remaining_courses:
        logging.info(f"剩余课程数: {len(remaining_courses)}")
        course_code = remaining_courses[i]
        if select_course(session, request_config['url'], headers, course_code):
            remaining_courses.pop(i)
        else:
            i = (i + 1) % len(remaining_courses)
        time.sleep(0.6)

    logging.info("所有课程已成功选课。")

if __name__ == "__main__":
    main()
