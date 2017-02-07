import json

import pytest

from django.core.urlresolvers import reverse

from csp_report.models import CSPReport, CleanedCSPReport, CSPReportFilter
from csp_report.utils import process_scp_report


@pytest.mark.urls('csp_report.tests.test_urls')
@pytest.mark.django_db(transaction=True)
def csp_report_view_test(client):
    # wrong request method
    response = client.get(reverse('csp_report_view'))
    assert response.status_code == 405

    # required fields
    response = client.post(
        reverse('csp_report_view'),
        data=json.dumps({'csp-report': {'test': 'test'}}),
        content_type='application/json',
    )
    assert response.status_code == 422

    response = client.post(
        reverse('csp_report_view'),
        data=json.dumps({'csp-report': {'document-uri': '/d-uri', 'blocked-uri': '/b-uri'}}),
        content_type='application/json',
    )
    assert response.status_code == 200


@pytest.mark.django_db(transaction=True)
def process_csp_report_test():
    with pytest.raises(TypeError):
        process_scp_report('this is not dict')

    with pytest.raises(KeyError):
        process_scp_report({})

    data = {'document-uri': '/d-uri', 'blocked-uri': '/b-uri', 'referrer': 'referrer'}
    process_scp_report(data, host='test_host')
    report = CSPReport.objects.all()[0]
    assert report.document_uri == '/d-uri' and report.blocked_uri == '/b-uri'
    assert report.host == 'test_host'
    assert report.referrer == 'referrer'
    assert report.body == data


@pytest.mark.urls('csp_report.tests.test_urls')
@pytest.mark.django_db(transaction=True)
def csp_filter_empty_test(client):
    response = client.post(
        reverse('csp_report_view'),
        data=json.dumps({'csp-report': {'document-uri': '/d-uri', 'blocked-uri': 'gsa://onpageload'}}),
        content_type='application/json',
    )
    assert response.status_code == 200
    assert CSPReport.objects.count() == 1
    assert CleanedCSPReport.objects.count() == 1


@pytest.mark.urls('csp_report.tests.test_urls')
@pytest.mark.django_db(transaction=True)
def csp_filter_startswith_test(client):
    CSPReportFilter.objects.create(filter_type='startswith', value='gsa://onpageload')
    response = client.post(
        reverse('csp_report_view'),
        data=json.dumps({'csp-report': {'document-uri': '/d-uri', 'blocked-uri': 'gsa://onpageload'}}),
        content_type='application/json',
    )
    assert response.status_code == 200
    assert CSPReport.objects.count() == 1
    assert CleanedCSPReport.objects.count() == 0
