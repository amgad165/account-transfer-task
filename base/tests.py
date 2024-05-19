from django.test import TestCase, Client
from django.urls import reverse
from .models import Account
from decimal import Decimal
import pandas as pd
from io import StringIO, BytesIO




class AccountTransferViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.sender_account = Account.objects.create(id='acc1', name='Sender Account', balance=Decimal('100.00'))
        self.receiver_account = Account.objects.create(id='acc2', name='Receiver Account', balance=Decimal('50.00'))

    def test_account_transfer_page(self):
        response = self.client.get(reverse('account_transfer'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_transfer.html')
        self.assertIn('accounts', response.context)

    def test_send_money_success(self):
        response = self.client.post(reverse('send_money'), {
            'senderAccountId': 'acc1',
            'receiverAccountId': 'acc2',
            'amount': '10.00'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'Money sent successfully'})
        self.sender_account.refresh_from_db()
        self.receiver_account.refresh_from_db()
        self.assertEqual(self.sender_account.balance, Decimal('90.00'))
        self.assertEqual(self.receiver_account.balance, Decimal('60.00'))

    def test_send_money_insufficient_balance(self):
        response = self.client.post(reverse('send_money'), {
            'senderAccountId': 'acc1',
            'receiverAccountId': 'acc2',
            'amount': '150.00'
        })
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Insufficient balance'})

    def test_send_money_same_account(self):
        response = self.client.post(reverse('send_money'), {
            'senderAccountId': 'acc1',
            'receiverAccountId': 'acc1',
            'amount': '10.00'
        })
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Sender and receiver accounts cannot be the same.'})

class ImportAccountsViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_import_accounts_invalid_file_type(self):
        response = self.client.post(reverse('import_accounts'), {'file': StringIO('Invalid file content')})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid file type. Please upload a CSV or Excel file.')

    def test_import_accounts_csv(self):
        csv_file = StringIO("ID,Name,Balance\nacc3,New Account,200.00")
        csv_file.name = 'test.csv'
        response = self.client.post(reverse('import_accounts'), {'file': csv_file})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1 rows imported successfully.')
        new_account = Account.objects.get(id='acc3')
        self.assertEqual(new_account.name, 'New Account')
        self.assertEqual(new_account.balance, Decimal('200.00'))

    def test_import_accounts_xlsx(self):
        data = {'ID': ['acc4'], 'Name': ['Another Account'], 'Balance': [300.00]}
        df = pd.DataFrame(data)
        excel_file = BytesIO()
        df.to_excel(excel_file, index=False)
        excel_file.seek(0)
        excel_file.name = 'test.xlsx'
        response = self.client.post(reverse('import_accounts'), {'file': excel_file})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1 rows imported successfully.')
        new_account = Account.objects.get(id='acc4')
        self.assertEqual(new_account.name, 'Another Account')
        self.assertEqual(new_account.balance, Decimal('300.00'))