import logging
from datetime import datetime
from pathlib import Path
import os


def get_logger(name: str = "pipeline") -> logging.Logger:
    """
    创建项目统一日志器
    同时输出到控制台 + 按日期分割日志文件
    :param name: 日志器名称，默认 pipeline
    :return: 配置完成的 logger 对象
    """
    # 日志存放目录，自动创建
    log_dir = Path("6_outputs") / "logs"
    log_dir.mkdir(exist_ok=True, parents=True)

    # 按日期命名日志文件
    log_filename = f"pipeline_{datetime.now().strftime('%Y%m%d')}.log"
    log_file = log_dir / log_filename

    # 获取日志实例
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 防止重复添加handler造成日志重复打印
    if not logger.handlers:
        # 文件输出处理器
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        # 控制台输出处理器
        console_handler = logging.StreamHandler()

        # 日志格式定义
        log_formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 绑定格式器
        file_handler.setFormatter(log_formatter)
        console_handler.setFormatter(log_formatter)

        # 挂载处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger