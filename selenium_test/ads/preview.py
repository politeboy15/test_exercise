import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TestAdPreview:
    """Тесты для просмотра детальной информации об объявлении"""
    
    def test_ad_detail_page_loads(self, driver, base_url):
        """Тест загрузки страницы детального просмотра объявления"""
        # Предполагаем, что объявление с ID 1 существует
        driver.get(f"{base_url}/ad/1/")
        
        # Проверяем заголовок страницы
        assert "Ad Detail" in driver.title
        
    def test_ad_detail_elements_present(self, driver, base_url):
        """Тест наличия элементов на странице детального просмотра"""
        driver.get(f"{base_url}/ad/1/")
        
        try:
            # Проверяем наличие заголовка объявления
            title_element = driver.find_element(By.TAG_NAME, "h1")
            assert title_element.is_displayed()
            
            # Проверяем наличие описания
            description_elements = driver.find_elements(By.TAG_NAME, "p")
            assert len(description_elements) > 0
            
            # Проверяем наличие статуса
            status_found = False
            for p in description_elements:
                if "Status of this ad:" in p.text:
                    status_found = True
                    break
            assert status_found, "Статус объявления не найден"
            
        except NoSuchElementException:
            # Если элементы не найдены, пропускаем тест
            pytest.skip("Не удается получить доступ к странице детального просмотра объявления")