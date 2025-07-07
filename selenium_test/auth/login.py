import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.csv_reader import CSVReader


class TestLogin:
    """Тесты для страницы входа"""
    
    def test_login_page_loads(self, driver, base_url):
        """Тест загрузки страницы входа"""
        driver.get(f"{base_url}/signin/")
        
        # Проверяем заголовок страницы
        assert "Sign In" in driver.title
        
        # Проверяем наличие формы входа
        form = driver.find_element(By.TAG_NAME, "form")
        assert form.is_displayed()
        
    def test_login_form_elements(self, driver, base_url):
        """Тест наличия элементов формы входа"""
        driver.get(f"{base_url}/signin/")
        
        # Проверяем наличие полей email и password
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        assert email_field.is_displayed()
        assert password_field.is_displayed()
        assert submit_button.is_displayed()
        assert submit_button.text == "Sign In"
        
    def test_home_button_exists(self, driver, base_url):
        """Тест наличия кнопки домой"""
        driver.get(f"{base_url}/signin/")
        
        home_link = driver.find_element(By.LINK_TEXT, "🏠 Домой")
        assert home_link.is_displayed()
        assert home_link.get_attribute("href") == f"{base_url}/"
        
    def test_home_button_confirmation(self, driver, base_url):
        """Тест подтверждения при нажатии кнопки домой"""
        driver.get(f"{base_url}/signin/")
        
        home_link = driver.find_element(By.LINK_TEXT, "🏠 Домой")
        onclick_attr = home_link.get_attribute("onclick")
        
        assert "confirm" in onclick_attr
        assert "вернуться на главную страницу" in onclick_attr
        
    def test_successful_login(self, driver, base_url):
        """Тест успешного входа"""
        driver.get(f"{base_url}/signin/")
        
        # Получаем данные из CSV
        credentials = CSVReader.get_valid_user_credentials()
        
        # Заполняем форму
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        
        email_field.send_keys(credentials["email"])
        password_field.send_keys(credentials["password"])
        
        # Отправляем форму
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Ожидаем перенаправления
        WebDriverWait(driver, 10).until(
            EC.url_contains(base_url)
        )
        
        # Проверяем, что мы на главной странице
        assert driver.current_url == f"{base_url}/"
        
    def test_login_with_invalid_credentials(self, driver, base_url):
        """Тест входа с неверными учетными данными"""
        driver.get(f"{base_url}/signin/")
        
        # Заполняем форму неверными данными
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        
        email_field.send_keys("invalid@example.com")
        password_field.send_keys("wrongpassword")
        
        # Отправляем форму
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Проверяем, что остались на странице входа
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
        
        assert "/signin/" in driver.current_url
        
    def test_login_with_empty_fields(self, driver, base_url):
        """Тест входа с пустыми полями"""
        driver.get(f"{base_url}/signin/")
        
        # Отправляем форму без заполнения полей
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Проверяем, что остались на странице входа
        assert "/signin/" in driver.current_url
        
    def test_login_with_invalid_email_format(self, driver, base_url):
        """Тест входа с неверным форматом email"""
        driver.get(f"{base_url}/signin/")
        
        # Заполняем форму с неверным email
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        
        email_field.send_keys("invalid-email")
        password_field.send_keys("somepassword")
        
        # Отправляем форму
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Проверяем, что остались на странице входа
        assert "/signin/" in driver.current_url
        
    @pytest.mark.parametrize("user_data", CSVReader.read_test_users())
    def test_login_with_multiple_users(self, driver, base_url, user_data):
        """Тест входа с различными пользователями из CSV"""
        driver.get(f"{base_url}/signin/")
        
        # Заполняем форму данными из CSV
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        
        email_field.clear()
        password_field.clear()
        
        email_field.send_keys(user_data["email"])
        password_field.send_keys(user_data["password"])
        
        # Отправляем форму
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Ожидаем результата (успешный вход или ошибка)
        try:
            WebDriverWait(driver, 5).until(
                EC.url_contains(base_url)
            )
            # Если вход успешен, проверяем главную страницу
            assert driver.current_url == f"{base_url}/"
        except TimeoutException:
            # Если вход неуспешен, проверяем, что остались на странице входа
            assert "/signin/" in driver.current_url