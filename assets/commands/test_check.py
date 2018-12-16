import unittest
import check

class TestPayload(unittest.TestCase):
    def setUp(self):
        self.payload = {
            "source": {
                "conduit_uri": "https://test.conduit.uri/api/",
                "conduit_token": "test-conduit-token",
                "repo_uri": "https://test.repo.uri"
            },
            "version": {
                "diff": "diffID",
                "branch": "test-branch",
                "base": "basehash",
                "rev": "Dtestrev",
            }
        }

    def test_get_from_source(self):
        self.assertEqual(check.get_token(self.payload), "test-conduit-token")
        self.assertEqual(check.get_conduit_uri(self.payload), "https://test.conduit.uri/api/")

    def test_get_from_version(self):
        self.assertEqual(check.get_last_diff_checked(self.payload), "diffID")


class TestDiff(unittest.TestCase):
    def setUp(self):
        self.diff = {
            "id": 932,
            "type": "DIFF",
            "phid": "PHID-DIFF-zbyph2rdona74vcgsu2g",
            "fields": {
                "revisionPHID": "PHID-DREV-lyl4plyiheajccqjkmo6",
                "authorPHID": "PHID-USER-oyjs33qezlnmaakylm3q",
                "repositoryPHID": "PHID-REPO-ayaleo55nfry53ns7x4m",
                "refs": [
                    {
                        "type": "branch",
                        "name": "arcpatch-D225_3"
                    },
                    {
                        "type": "base",
                        "identifier": "5666cdb29e45042565d921b0672f07814aacc06f"
                    }
                ],
                "dateCreated": 1544961500,
                "dateModified": 1544961502,
                "policy": {
                    "view": "public"
                }
            },
            "attachments": {}
        }

    def test_get_values_from_diff(self):
        self.assertEqual(check.get_diff_id(self.diff), '932')
        self.assertEqual(check.get_base(self.diff), "5666cdb29e45042565d921b0672f07814aacc06f")
        self.assertEqual(check.get_branch(self.diff), "arcpatch-D225_3")
        self.assertListEqual(check.get_revision_phids([self.diff]), ["PHID-DREV-lyl4plyiheajccqjkmo6"])


class TestRev(unittest.TestCase):
    def setUp(self):
        self.revisions = [
            {
                "id": 225,
                "type": "DREV",
                "phid": "PHID-DREV-lyl4plyiheajccqjkmo6",
                "fields": {
                    "title": "Upgrade from php 5 to php 7",
                    "authorPHID": "PHID-USER-oyjs33qezlnmaakylm3q",
                    "status": {
                        "value": "needs-review",
                        "name": "Needs Review",
                        "closed": False,
                        "color.ansi": "magenta"
                    },
                    "repositoryPHID": "PHID-REPO-ayaleo55nfry53ns7x4m",
                    "diffPHID": "PHID-DIFF-btkzxcucrjcz5feorcuv",
                    "summary": "As PHP5 gets EOL in 2018, see T2366",
                    "dateCreated": 1544179006,
                    "dateModified": 1544965192,
                    "policy": {
                        "view": "users",
                        "edit": "users"
                    }
                },
                "attachments": {}
            }
        ]

    def test_get_values_from_rev(self):
        self.assertEqual(check.get_rev_id(self.revisions[0]), "D225")

    def test_get_revisions_from_diffs(self):
        self.assertEqual(1,2)


class TestVersions(unittest.TestCase):
    def test_get_new_diffs_and_revisions_since(self):
        self.assertEqual(1,2)

    def test_get_new_versions(self):
        self.assertEqual(1,2)
    

if __name__ == '__main__':
    unittest.main()
