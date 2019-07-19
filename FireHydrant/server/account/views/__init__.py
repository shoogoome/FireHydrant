from .list import AccountListView
from .info import AccountInfoView
from .register import AccountRegisterView
from .login import AccountLoginView

__all__ = [
    'AccountRegisterView', 'AccountLoginView',
    'AccountListView', 'AccountInfoView',
]