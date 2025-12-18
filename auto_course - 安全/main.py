import logging
import os
from main_logic import MainLogic
from config_loader import Config

# 初始化日志
def init_logger():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.basicConfig(
        filename=os.path.join(log_dir, "app.log"),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    # 同时输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logging.getLogger().addHandler(console_handler)

def main():
    init_logger()
    try:
        logging.info("=== 智慧树全自动答题助手启动 ===")
        # 加载配置
        config = Config()
        # 初始化主逻辑并运行
        main_logic = MainLogic(config)
        main_logic.run()
        logging.info("=== 程序运行完成 ===")
    except Exception as e:
        logging.error(f"程序运行出错：{str(e)}", exc_info=True)
        print(f"错误：{str(e)}，详细日志请查看 logs/app.log")

if __name__ == "__main__":
    main()