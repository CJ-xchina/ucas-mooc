#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Python 
@File    ：main.py
@IDE     ：PyCharm 
@Author  ：Cjx_1023
@Date    ：2023/11/9 15:39 
'''
import numpy as np
import win32api
import win32con
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pyautogui
import threading
from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm


# 解析视频持续时间
def convertTime(time):
    # 解析时间值
    minutes, seconds = map(int, time.split(':'))
    total_time = minutes * 60 + seconds
    return total_time


# 移动鼠标函数
def mouseMoveTo(element, driver):
    # Assume there is equal amount of browser chrome on the left and right sides of the screen.
    canvas_x_offset = driver.execute_script(
        "return window.screenX + (window.outerWidth - window.innerWidth) / 2 - window.scrollX;")
    # Assume all the browser chrome is on the top of the screen and none on the bottom.
    canvas_y_offset = driver.execute_script(
        "return window.screenY + (window.outerHeight - window.innerHeight) - window.scrollY;")
    # Get the element center.
    element_location = (element.rect["x"] + canvas_x_offset + element.rect["width"] / 2,
                        element.rect["y"] + canvas_y_offset + element.rect["height"] / 2)
    # 移动物理鼠标到目标位置
    pyautogui.moveTo(element_location[0], element_location[1], duration=0.1)  # 可以指定移动时间


def process_video(idx, url, account, password, maxThreads):
    print("\n-------%s thread is process section %s-------" % (threading.current_thread().name, idx))
    driver, a_elements = create_base_page(url, account, password)
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of(a_elements[idx])
        )
        a_elements[idx].click()
        time.sleep(2)
        iframe1 = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'iframe'))
        )
        driver.switch_to.frame(iframe1)
        vdsFrames = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, 'iframe[src="/ananas/modules/video/index.html?v=2023-0105-1556"]'))
        )
        print("\n检测到本页中的视频数量为:", len(vdsFrames))

        # 页面无视频
        if len(vdsFrames) == 0:
            driver.quit()
            return

        for i in range(len(vdsFrames)):
            driver.switch_to.default_content()
            driver.switch_to.frame(iframe1)
            driver.switch_to.frame(vdsFrames[i])
            startButton = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "vjs-big-play-button"))
            )
            driver.execute_script("arguments[0].scrollIntoViewIfNeeded(true);", startButton)



            # 播放视频
            startButton.click()
            time.sleep(0.5)

            controlButton = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "vjs-button"))
            )
            # 暂停视频
            controlButton.click()

            # 定位到进度条元素
            progress_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "vjs-progress-holder"))
            )

            # 获取进度条的宽度
            progress_width = progress_element.size["width"]

            # 拖拽视频，减去已经看过的部分，节省时间
            for distance in np.arange(0.1, 0.6, 0.1):
                # 计算拖动的距离（根据需要拖动的百分比进行计算）
                drag_distance = progress_width * distance  # 例如，拖动到进度条一半的位置

                # 使用动作链进行拖动操作
                action_chains = ActionChains(driver)
                action_chains.click_and_hold(progress_element).move_by_offset(drag_distance, 0).release().perform()

            # 获取视频总时长，单位：s
            during = convertTime(WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "vjs-duration-display"))
            ).text)
            # 获取视频已观看时长，单位： s
            last = convertTime(WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "vjs-current-time-display"))
            ).text)

            # 开始观看视频
            controlButton.click()
            print("\n thread %s is watching vedio：" % (i + 1), "总时长：%s" % str(during), "已观看时长：%s" % str(last),
                  "剩余时长：%s" % str(during - last))
            for _ in tqdm(range((during - last + 3) // 3), desc=threading.current_thread().name, position=idx % maxThreads):
                time.sleep(3)

        print("-------%s thread finish %s -------" % (threading.current_thread().name, idx))
    except Exception:
        print(Exception)

    finally:
        driver.quit()


def deal_vedios(idx, max_threads, url, account, password):
    threadPool = ThreadPoolExecutor(max_workers=max_threads, thread_name_prefix="视频处理线程_")
    futures = []

    for i in idx:
        future = threadPool.submit(process_video, i, url, account, password, max_threads)
        futures.append(future)

    threadPool.shutdown(wait=True)  # 等待所有线程完成

    print("所有视频处理完成")
    # 进行其他操作


def deal_PPT(index, url, account, password):
    for i in index:
        driver, a_elements = create_base_page(url, account, password)
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of(a_elements[i])
            )
            a_elements[i].click()
            time.sleep(2)
            # 一层frame特点：id = "iframe"
            iframe1 = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'iframe'))
            )
            driver.switch_to.frame(iframe1)
            # 二层frame为视频层,视频可能存在多个
            iframes = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, 'iframe[src="/ananas/modules/pdf/index.html?v=2022-1202-1135"]'))
            )
            print("number of PPT in section %s " % i, ": %s" % len(iframes))

            if len(iframes) == 0:
                driver.quit()
                continue;

            for j in range(len(iframes)):
                driver.switch_to.default_content()
                driver.switch_to.frame(iframe1)
                driver.switch_to.frame(iframes[j])
                PPT_Window = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "imglook"))
                )
                # 使用 execute_script() 方法将元素滚动到可见区域
                driver.execute_script("arguments[0].scrollIntoViewIfNeeded(true);", PPT_Window)
                time.sleep(1)
                mouseMoveTo(PPT_Window, driver)
                for k in range(10000):
                    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -10)
                time.sleep(1)

        except Exception:
            print('error from ',i)

        finally:
            driver.quit()


def create_base_page(url, account, password):
    retryTime = 0
    while retryTime < 50000:
        try:
            # 创建浏览器实例
            driver = webdriver.Chrome()
            # 最大化窗口
            driver.maximize_window()
            # 打开Chrome页面
            driver.get(url)
            # 等待账号输入栏可见
            account_input = WebDriverWait(driver, 4).until(
                EC.visibility_of_element_located((By.ID, "phone"))
            )

            # 输入账号
            account_input.send_keys(account)  # 替换为您的账号

            # 等待密码输入栏可见
            password_input = WebDriverWait(driver, 4).until(
                EC.visibility_of_element_located((By.ID, "pwd"))
            )

            # 输入密码
            password_input.send_keys(password)  # 替换为您的密码

            # 等待登录按钮可点击
            login_button = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-big-blue.margin-btm24"))
            )

            # 点击登录按钮
            login_button.click()
            # 等待onetoone的div加载完成
            wait = WebDriverWait(driver, 4)
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'onetoone')))

            # 找到所有的a标签
            a_elements = driver.find_elements(By.CLASS_NAME, 'onetoone')[0].find_elements(By.TAG_NAME, 'a')
            return driver, a_elements

        # 打开网页失败，关闭浏览器
        except Exception:
            print("\n网络连接失败........")
            print("尝试连接：", retryTime)
            driver.quit()
            retryTime = retryTime + 1


def create_and_login(url, account, password):
    # 创建基础页面
    driver, a_elements = create_base_page(url, account, password)
    print("全部的章节数量：", len(a_elements))

    # 找到 onetoone 下的所有 span 元素
    span_elements = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, 'roundpointStudent'))
    )

    # 需要学习的 a 编号
    ret = []

    print("-----------------------未完成章节列表---------------------")
    for i in range(len(span_elements)):

        if 'orange01' in span_elements[i].get_attribute('class'):
            spans = a_elements[i].find_elements(By.TAG_NAME, "span")
            add = 1
            for span in spans:
                if "quiz" in span.text.lower():
                    add = 0
            if add == 1:
                ret.append(i)

    print("未完成章节：", ret)
    print("未完成的章节数量：", len(ret))
    driver.quit()
    return ret


# ...

def main():
    # 替换为你的mooc网址
    url = ""
    # mooc账号
    account = ""
    # mooc密码
    password = ""

    n = int(input("请输入视频线程数量："))

    idx = create_and_login(url, account, password)
    while len(idx) != 0:
        try:
            deal_vedios(idx, n, url, account, password)
            deal_PPT(idx, url, account, password)
            idx = create_and_login(url, account, password)
        except Exception:
            print(Exception)

    print("刷完啦！！")


if __name__ == "__main__":
    main()
