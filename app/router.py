from app.page import (home_page)
from app.layout import (base_layout)
ROUTES=[
    {
        'path': '/',
        'component': home_page,
        'label': 'Home',
        'layout': base_layout,
    }
]