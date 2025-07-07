import csv
import os
from typing import List, Dict, Any


class CSVReader:
    """Класс для чтения тестовых данных из CSV файлов"""
    
    @staticmethod
    def read_csv(file_path: str) -> List[Dict[str, Any]]:
        """Чтение данных из CSV файла"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        
        data = []
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        
        return data
    
    @staticmethod
    def read_test_users(file_path: str = "data/test_case.csv") -> List[Dict[str, str]]:
        """Чтение данных тестовых пользователей"""
        try:
            users = CSVReader.read_csv(file_path)
            return users
        except FileNotFoundError:
            # Возвращаем тестовые данные по умолчанию
            return [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john.doe@example.com",
                    "password": "password123",
                    "date_of_birth": "1990-01-01"
                },
                {
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "email": "jane.smith@example.com",
                    "password": "password456",
                    "date_of_birth": "1985-05-15"
                },
                {
                    "first_name": "Bob",
                    "last_name": "Johnson",
                    "email": "bob.johnson@example.com",
                    "password": "password789",
                    "date_of_birth": "1995-12-10"
                }
            ]
    
    @staticmethod
    def read_test_ads(file_path: str = "data/test_ads.csv") -> List[Dict[str, str]]:
        """Чтение данных тестовых объявлений"""
        try:
            ads = CSVReader.read_csv(file_path)
            return ads
        except FileNotFoundError:
            # Возвращаем тестовые данные по умолчанию
            return [
                {
                    "title": "Продам велосипед",
                    "description": "Отличный велосипед в хорошем состоянии",
                    "status": "active"
                },
                {
                    "title": "Куплю книги",
                    "description": "Покупаю книги по программированию",
                    "status": "active"
                },
                {
                    "title": "Обменяю телефон",
                    "description": "Обменяю iPhone на Android",
                    "status": "active"
                }
            ]
    
    @staticmethod
    def get_user_by_email(email: str, file_path: str = "data/test_case.csv") -> Dict[str, str]:
        """Получение пользователя по email"""
        users = CSVReader.read_test_users(file_path)
        for user in users:
            if user.get("email") == email:
                return user
        
        raise ValueError(f"Пользователь с email {email} не найден")
    
    @staticmethod
    def get_valid_user_credentials(file_path: str = "data/test_case.csv") -> Dict[str, str]:
        """Получение валидных учетных данных пользователя"""
        users = CSVReader.read_test_users(file_path)
        if users:
            return {
                "email": users[0]["email"],
                "password": users[0]["password"]
            }
        
        return {
            "email": "test@example.com",
            "password": "testpassword"
        }