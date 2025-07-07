import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.csv_reader import CSVReader
import time


class TestSignup:
    """Тесты для страницы регистрации"""
    
    def test_signup_page_loads(self, driver, base_url):
        """Тест загрузки страницы регистрации"""
        driver.get(f"{base_url}/signup/")
        
        # Проверяем заголовок страницы
        assert "Sign Up" in driver.title
        
        # Проверяем наличие формы регистрации
        form = driver.find_element(By.TAG_NAME, "form")
        assert form.is_displayed()
        
    def test_signup_form_elements(self, driver, base_url):
        """Тест наличия элементов формы регистрации"""
        driver.get(f"{base_url}/signup/")
        
        # Проверяем наличие всех полей формы
        first_name_field = driver.find_element(By.NAME, "first_name")
        last_name_field = driver.find_element(By.NAME, "last_name")
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        confirm_password_field = driver.find_element(By.NAME, "confirm_password")
        date_of_birth_field = driver.find_element(By.NAME, "date_of_birth")
        
        first_name_field.send_keys(test_user_data["first_name"])
        last_name_field.send_keys(test_user_data["last_name"])
        email_field.send_keys("invalid-email-format")
        password_field.send_keys(test_user_data["password"])
        confirm_password_field.send_keys(test_user_data["password"])
        date_of_birth_field.send_keys(test_user_data["date_of_birth"])
        
        # Отправляем форму
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Проверяем, что остались на странице регистрации
        assert "/signup/" in driver.current_url
        
    def test_signup_with_invalid_date_format(self, driver, base_url, test_user_data):
        """Тест регистрации с неверным форматом даты"""
        driver.get(f"{base_url}/signup/")
        
        # Заполняем форму с неверным форматом даты
        first_name_field = driver.find_element(By.NAME, "first_name")
        last_name_field = driver.find_element(By.NAME, "last_name")
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        confirm_password_field = driver.find_element(By.NAME, "confirm_password")
        date_of_birth_field = driver.find_element(By.NAME, "date_of_birth")
        
        first_name_field.send_keys(test_user_data["first_name"])
        last_name_field.send_keys(test_user_data["last_name"])
        email_field.send_keys(f"test_{int(time.time())}@example.com")
        password_field.send_keys(test_user_data["password"])
        confirm_password_field.send_keys(test_user_data["password"])
        date_of_birth_field.send_keys("invalid-date")
        
        # Отправляем форму
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Проверяем, что остались на странице регистрации
        assert "/signup/" in driver.current_url
        
    def test_signup_with_duplicate_email(self, driver, base_url):
        """Тест регистрации с уже существующим email"""
        driver.get(f"{base_url}/signup/")
        
        # Получаем существующего пользователя из CSV
        existing_user = CSVReader.read_test_users()[0]
        
        # Заполняем форму с существующим email
        first_name_field = driver.find_element(By.NAME, "first_name")
        last_name_field = driver.find_element(By.NAME, "last_name")
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        confirm_password_field = driver.find_element(By.NAME, "confirm_password")
        date_of_birth_field = driver.find_element(By.NAME, "date_of_birth")
        
        first_name_field.send_keys("New")
        last_name_field.send_keys("User")
        email_field.send_keys(existing_user["email"])
        password_field.send_keys("newpassword123")
        confirm_password_field.send_keys("newpassword123")
        date_of_birth_field.send_keys("1990-01-01")
        
        # Отправляем форму
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Проверяем, что остались на странице регистрации или показали ошибку
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
        
        assert "/signup/" in driver.current_url
        
    @pytest.mark.parametrize("invalid_date", [
        "32-12-2000",  # Неверный день
        "01-13-2000",  # Неверный месяц
        "2000-13-01",  # Неверный месяц в правильном формате
        "2000-02-30",  # Неверная дата для февраля
        "abc-def-ghij",  # Полностью неверный формат
    ])
    def test_signup_with_various_invalid_dates(self, driver, base_url, test_user_data, invalid_date):
        """Тест регистрации с различными неверными датами"""
        driver.get(f"{base_url}/signup/")
        
        # Заполняем форму с неверной датой
        first_name_field = driver.find_element(By.NAME, "first_name")
        last_name_field = driver.find_element(By.NAME, "last_name")
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        confirm_password_field = driver.find_element(By.NAME, "confirm_password")
        date_of_birth_field = driver.find_element(By.NAME, "date_of_birth")
        
        first_name_field.send_keys(test_user_data["first_name"])
        last_name_field.send_keys(test_user_data["last_name"])
        email_field.send_keys(f"test_{int(time.time())}@example.com")
        password_field.send_keys(test_user_data["password"])
        confirm_password_field.send_keys(test_user_data["password"])
        date_of_birth_field.send_keys(invalid_date)
        
        # Отправляем форму
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Проверяем, что остались на странице регистрации
        assert "/signup/" in driver.current_url
        date_of_birth_field = driver.find_element(By.NAME, "date_of_birth")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        assert first_name_field.is_displayed()
        assert last_name_field.is_displayed()
        assert email_field.is_displayed()
        assert password_field.is_displayed()
        assert confirm_password_field.is_displayed()
        assert date_of_birth_field.is_displayed()
        assert submit_button.is_displayed()
        assert submit_button.text == "Sign Up"
        
    def test_signup_form_labels(self, driver, base_url):
        """Тест наличия подписей к полям формы"""
        driver.get(f"{base_url}/signup/")
        
        # Проверяем текст подписей
        page_text = driver.page_source
        
        assert "Your first name:" in page_text
        assert "Your last name:" in page_text
        assert "Your email:" in page_text
        assert "Your password:" in page_text
        assert "Confirm password:" in page_text
        assert "Your date of birth[YYYY-MM-DD]:" in page_text
        
    def test_home_button_exists(self, driver, base_url):
        """Тест наличия кнопки домой"""
        driver.get(f"{base_url}/signup/")
        
        home_link = driver.find_element(By.LINK_TEXT, "🏠 Домой")
        assert home_link.is_displayed()
        assert home_link.get_attribute("href") == f"{base_url}/"
        
    def test_successful_signup(self, driver, base_url, test_user_data):
        """Тест успешной регистрации"""
        driver.get(f"{base_url}/signup/")
        
        # Заполняем форму регистрации
        first_name_field = driver.find_element(By.NAME, "first_name")
        last_name_field = driver.find_element(By.NAME, "last_name")
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        confirm_password_field = driver.find_element(By.NAME, "confirm_password")
        date_of_birth_field = driver.find_element(By.NAME, "date_of_birth")
        
        # Добавляем уникальный email для избежания дублирования
        unique_email = f"test_{int(time.time())}@example.com"
        
        first_name_field.send_keys(test_user_data["first_name"])
        last_name_field.send_keys(test_user_data["last_name"])
        email_field.send_keys(unique_email)
        password_field.send_keys(test_user_data["password"])
        confirm_password_field.send_keys(test_user_data["password"])
        date_of_birth_field.send_keys(test_user_data["date_of_birth"])
        
        # Отправляем форму
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Ожидаем перенаправления
        WebDriverWait(driver, 10).until(
            EC.url_contains(base_url)
        )
        
        # Проверяем успешную регистрацию (перенаправление на главную или страницу входа)
        assert driver.current_url in [f"{base_url}/", f"{base_url}/signin/"]
        
    def test_signup_with_mismatched_passwords(self, driver, base_url, test_user_data):
        """Тест регистрации с несовпадающими паролями"""
        driver.get(f"{base_url}/signup/")
        
        # Заполняем форму с разными паролями
        first_name_field = driver.find_element(By.NAME, "first_name")
        last_name_field = driver.find_element(By.NAME, "last_name")
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        confirm_password_field = driver.find_element(By.NAME, "confirm_password")
        date_of_birth_field = driver.find_element(By.NAME, "date_of_birth")
        
        first_name_field.send_keys(test_user_data["first_name"])
        last_name_field.send_keys(test_user_data["last_name"])
        email_field.send_keys(f"test_{int(time.time())}@example.com")
        password_field.send_keys(test_user_data["password"])
        confirm_password_field.send_keys("different_password")
        date_of_birth_field.send_keys(test_user_data["date_of_birth"])
        
        # Отправляем форму
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Проверяем, что остались на странице регистрации
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
        
        assert "/signup/" in driver.current_url
        
    def test_signup_with_empty_fields(self, driver, base_url):
        """Тест регистрации с пустыми полями"""
        driver.get(f"{base_url}/signup/")
        
        # Отправляем форму без заполнения полей
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Проверяем, что остались на странице регистрации
        assert "/signup/" in driver.current_url
        
    def test_signup_with_invalid_email(self, driver, base_url, test_user_data):
        """Тест регистрации с неверным форматом email"""
        driver.get(f"{base_url}/signup/")
        
        # Заполняем форму с неверным email
        first_name_field = driver.find_element(By.NAME, "first_name")
        last_name_field = driver.find_element(By.NAME, "last_name")
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        confirm_password_field = driver.find_element(By.NAME, "confirm_password")