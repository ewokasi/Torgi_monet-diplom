from .short_get_all import short_get_all
from .autoset_active_status import autoset_active_status
async def update_all():
    auctioons = await short_get_all()
    for a in auctioons:
        if 'deleted' not in a:
            await autoset_active_status(a["a_id"])
