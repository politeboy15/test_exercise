import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time


@pytest.fixture
def driver():
    """Fixture для создания и настройки WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск в headless режиме
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def authenticated_driver(driver):
    """Fixture для авторизованного пользователя"""
    driver.get("http://localhost:8000/signin/")
    
    # Заполняем форму входа
    email_field = driver.find_element(By.NAME, "email")
    password_field = driver.find_element(By.NAME, "password")
    
    email_field.send_keys("test@example.com")
    password_field.send_keys("testpassword")
    
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    
    # Ждем перенаправления на главную страницу
    WebDriverWait(driver, 10).until(
        EC.url_contains("localhost:8000")
    )
    
    return driver


@pytest.fixture
def test_user_data():
    """Fixture с тестовыми данными пользователя"""
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "password": "testpassword123",
        "date_of_birth": "1990-01-01"
    }


@pytest.fixture
def test_ad_data():
    """Fixture с тестовыми данными объявления"""
    return {
        "title": "Test Ad Title",
        "description": "This is a test ad description",
        "image_path": "/path/to/test/image.jpg"
    }


@pytest.fixture
def base_url():
    """Fixture с базовым URL приложения"""
    return "http://localhost:8000"


def wait_for_element(driver, by, value, timeout=10):
    """Утилита для ожидания элемента"""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def wait_for_clickable(driver, by, value, timeout=10):
    """Утилита для ожидания кликабельного элемента"""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )


def wait_for_url_contains(driver, url_part, timeout=10):
    """Утилита для ожидания URL"""
    return WebDriverWait(driver, timeout).until(
        EC.url_contains(url_part)
    )


def handle_alert(driver, accept=True):
    """Утилита для работы с алертами"""
    try:
        alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
        if accept:
            alert.accept()
        else:
            alert.dismiss()
        return True
    except TimeoutException:
        return False