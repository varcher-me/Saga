import win32api
import win32gui
import win32con
# import win32process
import time
import os
import shutil
import traceback
import logger
import Calchash as calchash
import redis

path_init = 'd:\\temp\\init\\'
path_processed = 'd:\\temp\\processed\\'   # todo:改为正确目录1
path_error = 'd:\\temp\\error\\'
path_result = 'd:\\temp\\result\\'
path_printed = 'd:\\temp\\'
file_printed = 'PrintedPDF.pdf'
retry_interval = 0.2
retry_seconds = 20
logger = logger.logger

redis_ip = '127.0.0.1'
redis_port = '6379'


class FileOperaException(Exception):
    pass


def compare_file(file1, file2):
    hash1 = calchash.calc_sha1(file1)
    hash2 = calchash.calc_sha1(file2)
    if 0 == hash1 or 0 == hash2 or not hash1 == hash2:
        return False
    else:
        return True


def get_window(hwnd_father, hwnd_child_after, window_class, window_context):
    retry_time = retry_seconds / retry_interval
    while retry_time > 0:
        time.sleep(0.2)
        hwnd = win32gui.FindWindowEx(hwnd_father, hwnd_child_after, window_class, window_context)
        if hwnd:
            break
        else:
            retry_time -= 1
    if hwnd:
        return hwnd
    else:
        raise FileOperaException("Wait for window appear timed out.")


def wait_window_disappear(hwnd):
    retry_time = retry_seconds / retry_interval
    while retry_time > 0:
        time.sleep(0.2)
        result = win32gui.IsWindow(hwnd)
        if result:
            retry_time -= 1
        else:
            return True
    raise FileOperaException("Wait for window disappear timed out.")


def wait_for_file(full_file):
    retry_time = retry_seconds / retry_interval
    while retry_time > 0:
        time.sleep(0.2)
        if os.path.isfile(full_file):
            try:
                time.sleep(0.5)
                fp = open(full_file, 'a')
                fp.close()
                return True
            except:
                retry_time -= 1
        else:
            retry_time -= 1
    raise FileOperaException("Wait for file "+full_file+" appear timed out.")


def rename_file(printed_file, renamed_file):
    wait_for_file(printed_file)
    if os.path.isfile(renamed_file):
        if compare_file(printed_file, renamed_file):
            logger.warning("File ["+renamed_file+"] existed when renamed, sha1 is identity, origin is remained.")
            os.remove(printed_file)
            return True
        else:
            logger.warning("File ["+renamed_file+"] existed when renamed, sha1 is different, incoming is remained.")
            os.remove(renamed_file)
    os.rename(printed_file, renamed_file)


def move_file(origin_file, new_file, new_path):
    if os.path.isfile(new_file):
        if compare_file(origin_file, new_file):
            logger.warning("File ["+new_file+"] existed when copied, sha1 is identity, origin is remained.")
            os.remove(origin_file)
            return True
        else:
            logger.warning("File ["+new_file+"] existed when copied, sha1 is different, incoming is remained.")
            os.remove(new_file)
    shutil.move(origin_file, new_path)
    print("File "+new_file+" moved.")


def process_file(path, raw_file):
    # 打开文件
    print("Starting processing " + raw_file)
    win32api.ShellExecute(0, 'open', path + raw_file, '', '', 1)
    hwnd_main_sep = get_window(None, None, None, 'SEP Reader - [' + raw_file + ']')
    if 0 == hwnd_main_sep:
        logger.fatal("FATAL ERROR: SEP Reader Window not found! program terminated.")
        exit(100)

    # 发送打印指令
    win32gui.SetForegroundWindow(hwnd_main_sep)
    win32api.keybd_event(17, 0, 0, 0)  # Ctrl
    win32api.keybd_event(80, 0, 0, 0)  # P
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(80, 0, win32con.KEYEVENTF_KEYUP, 0)

    # 等待打印窗体、按回车并判断窗体消失
    hwnd_printer = get_window(None, None, None, 'SEP Reader')
    win32gui.SetForegroundWindow(hwnd_printer)
    win32api.keybd_event(13, 0, 0, 0)  # Enter
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
    if not wait_window_disappear(hwnd_printer):
        logger.error("File [" + raw_file + "] print-window-disappear timed out; WM_CLOSE signal sent.")
        win32api.SendMessage(hwnd_printer, win32con.WM_CLOSE, 0, 0)

    # 窗口清理（SEP为关闭文件，保留程序窗口）
    win32gui.SetForegroundWindow(hwnd_main_sep)
    win32api.keybd_event(17, 0, 0, 0)  # Ctrl
    win32api.keybd_event(87, 0, 0, 0)  # W
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(87, 0, win32con.KEYEVENTF_KEYUP, 0)
    print("File " + raw_file + " printed.")
    # win32api.SendMessage(hwnd_main, win32con.WM_CLOSE, 0, 0)

    printed_file = os.path.join(path_printed, file_printed)
    renamed_file = os.path.join(path_printed, raw_file + '.pdf')
    moved_file = os.path.join(path_result, raw_file + '.pdf')

    # 重命名文件
    try:
        rename_file(printed_file, renamed_file)
    except Exception as e:
        logger.fatal("FATAL ERROR: rename file failed, exception is "+str(e)+", process terminated.")
        exit(100)

    # 移动文件
    try:
        move_file(renamed_file, moved_file, path_result)
    except Exception as e:
        logger.fatal("FATAL ERROR: move file failed, exception is "+str(e)+", process terminated.")
        exit(101)


while 1:
    for i in os.walk(path_init):
        for fileName in i[2]:
            try:
                process_file(path_init, fileName)
                if path_init != path_processed:
                    move_file(path_init+fileName, path_processed+fileName, path_processed)
            except Exception as e:
                logger.fatal("FATAL ERROR: something error, exception is "+str(e)+".")
    time.sleep(10)
