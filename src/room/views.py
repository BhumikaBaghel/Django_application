from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Room, Message

@login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'room/rooms.html', {'rooms': rooms})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]

    return render(request, 'room/room.html', {'room': room, 'messages': messages})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

@login_required
def get_messages(request, slug):
    room = get_object_or_404(Room, slug=slug)
    messages = Message.objects.filter(room=room).order_by('date_added')

    message_data = []
    for message in messages:
        message_data.append({
            'user': message.user.username,
            'content': message.content,
            'date_added': message.date_added.strftime('%Y-%m-%d %H:%M:%S')
        })

    return JsonResponse({'messages': message_data})


@login_required
@csrf_exempt  # Add this decorator to bypass CSRF token requirement for AJAX
def send_message(request):
    print("entered")
    if request.method == 'POST' and request.is_ajax():
        user = request.user
        room_name = request.POST.get('room')
        content = request.POST.get('message')

        if room_name and content:
            try:
                room = Room.objects.get(slug=room_name)
                message = Message.objects.create( room=room,user=user, content=content)

                # Create a dictionary with the message details
                message_data = {
                    'user': message.user.username,
                    'content': message.content,
                    # 'date_added': message.date_added.strftime('%Y-%m-%d %H:%M:%S')
                }
                print("Message Saved Successfully:", message_data)

                return JsonResponse({'status': 'success', 'message': message_data})
            except Room.DoesNotExist:
                print("Room not found for room_name:", room_name) 
                return JsonResponse({'status': 'error', 'message': 'Room not found'})
                
        else:
            print("Invalid data - room_name:", room_name, "content:", content)
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})

    print("Invalid request method or not AJAX")
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})