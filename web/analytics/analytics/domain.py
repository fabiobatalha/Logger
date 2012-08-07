

class Recorder(object):

    def __init__(self, request):
        self._request = request

    def _record(self, uid="", data=""):
        self._request['db']['accesses'].update(uid, data, True)

    def record_article(self, uid="", data=""):

        # Checking if there is a valid uid.
        if not 'uid' in uid:
            return False
        else:
            if len(uid['uid']) == 0:
                return False

        mandatory_data = ('journal_id', 'issue_id', 'region')
        for i in mandatory_data:
            if not i in data:
                return False

        self._record(uid, data)

        return True
