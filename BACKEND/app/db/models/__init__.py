"""Import every model module so Base.metadata is complete for Alembic."""

from . import (
    activity,
    ai,
    analytics,
    assessment,
    billing,
    communication,
    content,
    governance,
    gamification,
    identity,
    knowledge,
    personalization,
    taxonomy,
    video,
)
from .activity import *  # noqa: F401,F403
from .ai import *  # noqa: F401,F403
from .analytics import *  # noqa: F401,F403
from .assessment import *  # noqa: F401,F403
from .billing import *  # noqa: F401,F403
from .communication import *  # noqa: F401,F403
from .content import *  # noqa: F401,F403
from .governance import *  # noqa: F401,F403
from .gamification import *  # noqa: F401,F403
from .identity import *  # noqa: F401,F403
from .knowledge import *  # noqa: F401,F403
from .personalization import *  # noqa: F401,F403
from .taxonomy import *  # noqa: F401,F403
from .video import *  # noqa: F401,F403

__all__ = [
    name
    for name in globals()
    if not name.startswith("_") and name not in {"activity", "ai", "analytics", "assessment", "billing", "communication", "content", "governance", "gamification", "identity", "knowledge", "personalization", "taxonomy", "video"}
]