from phabricator import Phabricator
import sys
import json

def get_value_from_payload(value, payload, field):
    if payload:
        try:
            return payload[field][value] if payload[field] else None
        except KeyError:
            raise KeyError(f'{value} not found')

def get_token(payload):
    return get_value_from_payload('conduit_token', payload, 'source')

def get_conduit_uri(payload):
    return get_value_from_payload('conduit_uri', payload, 'source')

def get_last_diff_checked(payload):
    try:
        return get_value_from_payload('diff', payload, 'version')
    except KeyError:
        return None

def get_diff_id(diff):
    return str(diff.get('id'))

def get_rev_id(revision):
    return "D" + str(revision.get("id")) if revision else None

def get_base(diff):
    for ref in diff.get('fields').get('refs'):
        if ref.get('type') == "base":
            return ref.get('identifier')

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

def get_new_diffs_and_revisions_since(diff, repo_PHID, phab):
    if diff:
        return get_diffs_and_revisions_since(diff, repo_PHID, phab)
    else:
        return get_latest_diff_and_revision(phab, repo_PHID)

def get_latest_diff_and_revision(phab, repo_PHID):
    latest_diffs = phab.differential.diff.search(limit=1).get('data')
    latest_diff_for_repo = filter_diffs_for_repo(latest_diffs, repo_PHID)  # if latest diff was not for repo return nothing for now
    latest_diff_revision = get_revisions_from_diffs(latest_diff_for_repo, phab)
    return latest_diff_for_repo, latest_diff_revision

def get_diffs_and_revisions_since(diff_id, repo_PHID, phab):
    new_diffs = phab.differential.diff.search(order=["-id"], after=int(diff_id)-1).get('data')
    new_diffs_for_repo = filter_diffs_for_repo(new_diffs, repo_PHID)
    new_diffs_revisions = get_revisions_from_diffs(new_diffs_for_repo, phab)
    return new_diffs_for_repo, new_diffs_revisions

def filter_diffs_for_repo(diffs, repo_PHID):
    return [diff for diff in diffs if diff.get('fields').get('repositoryPHID') == repo_PHID]

def get_phabricator(payload):
    api_uri = get_conduit_uri(payload)
    token = get_token(payload)
    phab = Phabricator(host=api_uri, token=token)
    phab.update_interfaces()
    return phab

def concourse_version(diff, rev):
    return {
        'diff': get_diff_id(diff),
        'branch': get_branch(diff),
        'base': get_base(diff),
        'rev': get_rev_id(rev),
    }

def get_new_versions(last_checked_diff, repo_PHID, phab):
    new_diffs, revisions = get_new_diffs_and_revisions_since(last_checked_diff, repo_PHID, phab)
    return [concourse_version(diff, rev) for diff, rev in zip(new_diffs, revisions) if rev]

def get_repo_PHID(payload, phab):
    repo_uri = get_repo_uri(payload)
    return phab.diffusion.repository.search(constraints={'uris':[repo_uri]}).get('data')[0].get('phid')
   
def get_repo_uri(payload):
    return get_value_from_payload('repo_uri', payload, 'source')

if __name__ == "__main__":
    payload = json.loads(input())
    phab = get_phabricator(payload)
    last_checked_diff = get_last_diff_checked(payload)
    repo_PHID = get_repo_PHID(payload, phab)
    new_versions = get_new_versions(last_checked_diff, repo_PHID, phab)
    print(json.dumps(new_versions))
