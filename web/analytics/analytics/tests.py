#utf-8

import unittest

from pyramid import testing
from mocker import (
                 Mocker,
                 ANY,
                 ARGS
                 )

import domain

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from .views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'analytics')


class RecorderTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

        # Journal Assets
        self._journal_assets_code = {"uid": "1807-8621"}
        self._journal_assets = {
                                "region": "bra",
                                }

        # Issue Assets
        self._issue_assets_code = {"uid": "e0ffe7251bf22c6220e437c0ab16a720"}
        self._issue_assets = {
                                "journal_id": "1807-8621",
                                "region": "bra"
                            }

        # Article Assets
        # raindistributionintangaradaserra,mid-northernmatogrossostate,brazilrivanildodallacort
        self._article_assets_code = {"uid": "15490819d7d0dde7a5ee37bfcf5241b8"}
        self._article_assets = {
                                "journal_id": "1807-8621", #  Latindex journa ID
                                "issue_id": "15490819d7d0dde7a5ee37bfcf5241b8", #  1807-8621201100020001
                                "region": "bra"
                                }

        # PDF Assets
        # raindistributionintangaradaserra,mid-northernmatogrossostate,brazilrivanildodallacort
        self._pdf_assests_id = {"uid": "15490819d7d0dde7a5ee37bfcf5241b8"}
        self._pdf_assests = {
                                "journal_id": "1807-8621", #  Latindex journa ID
                                "issue_id": "e0ffe7251bf22c6220e437c0ab16a720", #  1807-8621201100020001
                                "region": "bra"
                            }

    def tearDown(self):
        testing.tearDown()

    def test_record_article(self):
        import copy
        request = testing.DummyRequest()

        # MongoDB Connection Mocker
        mocker = Mocker()
        dummy_mongodb = mocker.mock()
        dummy_mongodb_conn = mocker.mock()
        dummy_mongodb_db = mocker.mock()
        dummy_mongodb_col = mocker.mock()

        dummy_mongodb.Connection(ANY)
        mocker.result(dummy_mongodb_conn)

        dummy_mongodb_conn['analytics']
        mocker.result(dummy_mongodb_db)

        dummy_mongodb_db['accesses']
        mocker.result(dummy_mongodb_col)

        dummy_mongodb_col.update(ANY, ARGS)
        mocker.result(dummy_mongodb_col)

        dummy_mongodb_col.update(self._article_assets_code, self._article_assets, True)
        mocker.replay()

        conn = dummy_mongodb.Connection('localhost')

        request['db'] = conn['analytics']
        request['subpath'] = (u'v1', u'article')

        rec = domain.Recorder(request)

        # Testing with valid data and code
        self.assertTrue(rec.record_article(self._article_assets_code, self._article_assets))

        # Testing with invalid code
        self.assertFalse(rec.record_article("", self._article_assets))

        # Testing with invalid data
        self.assertFalse(rec.record_article(self._article_assets_code, ""))

        # Testing empty journal_id
        x = copy.deepcopy(self._article_assets)
        del(x['journal_id'])
        self.assertFalse(rec.record_article(self._article_assets_code, x))

        # Testing empty issue_id
        x = copy.deepcopy(self._article_assets)
        del(x['issue_id'])
        self.assertFalse(rec.record_article(self._article_assets_code, x))

        # Testing empty region
        x = copy.deepcopy(self._article_assets)
        del(x['region'])
        self.assertFalse(rec.record_article(self._article_assets_code, x))

    def test_record_journal(self):
        request = testing.DummyRequest()

        request['subpath'] = (u'v1', u'journal')

        rec = domain.Recorder(request)

        pass

    def test_record_issue(self):
        request = testing.DummyRequest()

        request['subpath'] = (u'v1', u'issue')

        rec = domain.Recorder(request)

        pass

    def test_record_pdf(self):
        request = testing.DummyRequest()

        request['subpath'] = (u'v1', u'pdf')

        rec = domain.Recorder(request)

        pass

    def test_is_allowed_domain(self):
        pass
