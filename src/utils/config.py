import json
import os

class Config:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self):
        """Load configuration from a JSON file or environment variables."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                return json.load(file)
        else:
            return self.load_from_env()

    def load_from_env(self):
        """Load configuration from environment variables."""
        config = {
            'DATABASE_URL': os.getenv('DATABASE_URL', 'sqlite:///default.db'),
            'API_KEY': os.getenv('API_KEY', 'default_api_key'),
            'DEBUG': os.getenv('DEBUG', 'false').lower() in ('true', '1', 't')
        }
        return config

    def get(self, key, default=None):
        """Get a configuration value by key."""
        return self.config_data.get(key, default)

# Example usage
if __name__ == "__main__":
    config = Config()
    print("Database URL:", config.get('DATABASE_URL'))
    print("API Key:", config.get('API_KEY'))
    print("Debug Mode:", config.get('DEBUG'))
