from django.shortcuts import render

# Create your views here.
import csv
from django.shortcuts import render
from django.http import JsonResponse
from .models import Member, Inventory,Booking, MAX_BOOKINGS
from django.core.files.storage import FileSystemStorage
from .forms import CSVUploadForm
import datetime as dt


from django.utils import timezone

def home(request):
    return render(request, 'upload.html')

def handle_uploaded_file(f, model_class):
    """Helper function to handle CSV file upload and parsing."""
    decoded_file = f.read().decode('utf-8').splitlines()
    csv_reader = csv.reader(decoded_file)
    
    if model_class == Member:
        for row in csv_reader:
            _, created = Member.objects.get_or_create(
                first_name=row[0],
                last_name=row[1],
                booking_count=int(row[2]),
                date_joined=row[3]
            )
    elif model_class == Inventory:
        for row in csv_reader:
            _, created = Inventory.objects.get_or_create(
                title=row[0],
                description=row[1],
                remaining_count=int(row[2]),
                expiration_date=dt.datetime.strptime(row[3], "%d-%m-%Y")
            )

def upload_csv(request):
    """View to upload CSV file via form."""
    print(request)
    #print(request.FILES['csv_file'])
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        if 'members' in csv_file.name:
            print("Inside the members")
            handle_uploaded_file(csv_file, Member)
        elif 'inventory' in csv_file.name:
            print("Inside the INventory")
            handle_uploaded_file(csv_file, Inventory)
        return JsonResponse({'message': 'File uploaded successfully'}, status=200)
    # else:
    #     form = CSVUploadForm
    # context = {'form': form}  https://github.com/nawaz-07/Catalyst_task_File_Parser/blob/master/catalyst_count/catalyst_task/views.py
    return render(request, 'upload.html')



def book_item(request):
    """Book an inventory item for a member."""
    member_id = request.GET.get('member_id')
    inventory_id = request.GET.get('inventory_id')

    try:
        member = Member.objects.get(id=member_id)
        inventory = Inventory.objects.get(id=inventory_id)

        # Check if the member has reached MAX_BOOKINGS
        if member.booking_count >= MAX_BOOKINGS:
            return JsonResponse({'error': 'Maximum bookings reached.'}, status=400)

        # Check if the item is available
        if inventory.remaining_count <= 0:
            return JsonResponse({'error': 'Inventory item is out of stock.'}, status=400)

        # Create a new booking
        booking = Booking.objects.create(member=member, inventory=inventory)
        member.booking_count += 1
        inventory.remaining_count -= 1

        member.save()
        inventory.save()

        return JsonResponse({'message': 'Booking successful', 'booking_id': booking.id}, status=200)

    except Member.DoesNotExist:
        return JsonResponse({'error': 'Member not found.'}, status=404)
    except Inventory.DoesNotExist:
        return JsonResponse({'error': 'Inventory item not found.'}, status=404)

def cancel_booking(request):
    """Cancel a booking based on booking reference."""
    booking_id = request.GET.get('booking_id')

    try:
        booking = Booking.objects.get(id=booking_id)
        member = booking.member
        inventory = booking.inventory

        booking.delete()
        member.booking_count -= 1
        inventory.remaining_count += 1

        member.save()
        inventory.save()

        return JsonResponse({'message': 'Booking cancelled successfully.'}, status=200)

    except Booking.DoesNotExist:
        return JsonResponse({'error': 'Booking not found.'}, status=404)


