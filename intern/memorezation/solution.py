from typing import Callable
import functools
import hashlib
import pickle

def memoize(func: Callable) -> Callable:
    """Memoize function"""
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Создаем уникальный хеш из аргументов"""
        key = hashlib.sha256(pickle.dumps((args, kwargs))).hexdigest()
        # Проверяем, есть ли сохраненное значение для данного хеша
        if key not in cache:
            # Вызываем функцию и сохраняем результат в кэше
            cache[key] = func(*args, **kwargs)

        return cache[key]

    return wrapper
