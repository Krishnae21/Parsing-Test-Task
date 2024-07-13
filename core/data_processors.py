class DataProcessor:
    """Базовый обработчик. Без модификации данных"""

    async def process_data[T](self, data: T) -> T:
        return data


class CustomDataProcessor:
    """Example"""

    async def process_data[T](self, data: T) -> dict[str, T]:
        return {"new_data": data}
