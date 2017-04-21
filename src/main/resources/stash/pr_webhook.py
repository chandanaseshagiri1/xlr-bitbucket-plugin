#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#


from com.xebialabs.xlrelease.api.v1.forms import StartRelease
from java.util import HashMap


def handle_request(event, template_filter = None):
    
    print event
    print template_filter
    logger.info(str(event))
    #try:
    #    if event["push"]:
    #        logger.info("Found push event for template %s " % template_filter)
    #        handle_push_event(event, template_filter)
    #except:
    #    e = sys.exc_info()[1]
    #    msg = ("Could not parse payload, check your Bitbucket Webhook "
    #           "configuration. Error: %s. Payload:\n%s" % (e, event))
    #    logger.warn(msg)
    #    return

def handle_push_event(event, template_filter):
    proj_name = event['proj']
    repo_name = event["repository"]
    pr_number = event['pr_number']
    pr_title = event['pr_title']
    comment = event['comment']
    source_hash = event['source_hash']
    target_hash = event['target_hash']
    start_pr_release(proj_name, repo_name, pr_number, pr_title, comment, source_hash,target_hash, template_filter)


def start_new_branch_release(repo_full_name, branch_name, current_commit_hash, template_filter = None):
    templates = templateApi.getTemplates(template_filter)
    if not templates:
        raise Exception('Could not find any templates by tag [pull_request_merger]. '
                        'Did the xlr-development-workflow-plugin initializer run?')
    else:
        if len(templates) > 1:
            logger.warn("Found more than one template with tag '%s', using the first one" % template_filter)
        template_id = templates[0].id

    params = StartRelease()
    params.setReleaseTitle("Release for BRANCH: %s/%s" % (repo_full_name,branch_name))
    variables = HashMap()
    variables.put('${repo_full_name}', '%s' % repo_full_name)
    variables.put('${branch_name}', '%s' % branch_name)
    variables.put('${current_commit_hash}', '%s' % current_commit_hash)
    params.setReleaseVariables(variables)
    started_release = templateApi.start(template_id, params)
    response.entity = started_release
    logger.info("Started Release %s for BRANCH: %s/%s" % (started_release.getId(), repo_full_name, branch_name))


def start_pr_release(proj_name, repo_name, pr_number, pr_title, comment, source_hash,target_hash, tag = 'pull_request_merger'):
    pr_templates = templateApi.getTemplates(tag)
    if not pr_templates:
        raise Exception('Could not find any templates by tag [pull_request_merger]. '
                        'Did the xlr-development-workflow-plugin initializer run?')
    else:
        if len(pr_templates) > 1:
            logger.warn("Found more than one template with tag '%s', using the first one" % tag)
        template_id = pr_templates[0].id

    params = StartRelease()
    params.setReleaseTitle('Pull Request #%s: %s' % (pr_number, pr_title))
    variables = HashMap()
    variables.put('${pull_request_number}', '%s' % pr_number)
    variables.put('${pull_request_title}', '%s' % pr_title)
    variables.put('${repository_name}', '%s' % repo_name)
    variables.put('${pull_request_comment}', '%s' % comment)
    variables.put('${proj_name}', '%s' % proj_name)
    variables.put('${source_hash}', '%s' % source_hash)
    variables.put('${target_hash}', '%s' % target_hash)
    params.setReleaseVariables(variables)
    started_release = templateApi.start(template_id, params)
    response.entity = started_release
    logger.info("Started release %s for Pull Request %s" % (started_release.getId(), pr_number))

handle_request(request.entity, request.query['template'])
