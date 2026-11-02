import logging

from ollama import ResponseError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from assistant.agent_service import run_agent
from assistant.serializers import ChatRequestSerializer


logger = logging.getLogger(__name__)


class ExpenseAssistantView(APIView):

    def post(self, request):
        serializer = ChatRequestSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user_message = serializer.validated_data["message"]

        try:
            answer = run_agent(user_message)

            return Response(
                {
                    "answer": answer,
                },
                status=status.HTTP_200_OK,
            )

        except ResponseError:
            logger.exception("Local LLM request failed.")

            return Response(
                {
                    "error": (
                        "The local model could not process "
                        "the request. Check the model and "
                        "Ollama configuration."
                    )
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        except Exception:
            logger.exception("Expense assistant failed.")

            return Response(
                {
                    "error": (
                        "The assistant encountered an error. "
                        "Please try again."
                    )
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )