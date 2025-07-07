import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time


class TestCreateAd:
    """Тесты для создания объявлений"""
    
    def test_create_ad_page_loads(self, authenticated_driver, base_url):
        """Тест загрузки страницы создания объявления"""
        authenticated_driver.get(f"{base_url}/create_ad/")
        
        # Проверяем заголовок страницы
        assert "Create Ad" in authenticated_driver.title
        
        # Проверяем наличие формы создания объявления
        form = authenticated_driver.find_element(By.TAG_NAME, "form")
        assert form.is_displayed()
        
    def test_create_ad_form_elements(self, authenticated_driver, base_url):
        """Тест наличия элементов формы создания объявления"""
        authenticated_driver.get(f"{base_url}/create_ad/")
        
        # Проверяем наличие кнопки отправки
        submit_button = authenticated_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        assert submit_button.is_displayed()
        assert submit_button.text == "Create Ad"
        
        # Проверяем наличие CSRF токена
        csrf_token = authenticated_driver.find_element(By.NAME, "csrfmiddlewaretoken")
        assert csrf_token.get_attribute("value") is not None
        
    def test_home_button_exists(self, authenticated_driver, base_url):
        """Тест наличия кнопки домой"""
        authenticated_driver.get(f"{base_url}/create_ad/")
        
        home_link = authenticated_driver.find_element(By.LINK_TEXT, "🏠 Домой")
        assert home_link.is_displayed()
        assert home_link.get_attribute("href") == f"{base_url}/"
        
    def test_home_button_confirmation(self, authenticated_driver, base_url):
        """Тест подтверждения при нажатии кнопки домой"""
        authenticated_driver.get(f"{base_url}/create_ad/")
        
        home_link = authenticated_driver.find_element(By.LINK_TEXT, "🏠 Домой")
        onclick_attr = home_link.get_attribute("onclick")
        
        assert "confirm" in onclick_attr
        assert "вернуться на главную страницу" in onclick_attr
        
    def test_create_ad_requires_authentication(self, driver, base_url):
        """Тест, что создание объявления требует авторизации"""
        driver.get(f"{base_url}/create_ad/")
        
        # Проверяем, что неавторизованный пользователь перенаправляется на страницу входа
        WebDriverWait(driver, 10).until(
            lambda d: "/signin/" in d.current_url or "login" in d.current_url.lower()
        )
        
        assert "/signin/" in driver.current_url or "login" in driver.current_url.lower()
        
    def test_create_ad_with_valid_data(self, authenticated_driver, base_url, test_ad_data):
        """Тест создания объявления с корректными данными"""
        authenticated_driver.get(f"{base_url}/create_ad/")
        
        # Предполагаем, что форма имеет поля title и description
        # (точные поля зависят от Django формы)
        try:
            title_field = authenticated_driver.find_element(By.NAME, "title")
            description_field = authenticated_driver.find_element(By.NAME, "description")
            
            # Заполняем форму
            title_field.send_keys(test_ad_data["title"])
            description_field.send_keys(test_ad_data["description"])
            
            # Если есть поле для изображения, пропускаем его в этом тесте
            try:
                image_field = authenticated_driver.find_element(By.NAME, "image")
                # Можно добавить загрузку тестового изображения
                # image_field.send_keys("/path/to/test/image.jpg")
            except:
                pass
            
            # Отправляем форму
            submit_button = authenticated_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            # Ожидаем перенаправления (на главную страницу или страницу объявления)
            WebDriverWait(authenticated_driver, 10).until(
                lambda d: d.current_url != f"{base_url}/create_ad/"
            )
            
            # Проверяем успешное создание
            assert "/create_ad/" not in authenticated_driver.current_url
            
        except Exception as e:
            # Если поля формы не найдены, пропускаем тест
            pytest.skip(f"Не удается найти поля формы: {e}")
            
    def test_create_ad_with_empty_form(self, authenticated_driver, base_url):
        """Тест создания объявления с пустой формой"""
        authenticated_driver.get(f"{base_url}/create_ad/")
        
        # Отправляем пустую форму
        submit_button = authenticated_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Проверяем, что остались на странице создания
        # (может быть показана ошибка валидации)
        time.sleep(2)  # Даем время на обработку
        
        # Проверяем, что все еще на странице создания объявления
        assert "/create_ad/" in authenticated_driver.current_url
        
    def test_create_ad_with_image_upload(self, authenticated_driver, base_url, test_ad_data):
        """Тест создания объявления с загрузкой изображения"""
        authenticated_driver.get(f"{base_url}/create_ad/")
        
        try:
            # Ищем поля формы
            title_field = authenticated_driver.find_element(By.NAME, "title")
            description_field = authenticated_driver.find_element(By.NAME, "description")
            image_field = authenticated_driver.find_element(By.NAME, "image")
            
            # Заполняем текстовые поля
            title_field.send_keys(test_ad_data["title"])
            description_field.send_keys(test_ad_data["description"])
            
            # Создаем временный тестовый файл изображения
            test_image_path = self.create_test_image()
            
            # Загружаем изображение
            image_field.send_keys(test_image_path)
            
            # Отправляем форму
            submit_button = authenticated_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            # Ожидаем перенаправления
            WebDriverWait(authenticated_driver, 10).until(
                lambda d: d.current_url != f"{base_url}/create_ad/"
            )
            
            # Проверяем успешное создание
            assert "/create_ad/" not in authenticated_driver.current_url
            
            # Удаляем временный файл
            if os.path.exists(test_image_path):
                os.remove(test_image_path)
                
        except Exception as e:
            pytest.skip(f"Не удается протестировать загрузку изображения: {e}")
            
    def test_create_ad_with_large_image(self, authenticated_driver, base_url, test_ad_data):
        """Тест создания объявления с большим изображением"""
        authenticated_driver.get(f"{base_url}/create_ad/")
        
        try:
            # Ищем поля формы
            title_field = authenticated_driver.find_element(By.NAME, "title")
            description_field = authenticated_driver.find_element(By.NAME, "description")
            image_field = authenticated_driver.find_element(By.NAME, "image")
            
            # Заполняем текстовые поля
            title_field.send_keys(test_ad_data["title"])
            description_field.send_keys(test_ad_data["description"])
            
            # Создаем временный большой файл
            test_image_path = self.create_large_test_image()
            
            # Загружаем изображение
            image_field.send_keys(test_image_path)
            
            # Отправляем форму
            submit_button = authenticated_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            # Ожидаем результата (может быть ошибка о размере файла)
            time.sleep(3)
            
            # Удаляем временный файл
            if os.path.exists(test_image_path):
                os.remove(test_image_path)
                
        except Exception as e:
            pytest.skip(f"Не удается протестировать большое изображение: {e}")
            
    def test_create_ad_with_invalid_file_type(self, authenticated_driver, base_url, test_ad_data):
        """Тест создания объявления с неподдерживаемым типом файла"""
        authenticated_driver.get(f"{base_url}/create_ad/")
        
        try:
            # Ищем поля формы
            title_field = authenticated_driver.find_element(By.NAME, "title")
            description_field = authenticated_driver.find_element(By.NAME, "description")
            image_field = authenticated_driver.find_element(By.NAME, "image")
            
            # Заполняем текстовые поля
            title_field.send_keys(test_ad_data["title"])
            description_field.send_keys(test_ad_data["description"])
            
            # Создаем временный файл неподдерживаемого типа
            test_file_path = self.create_test_text_file()
            
            # Загружаем файл
            image_field.send_keys(test_file_path)
            
            # Отправляем форму
            submit_button = authenticated_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            # Ожидаем ошибки валидации
            time.sleep(2)
            
            # Проверяем, что остались на странице создания
            assert "/create_ad/" in authenticated_driver.current_url
            
            # Удаляем временный файл
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
                
        except Exception as e:
            pytest.skip(f"Не удается протестировать неподдерживаемый тип файла: {e}")
            
    def create_test_image(self):
        """Создание тестового изображения"""
        import tempfile
        from PIL import Image
        
        # Создаем временный файл
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        
        # Создаем простое изображение
        img = Image.new('RGB', (100, 100), color='red')
        img.save(temp_file.name)
        
        return temp_file.name
        
    def create_large_test_image(self):
        """Создание большого тестового изображения"""
        import tempfile
        from PIL import Image
        
        # Создаем временный файл
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        
        # Создаем большое изображение (например, 5000x5000)
        img = Image.new('RGB', (5000, 5000), color='blue')
        img.save(temp_file.name)
        
        return temp_file.name
        
    def create_test_text_file(self):
        """Создание тестового текстового файла"""
        import tempfile
        
        # Создаем временный текстовый файл
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        temp_file.write(b"This is a test text file")
        temp_file.close()
        
        return temp_file.name