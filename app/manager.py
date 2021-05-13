from .models import Claim, ClaimFile


class ClaimManager:
    """Class to manage process of claiming"""
    model = Claim

    def __init__(self):
        self.data = None

    def start(self):
        self.data = self.model.objects.create()
