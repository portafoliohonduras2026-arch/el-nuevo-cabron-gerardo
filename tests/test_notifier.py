import unittest
from unittest.mock import patch, MagicMock
from connectors.notifier import TelegramNotifier

class TestTelegramNotifier(unittest.TestCase):

    def test_notifier_disabled_without_credentials(self):
        notifier = TelegramNotifier(token="", chat_id="")
        self.assertFalse(notifier.enabled)
        self.assertFalse(notifier.send_alert("Test mensaje"))

    @patch('connectors.notifier.urllib.request.urlopen')
    def test_notifier_handles_network_failure_gracefully(self, mock_urlopen):
        # Simular caída de red o timeout al intentar contactar la API de Telegram
        mock_urlopen.side_effect = Exception("Conexión fallida con Telegram")
        
        notifier = TelegramNotifier(token="fake_token", chat_id="fake_chat")
        self.assertTrue(notifier.enabled)
        
        # El método debe capturar la excepción internamente y retornar False sin lanzar error
        result = notifier.send_alert("Prueba de fallo de red")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
