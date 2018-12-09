from phabricator import Phabricator
import sys
import json

def get_value_from_payload(value, payload, field):
    try:
        return payload[field][value]
    except KeyError:
        raise KeyError(f'{value} not found')

def get_token(payload):
    return get_value_from_payload('token', payload, 'source')

def get_uri(payload):
    return get_value_from_payload('uri', payload, 'source')

def get_last_diff_checked(payload):
    try:
        return get_value_from_payload('diff', payload, 'version')
    except KeyError:
        return None

def get_diff_id(diff):
    return diff.get('id')

def get_rev_id(revision):
    return "D" + str(revision.get("id")) if revision else None

def get_rev_title(revision):
    return revision.get('fields').get('title') if revision else None

def get_branch(diff):
    for ref in diff.get('fields').get('refs'):
        if ref.get('type') == "branch":
            return ref.get('name')

def get_revision(revision_phid, phab):
    return phab.differential.revision.search(constraints={'phids':[revision_phid]}).get('data')[0] if revision_phid else None

def get_revisions_from_diffs(diffs, phab):
    return [get_revision(phid, phab) for phid in get_revision_phids(diffs)]

def get_revision_phid(diff):
    return diff.get('fields',[]).get('revisionPHID')

def get_revision_phids(diffs):
    return [get_revision_phid(diff) for diff in diffs]

def get_new_diffs_and_revisions_since(diff, phab):
    if diff:
        return get_diffs_and_revisions_since(diff, phab)
    else:
        return get_latest_diff_and_revision(phab)

def get_latest_diff_and_revision(phab):
    latest_diff = phab.differential.diff.search(limit=1).get('data')
    latest_diff_revision = get_revisions_from_diffs(latest_diff, phab)
    return latest_diff, latest_diff_revision

def get_diffs_and_revisions_since(diff, phab):
    new_diffs = phab.differential.diff.search(order=["-id"], after=diff-1).get('data')
    new_diffs_revisions = get_revisions_from_diffs(new_diffs, phab)
    return new_diffs, new_diffs_revisions

def get_phabricator(payload):
    uri = get_uri(payload)
    uri = uri if uri.endswith("/") else uri + "/"
    api_uri = uri if uri.endswith("api/") else uri + "api/"
    token = get_token(payload)
    phab = Phabricator(host=api_uri, token=token)
    phab.update_interfaces()
    return phab

def concourse_version(diff, rev):
    return {
        'diff': get_diff_id(diff),
        'branch': get_branch(diff),
        'rev': get_rev_id(rev),
        'revisionName': get_rev_title(rev)
    }

def get_new_versions(last_checked_diff, phab):
    new_diffs, revisions = get_new_diffs_and_revisions_since(last_checked_diff, phab)
    return [concourse_version(diff, rev) for diff, rev in zip(new_diffs, revisions)]


if __name__ == "__main__":
    payload = json.loads(input())
    phab = get_phabricator(payload)
    last_checked_diff = get_last_diff_checked(payload)
    new_versions = get_new_versions(last_checked_diff, phab)
    print(json.dumps(new_versions))
