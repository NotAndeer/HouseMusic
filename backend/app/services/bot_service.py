"""Simple conversational bot engine."""

from app.models.conversation import Channel, Conversation, ConversationState


class BotService:
    """Determines replies based on conversation state."""

    def handle_message(self, conversation: Conversation, message: str) -> tuple[ConversationState, str]:
        """Return next state and response for the given message."""
        message_lower = message.strip().lower()

        if conversation.state == ConversationState.STEP_1:
            return ConversationState.STEP_2, "Gracias por contactarnos. ¿Cuál es tu email?"

        if conversation.state == ConversationState.STEP_2:
            return ConversationState.STEP_3, "¿Deseas recibir campañas? (Responde sí o no)"

        if conversation.state == ConversationState.STEP_3:
            if message_lower in ("sí", "si", "yes", "y"):
                return ConversationState.STEP_3, "¡Perfecto! Te mantendremos informado."
            elif message_lower in ("no", "n"):
                return ConversationState.STEP_3, "Entendido. No recibirás campañas promocionales."
            else:
                return ConversationState.STEP_3, "Por favor, responde 'sí' o 'no'."

        # Fallback for unknown states
        return ConversationState.STEP_3, "Un asesor se comunicará contigo pronto."