from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import os


class DriverFactory:
    """Фабрика для создания WebDriver с различными настройками"""
    
    @staticmethod
    def create_chrome_driver(headless=True, window_size=(1920, 1080)):
        """Создание Chrome WebDriver"""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
        
        # Отключение логов
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        return driver
    
    @staticmethod
    def create_firefox_driver(headless=True, window_size=(1920, 1080)):
        """Создание Firefox WebDriver"""
        firefox_options = FirefoxOptions()
        
        if headless:
            firefox_options.add_argument("--headless")
        
        firefox_options.add_argument(f"--width={window_size[0]}")
        firefox_options.add_argument(f"--height={window_size[1]}")
        
        driver = webdriver.Firefox(options=firefox_options)
        driver.implicitly_wait(10)
        return driver
    
    @staticmethod
    def create_edge_driver(headless=True, window_size=(1920, 1080)):
        """Создание Edge WebDriver"""
        edge_options = EdgeOptions()
        
        if headless:
            edge_options.add_argument("--headless")
        
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
        
        driver = webdriver.Edge(options=edge_options)
        driver.implicitly_wait(10)
        return driver
    
    @staticmethod
    def create_driver(browser_name="chrome", headless=True, window_size=(1920, 1080)):
        """Создание WebDriver для указанного браузера"""
        browser_name = browser_name.lower()
        
        if browser_name == "chrome":
            return DriverFactory.create_chrome_driver(headless, window_size)
        elif browser_name == "firefox":
            return DriverFactory.create_firefox_driver(headless, window_size)
        elif browser_name == "edge":
            return DriverFactory.create_edge_driver(headless, window_size)
        else:
            raise ValueError(f"Неподдерживаемый браузер: {browser_name}")
    
    @staticmethod
    def get_browser_from_env():
        """Получение браузера из переменной окружения"""
        return os.getenv("BROWSER", "chrome")
    
    @staticmethod
    def get_headless_from_env():
        """Получение режима headless из переменной окружения"""
        return os.getenv("HEADLESS", "true").lower() == "true"