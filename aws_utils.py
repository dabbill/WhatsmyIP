#!/usr/bin/python3

#Obtain the current Sub_domains in route53
def aws_obtain_domains(client, hostedZoneId, domain_type):
    parsed = []
    paginator = client.get_paginator('list_resource_record_sets')
    source_zone_records = paginator.paginate(HostedZoneId = hostedZoneId)
    for record_set in source_zone_records:
        for record in record_set['ResourceRecordSets']:
            if record['Type'] == domain_type:
                parsed.append((record['Name'])[:-1])
    return parsed

# Get record value for route53 entry
def aws_route53_record_value(domain, client, hostedZoneId, record_type):
    paginator = client.get_paginator('list_resource_record_sets')
    source_zone_records = paginator.paginate(HostedZoneId = hostedZoneId)
    for record_set in source_zone_records:
        for record in record_set['ResourceRecordSets']:
            if record['Name'][:-1] == domain:
                if record['Type'] == record_type:
                    for ip in record['ResourceRecords']:
                        return(ip['Value'])

# update route53 entries
def aws_route53(domain, route53Action, comment_var, currentIP, client, hostedZoneId, record_type):
    client.change_resource_record_sets(
    HostedZoneId = hostedZoneId,
    ChangeBatch={
        'Comment': domain + comment_var,
        'Changes': [
            {
                'Action': route53Action,
                'ResourceRecordSet': {
                    'Name': domain,
                    'Type': record_type,
                    'TTL': 300,
                    'ResourceRecords': [
                        {
                            'Value': currentIP
                        },
                    ],
                }
            },
        ]
        }
    )
