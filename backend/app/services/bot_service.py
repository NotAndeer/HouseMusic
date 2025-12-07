"""Simple conversational bot engine."""

from app.models.conversation import Channel, Conversation, ConversationState


class BotService:
    """Determines replies based on conversation state."""

    def handle_message(self, conversation: Conversation, message: str) -> tuple[ConversationState, str]:
        """Return next state and response for the given message."""

        if conversation.state == ConversationState.STEP_1:
            return ConversationState.STEP_2, "Gracias por contactarnos. ¿Cuál es tu email?"
        if conversation.state == ConversationState.STEP_2:
            return ConversationState.STEP_3, "¿Deseas recibir campañas?"
        return ConversationState.STEP_3, "Un asesor se comunicará contigo pronto."
