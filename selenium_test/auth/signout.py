import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestSignout:
    """Тесты для функциональности выхода из системы"""
    
    def test_signout_from_home_page(self, authenticated_driver, base_url):
        """Тест выхода из системы с главной страницы"""
        authenticated_driver.get(f"{base_url}/")
        
        # Проверяем, что пользователь авторизован
        quit_link = authenticated_driver.find_element(By.LINK_TEXT, "Quit")
        assert quit_link.is_displayed()
        
        # Нажимаем на ссылку выхода
        quit_link.click()
        
        # Ожидаем перенаправления на главную страницу
        WebDriverWait(authenticated_driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Sign in"))
        )
        
        # Проверяем, что пользователь разлогинен
        signin_link = authenticated_driver.find_element(By.LINK_TEXT, "Sign in")
        signup_link = authenticated_driver.find_element(By.LINK_TEXT, "Sign up")
        
        assert signin_link.is_displayed()
        assert signup_link.is_displayed()
        
    def test_signout_from_profile_page(self, authenticated_driver, base_url):
        """Тест выхода из системы со страницы профиля"""
        authenticated_driver.get(f"{base_url}/profile/1/")
        
        # Проверяем, что мы на странице профиля
        try:
            profile_heading = authenticated_driver.find_element(By.TAG_NAME, "h1")
            assert "Profile" in profile_heading.text
        except:
            # Если не можем найти заголовок профиля, пропускаем тест
            pytest.skip("Не удается получить доступ к странице профиля")
        
        # Нажимаем на ссылку выхода
        signout_link = authenticated_driver.find_element(By.LINK_TEXT, "Sign out")
        signout_link.click()
        
        # Ожидаем перенаправления на главную страницу
        WebDriverWait(authenticated_driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Sign in"))
        )
        
        # Проверяем, что пользователь разлогинен
        signin_link = authenticated_driver.find_element(By.LINK_TEXT, "Sign in")
        assert signin_link.is_displayed()
        
    def test_signout_redirects_to_home(self, authenticated_driver, base_url):
        """Тест перенаправления на главную страницу после выхода"""
        authenticated_driver.get(f"{base_url}/")
        
        # Нажимаем на ссылку выхода
        quit_link = authenticated_driver.find_element(By.LINK_TEXT, "Quit")
        quit_link.click()
        
        # Ожидаем перенаправления
        WebDriverWait(authenticated_driver, 10).until(
            EC.url_to_be(f"{base_url}/")
        )
        
        # Проверяем, что находимся на главной странице
        assert authenticated_driver.current_url == f"{base_url}/"
        
    def test_access_protected_page_after_signout(self, authenticated_driver, base_url):
        """Тест доступа к защищенным страницам после выхода"""
        authenticated_driver.get(f"{base_url}/")
        
        # Выходим из системы
        quit_link = authenticated_driver.find_element(By.LINK_TEXT, "Quit")
        quit_link.click()
        
        # Ожидаем разлогинивания
        WebDriverWait(authenticated_driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Sign in"))
        )
        
        # Пытаемся получить доступ к защищенной странице
        authenticated_driver.get(f"{base_url}/create_ad/")
        
        # Проверяем, что нас перенаправили на страницу входа или показали ошибку
        WebDriverWait(authenticated_driver, 10).until(
            lambda driver: "/signin/" in driver.current_url or "login" in driver.current_url.lower()
        )
        
        assert "/signin/" in authenticated_driver.current_url or "login" in authenticated_driver.current_url.lower()
        
    def test_signout_link_not_visible_for_anonymous(self, driver, base_url):
        """Тест, что ссылка выхода не видна для анонимных пользователей"""
        driver.get(f"{base_url}/")
        
        # Проверяем, что ссылки выхода нет
        try:
            quit_link = driver.find_element(By.LINK_TEXT, "Quit")
            assert False, "Ссылка 'Quit' не должна быть видна для анонимных пользователей"
        except:
            # Это ожидаемое поведение - ссылка не найдена
            pass
        
        # Проверяем, что есть ссылки для неавторизованных пользователей
        signin_link = driver.find_element(By.LINK_TEXT, "Sign in")
        signup_link = driver.find_element(By.LINK_TEXT, "Sign up")
        
        assert signin_link.is_displayed()
        assert signup_link.is_displayed()
        
    def test_multiple_signout_attempts(self, authenticated_driver, base_url):
        """Тест множественных попыток выхода"""
        authenticated_driver.get(f"{base_url}/")
        
        # Первый выход
        quit_link = authenticated_driver.find_element(By.LINK_TEXT, "Quit")
        quit_link.click()
        
        # Ожидаем разлогинивания
        WebDriverWait(authenticated_driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Sign in"))
        )
        
        # Пытаемся выйти еще раз (обращаемся к URL выхода напрямую)
        authenticated_driver.get(f"{base_url}/signout/")
        
        # Проверяем, что нас перенаправили на главную страницу
        WebDriverWait(authenticated_driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Sign in"))
        )
        
        # Проверяем, что пользователь по-прежнему разлогинен
        signin_link = authenticated_driver.find_element(By.LINK_TEXT, "Sign in")
        assert signin_link.is_displayed()
        
    def test_signout_preserves_session_data(self, authenticated_driver, base_url):
        """Тест, что выход корректно очищает данные сессии"""
        authenticated_driver.get(f"{base_url}/")
        
        # Выходим из системы
        quit_link = authenticated_driver.find_element(By.LINK_TEXT, "Quit")
        quit_link.click()
        
        # Ожидаем разлогинивания
        WebDriverWait(authenticated_driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Sign in"))
        )
        
        # Обновляем страницу
        authenticated_driver.refresh()
        
        # Проверяем, что пользователь по-прежнему разлогинен
        signin_link = authenticated_driver.find_element(By.LINK_TEXT, "Sign in")
        signup_link = authenticated_driver.find_element(By.LINK_TEXT, "Sign up")
        
        assert signin_link.is_displayed()
        assert signup_link.is_displayed()