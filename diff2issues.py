# -*- coding: utf-8 -*-
import sys
import json
import time
import urllib2

token = ''

user = 'django-docs-ja'
repo = 'django-docs-ja'
milestone = 1
labels = ['enhancement']

start = 'Index: '
protocol = 'https'
domain = 'api.github.com'
issues_url = '/'.join(('%s://%s' % (protocol, domain), 'repos', user, repo,
    'issues'))


def create_issue(title, body, milestone, labels):
    issue = {
        'title': title,
        'body': body,
        'milestone': milestone,
        'labels': labels,
    }
    data = json.dumps(issue)
    request = urllib2.Request(issues_url, data=data)
    request.add_header('Authorization', 'token %s' % token)
    request.get_method = lambda: 'POST'
    response = urllib2.urlopen(request)
    return response.code == 201


def main():
    filename = None
    lines = []
    for line in file(sys.argv[1]):
        line = line.strip()
        line = line.decode('utf-8', 'replace')
        if line.startswith(start):
            if lines:
                diff = '```\n%s\n```' % '\n'.join(lines)
                success = create_issue(filename, diff, milestone, labels)
                if not success:
                    sys.stderr.write('failed to create issue: %s\n' % filename)
                filename = None
                lines = []
            filename = line[len(start):]
        if filename:
            lines.append(line)

if __name__ == '__main__':
    main()
