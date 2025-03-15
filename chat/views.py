from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ChatMessage
from .bot import get_response  # Import your chatbot function

@api_view(["POST"])
def chat(request):
    user_message = request.data.get("message", "")

    # Get bot's response
    bot_response = get_response(user_message)

    # Save chat to database
    chat_message = ChatMessage(user_message=user_message, bot_response=bot_response)
    chat_message.save()

    return Response({"user": user_message, "bot": bot_response})
