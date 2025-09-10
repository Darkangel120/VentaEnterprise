import requests
import json
from datetime import datetime, timedelta
import os

class ExchangeRateService:
    def __init__(self):
        self.cache_file = "exchange_rate_cache.json"
        self.cache_duration = timedelta(hours=1)  # Cache por 1 hora
        self.last_update = None
        self.rate = None

    def get_dollar_rate(self):
        """Obtiene la tasa del dólar en Venezuela"""
        try:
            # Verificar si hay cache válido
            if self._load_cache():
                return self.rate

            # Si no hay cache o está expirado, obtener nueva tasa
            rate = self._fetch_rate_from_api()
            if rate:
                self.rate = rate
                self.last_update = datetime.now()
                self._save_cache()
                return rate
            else:
                # Si no se pudo obtener de API, intentar usar cache anterior si existe
                if self._load_cache():
                    return self.rate

        except Exception as e:
            print(f"Error obteniendo tasa de cambio: {e}")
            # Intentar usar cache como fallback
            try:
                if self._load_cache():
                    return self.rate
            except:
                pass

        return None

    def _fetch_rate_from_api(self):
        """Obtiene la tasa desde APIs públicas"""
        # Lista de APIs para obtener tasa del dólar en Venezuela
        apis = [
            "https://pydolarve.org/api/v1/dollar?page=bcv",
            "https://api.exchangedyn.com/markets/quotes/usdves/bcv",
            "https://ve.dolarapi.com/v1/dolares/oficial"
        ]

        for api_url in apis:
            try:
                response = requests.get(api_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()

                    # Extraer tasa según la API
                    if "bcv" in api_url and "price" in data:
                        return float(data["price"])
                    elif "exchangedyn" in api_url and "price" in data:
                        return float(data["price"])
                    elif "dolarapi" in api_url and "promedio" in data:
                        return float(data["promedio"])

            except Exception as e:
                print(f"Error con API {api_url}: {e}")
                continue

        return None

    def _load_cache(self):
        """Carga la tasa desde cache si es válida"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)

                last_update = datetime.fromisoformat(cache_data['last_update'])
                if datetime.now() - last_update < self.cache_duration:
                    self.rate = cache_data['rate']
                    self.last_update = last_update
                    return True
        except Exception as e:
            print(f"Error cargando cache: {e}")

        return False

    def _save_cache(self):
        """Guarda la tasa en cache"""
        try:
            cache_data = {
                'rate': self.rate,
                'last_update': self.last_update.isoformat()
            }
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f)
        except Exception as e:
            print(f"Error guardando cache: {e}")

    def calculate_profit(self, cost_usd, selling_price_usd, quantity=1):
        """Calcula las ganancias en USD y VES"""
        if not self.rate:
            return None

        profit_usd = (selling_price_usd - cost_usd) * quantity
        profit_ves = profit_usd * self.rate

        return {
            'profit_usd': profit_usd,
            'profit_ves': profit_ves,
            'rate': self.rate
        }

    def convert_to_ves(self, amount_usd):
        """Convierte USD a VES usando la tasa actual"""
        if not self.rate:
            return None
        return amount_usd * self.rate

    def convert_to_usd(self, amount_ves):
        """Convierte VES a USD usando la tasa actual"""
        if not self.rate:
            return None
        return amount_ves / self.rate
