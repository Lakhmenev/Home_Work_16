import os
import json
import re
from app import db, models
from datetime import datetime
# from sqlalchemy.sql import exists


DATE_PATTERN = re.compile(r'\d{2}/\d{2}/\d{4}')


def load_fixture(file_path):
    """
    Загрузка содержимого фикстуры.
    :param file_path: Путь к файлу с фикстурой.
    :return: Данные из фикстуры или пустой список.
    """
    content = []
    if os.path.isfile(file_path):
        with open(file_path, encoding='utf8') as file:
            content = json.load(file)
    return content


def migration(fixture_path, model, convert_dates=False):
    fixture_content = load_fixture(fixture_path)

    for fixture in fixture_content:

        # Конвертация  дат из формата mm/dd/YYYY в ISO 8601.
        if convert_dates:
            for field_name, field_value in fixture.items():
                if isinstance(field_value, str) and re.search(DATE_PATTERN, field_value):
                    fixture[field_name] = datetime.strptime(field_value, '%m/%d/%Y').date()

        # if db.session.query(exists().where(models.UserRoles.id == role['id'])) is False: # один  из вариантов
        if db.session.query(model).filter(model.id == fixture['id']).first() is None:
            db.session.add(model(**fixture))

    db.session.commit()


def migrate_user_roles(fixture_path):
    migration(
        fixture_path=fixture_path,
        model=models.UserRole,
    )


def migrate_users(fixture_path):
    migration(
        fixture_path=fixture_path,
        model=models.User,
    )


def migrate_orders(fixture_path):
    migration(
        fixture_path=fixture_path,
        model=models.Order,
        convert_dates=True,
    )


def migrate_offers(fixture_path):
    migration(
        fixture_path=fixture_path,
        model=models.Offer,
    )
