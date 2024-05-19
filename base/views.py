from django.shortcuts import render
import pandas as pd
from django.contrib import messages
from .models import Account
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from decimal import Decimal


# Create your views here.

def index(request):
    return render(request, 'index.html')



def account_transfer(request):

    accounts = list(Account.objects.values())

    return render(request, 'account_transfer.html', {'accounts': accounts})



def import_accounts(request):
    if request.method == 'POST':
        file = request.FILES['file']
        
        # Check file type
        if not file.name.endswith(('.csv', '.xls', '.xlsx')):
            messages.error(request, 'Invalid file type. Please upload a CSV or Excel file.')
            return render(request, 'import_accounts.html')
        
        # Read the file using Pandas
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            
            # Check for duplicates based on ID
            existing_ids = Account.objects.values_list('id', flat=True)
            new_accounts = df[~df['ID'].isin(existing_ids)]
            
            # Import new accounts to the database
            imported_count = 0
            for index, row in new_accounts.iterrows():
                Account.objects.create(id=row['ID'], name=row['Name'], balance=row['Balance'])
                imported_count += 1
            
            messages.success(request, f'{imported_count} rows imported successfully.')
        except Exception as e:
            messages.error(request, f'Error importing accounts: {str(e)}')
    
    return render(request, 'import_accounts.html')





def send_money(request):
    if request.method == 'POST':
        sender_account_id = request.POST.get('senderAccountId').strip()
        receiver_account_id = request.POST.get('receiverAccountId').strip()

        if sender_account_id == receiver_account_id:
            return JsonResponse({'error': 'Sender and receiver accounts cannot be the same.'}, status=400)

        amount = Decimal(request.POST.get('amount'))

        try:
            sender_account = get_object_or_404(Account, id=sender_account_id)
            receiver_account = get_object_or_404(Account, id=receiver_account_id)
        except:
            return JsonResponse({'error': 'error retrieving account'}, status=400)
        
        if sender_account.balance >= amount:
            sender_account.balance -= amount
            receiver_account.balance += amount
            sender_account.save()
            receiver_account.save()
            return JsonResponse({'message': 'Money sent successfully'})
        else:
            return JsonResponse({'error': 'Insufficient balance'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)