import sys
import unittest
from unittest.mock import MagicMock, patch, AsyncMock

# Mock dependencies before importing manager
sys.modules['telethon'] = MagicMock()
sys.modules['telethon.sync'] = MagicMock()
sys.modules['telethon.errors'] = MagicMock()
sys.modules['telethon.errors.rpcerrorlist'] = MagicMock()
sys.modules['colorama'] = MagicMock()
sys.modules['pyfiglet'] = MagicMock()
sys.modules['keyboard'] = MagicMock()

import manager

class TestManager(unittest.IsolatedAsyncioTestCase):

    @patch('manager.check_account_status', new_callable=AsyncMock)
    async def test_check_all_accounts_parallel_empty_list(self, mock_check):
        """Test that check_all_accounts_parallel handles an empty list correctly."""
        results = await manager.check_all_accounts_parallel([])
        self.assertEqual(results, [])
        mock_check.assert_not_called()

    @patch('manager.check_account_status', new_callable=AsyncMock)
    async def test_check_all_accounts_parallel_single_account(self, mock_check):
        """Test that check_all_accounts_parallel processes a single account."""
        mock_account = [12345, 'hash', '+1234567890']
        mock_check.return_value = (mock_account, 'ACTIVE')

        results = await manager.check_all_accounts_parallel([mock_account])

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], (mock_account, 'ACTIVE'))
        mock_check.assert_called_once_with(mock_account)

if __name__ == '__main__':
    unittest.main()
