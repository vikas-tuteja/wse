from utils import getattrd

class AccessToAView(object):
    """
    maintains a list of page that is accessible to each user type
    and returns its acceiblity accordingly

    """

    def __init__(self, user_type, page):
        self.user_type = getattrd(user_type, 'userdetail.type.slug', None)
        self.page = page


    def is_accessible(self):
        """
        returns true if a page is accessible to a view

        """
        if self.user_type == 'client':
            if self.page in ('post_events',):
                return True

        elif self.user_type == 'candidate':
            if self.page in ('event_listing', 'apply_requirement'):
                return True

        else:
            return True

        return False
