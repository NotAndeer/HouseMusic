"""SQLAlchemy base module.

The declarative ``Base`` is shared by all ORM models. Importing the models
here ensures Alembic can auto-detect migrations without scanning the entire
project manually.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models for Alembic's autogenerate feature. These imports are unused
# at runtime but allow migration tools to pick up metadata from all models.
from app.models.user import User  # noqa: F401,E402
from app.models.campaign import Campaign, CampaignChannel  # noqa: F401,E402
from app.models.social_account import SocialAccount  # noqa: F401,E402
from app.models.conversation import Conversation  # noqa: F401,E402
from app.models.message_log import MessageLog  # noqa: F401,E402
from app.models.contact import Contact  # noqa: F401,E402
from app.models.contact_source import ContactSource  # noqa: F401,E402
from app.models.interaction_event import InteractionEvent  # noqa: F401,E402
