#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from string import Template
from datetime import datetime, timedelta
from time import mktime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from MySQLdb.cursors import DictCursor
from jinja2 import Environment, FileSystemLoader
import argparse
import smtplib
import sys
import MySQLdb


__author__ = 'Todd Radel'
__copyright__ = 'Copyright (c) 2013-2015 AppDynamics Inc.'
__version__ = '0.4.5'


def parse_argv():
    parser = argparse.ArgumentParser(add_help=False, usage='%(prog)s [options]',
                                     description='Generates an HTML audit report by querying the database '
                                                 'on an AppDynamics controller.')
    parser.add_argument('-h', '--host', dest='host',
                        default='localhost',
                        help='MySQL host name (default: %(default)s)')
    parser.add_argument('-P', '--port', dest='port',
                        type=int, default=3306,
                        help='MySQL server port (default: %(default)d)')
    parser.add_argument('-u', '--username', dest='username',
                        default='root',
                        help='MySQL user name (default: %(default)s)')
    parser.add_argument('-p', '--password', dest='password',
                        default='singcontroller',
                        help='MySQL password (default: %(default)s)')
    parser.add_argument('-d', '--database', dest='database',
                        default='controller',
                        help='MySQL database name (default: %(default)s)')
    parser.add_argument('-a', '--account', dest='account',
                        default='customer1',
                        help='Controller account name (default: %(default)s)')
    parser.add_argument('-n', '--days', dest='days',
                        type=int, default=1,
                        help='Number of days to report prior to today (default: %(default)d)')
    parser.add_argument('-i', '--ignore-user', dest='ignore_users',
                        action='append',
                        default=['system', 'singularity-agent', 'ldapsync'],
                        help='Users to filter from audit log (default: %(default)s)')
    parser.add_argument('-L', '--ignore-logins', dest='ignore_logins', action='store_true',
                        help='Ignore successful logins')
    parser.add_argument('-o' '--output', dest='outfile',
                        help='Send HTML output to a file instead of SMTP server')
    parser.add_argument('-f', '--from', dest='sender', default='help@appdynamics.com',
                        help='From address in email message (default: %(default)s)')
    parser.add_argument('-t', '--to', dest='to',
                        action='append',
                        default=['tradel@appdynamics.com'],
                        help='To address in email message (default: %(default)s)')
    parser.add_argument('-s', '--subject', dest='subject', default='Controller Audit Report',
                        help='Subject of email message (default: "%(default)s")')
    parser.add_argument('--smtp-server', dest='smtphost', default='localhost',
                        help='SMTP server to use (default: %(default)s)')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Enable verbose output')
    parser.add_argument('--help', action='help',
                        help='Display this help screen')
    return parser.parse_args()


def from_ts(ms):
    return datetime.fromtimestamp(ms / 1000)


def to_ts(dt):
    return int(mktime(dt.timetuple())) * 1000


ACTIONS = {
    'APP_ALERTS_CONFIGURATION': 'View Alerts',
    'APP_ANALYZE_HOME': 'Analyze',
    'APP_AUTOMATION_HOME': 'Automation',
    'APP_BACKEND_DASHBOARD|OVERVIEW_TAB': 'Backend Dashboard',
    'APP_BACKEND_LIST': 'Backends List',
    'APP_BASELINES': 'Baselines',
    'APP_BT_DETAIL': 'BT Dashboard',
    'APP_BT_DETAIL|OVERVIEW_TAB': 'BT Dashboard',
    'APP_BT_LIST': 'BT List',
    'APP_BT_LIST|OVERVIEW_TAB': 'BT List',
    'APP_COMPARE_METRICS': 'Correlation Analysis',
    'APP_COMPONENT_MANAGER': 'Tier Dashboard',
    'APP_COMPONENT_MANAGER|OVERVIEW_TAB': 'Tier Dashboard',
    'APP_CONFIGURATION': 'Configure',
    'APP_CONFIGURATION_ACTIONS': 'Actions',
    'APP_CONFIGURATION_HOME': 'Configure',
    'APP_CPU_VS_LOAD': 'Scalability Analysis',
    'APP_DASHBOARD': 'Application Dashboard',
    'APP_DASHBOARD|OVERVIEW_TAB': 'Application Dashboard',
    'APP_DATABASE_LIST': 'Databases',
    'APP_ENVIRONMENT_PROPERTIES'
    'APP_ERRORS': 'Errors',
    'APP_ERRORS|OVERVIEW_TAB': 'Errors',
    'APP_EVENTSTREAM_LIST': 'Events',
    'APP_IIS_APP_POOLS': 'IIS App Pools',
    'APP_INCIDENT_LIST': 'Policy Violations',
    'APP_INFO_POINT_LIST': 'Information Points',
    'APP_INFRA_MESSAGE_SERVERS': 'Message Servers',
    'APP_INFRA_OTHER_SERVERS': 'Other Backends',
    'APP_INFRASTRUCTURE': 'Servers',
    'APP_NODE_MANAGER': 'Node Dashboard',
    'APP_NODE_MANAGER|OVERVIEW_TAB': 'Node Dashboard',
    'APP_POLICY_LIST': 'Policies',
    'APP_RELEASE_ANALYSIS': 'Compare Releases',
    'APP_REPORTING': 'Reports',
    'APP_REQUEST_LIST': 'Requests',
    'APP_RESPONSE_TIME_VS_LOAD': 'Scalability Analysis',
    'APP_SCHEDULE_LIST': 'Schedules',
    'APP_SERVER_HOME': 'Home',
    'APP_SLOW_RESPONSE_TIMES': 'Slow Response times',
    'APP_TASK_LIST': 'Tasks',
    'APP_THRESHOLD_LIST': 'Thresholds',
    'APP_TROUBLESHOOT_HOME': 'Troubleshooting',
    'APP_WORKFLOW_EXECUTION_LIST': 'Workflow Executions',
    'APP_WORKFLOW_LIST': 'Workflows',
    'FLOW_ICON_MOVED': 'Flow Map Changed',
    'LOGIN': 'Login Success',
    'LOGIN_FAILED': 'Login Failure',
    'OBJECT_CREATED': 'Object Created',
    'OBJECT_DELETED': 'Object Deleted',
    'OBJECT_UPDATED': 'Object Changed',
    'USER_PASSWORD_CHANGED': 'Password Changed'
}

AUDIT_TABLES = {
    'AGENT_CONFIGURATION': {'select_expr': "CONCAT(t.agent_type, ' ', t.entity_type)",
                            'display_name': 'Agent Configuration'},
    'APPLICATION': {'display_name': 'Application',
                    'app_name_expr': 'name',
                    'app_id_expr': 'id'},
    'APPLICATION_COMPONENT_NODE': {'display_name': 'Node',
                                   'app_name_expr': 'NULL',
                                   'app_id_expr': 'NULL'},
    'APPLICATION_COMPONENT': {'display_name': 'Tier'},
    'APPLICATION_DIAGNOSTIC_DATA': {},
    'BACKEND_DISCOVERY_CONFIG': {'display_name': 'Backend Detection Config'},
    'BUSINESS_TRANSACTION': {'join_to': 'abusiness_transaction',
                             'display_name': 'Business Transaction'},
    'BUSINESS_TRANSACTION_GROUP': {'join_to': 'abusiness_transaction',
                                   'display_name': 'Business Transaction Group'},
    'CALL_GRAPH_CONFIGURATION': {'select_expr': "'CALL_GRAPH_CONFIGURATION'",
                                 'display_name': 'Call Graph Config'},
    'CUSTOM_EXIT_POINT_DEFINITION': {'display_name': 'Custom Backend Config'},
    'CUSTOM_MATCH_POINT_DEFINITION': {'select_expr': "CONCAT(t.name, ' [', t.entry_point_type, ']')",
                                      'display_name': 'Custom Entry Point'},
    'DASHBOARD': {'display_name': 'Custom Dashboard'},
    'DOT_NET_ERROR_CONFIGURATION': {'select_expr': "'DOT_NET_ERROR_CONFIGURATION'",
                                    'join_to': 'dotnet_error_configuration',
                                    'display_name': 'Error Detection Config [.NET]'},
    'ERROR_CONFIGURATION': {'select_expr': "'ERROR_CONFIGURATION'",
                            'display_name': 'Error Detection Config'},
    'EUM_CONFIGURATION': {'select_expr': "'EUM_CONFIGURATION'",
                          'display_name': 'EUM Config'},
    # 'GLOBAL_CONFIGURATION': ('name', 'GLOBAL_CONFIGURATION'),
    'HTTP_REQUEST_DATA_GATHERER_CONFIG': {'join_to': 'adata_gatherer_config',
                                          'display_name': 'HTTP Data Collector Config'},
    'JMX_CONFIG': {'join_to': 'jmx_rule'},
    'MEMORY_CONFIGURATION': {'select_expr': "'MEMORY_CONFIGURATION'",
                             'display_name': 'Memory Monitoring Config'},
    'POJO_DATA_GATHERER_CONFIG': {'join_to': 'adata_gatherer_config',
                                  'display_name': 'Custom Method Collector Config'},
    'POLICY': {'display_name': 'Policy'},
    # 'RULE': ('name', 'RULE'),
    'SQL_DATA_GATHERER_CONFIG': {'join_to': 'adata_gatherer_config',
                                 'display_name': 'SQL Data Collector Config'},
    'TRANSACTION_MATCH_POINT_CONFIG': {'display_name': 'Transaction Detection Config'},
    'USER': {'display_name': 'User'},
}

ENTITY_TYPES = {'APPLICATION': {'display_name': 'Application',
                                'app_name_expr': 't.name',
                                'app_id_expr': 't.id'},
                'APPLICATION_COMPONENT': {'display_name': 'Tier'},
                'APPLICATION_COMPONENT_NODE': {'display_name': 'Node'}}


def connect(args):
    conn = MySQLdb.connect(args.host, args.username, args.password, args.database, args.port,
                           cursorclass=DictCursor)
    cur = conn.cursor()
    return conn, cur


def create_temp_table(cur):
    try:
        sql = """
        CREATE TEMPORARY TABLE audit_report (
            ts_ms bigint,
            account_name varchar(100),
            account_id int,
            user_name varchar(100),
            user_security_provider_type varchar(25),
            user_id int,
            object_name varchar(100),
            object_id int,
            application_name varchar(100),
            application_id int,
            action varchar(100),
            execution_time_ms bigint,
            object_desc varchar(1000),
            INDEX ts_ms (ts_ms)) ENGINE=memory DEFAULT CHARSET=utf8;
        """
        cur.execute(sql)
    except:
        print("*** ERROR creating temporary table", file=sys.stderr)
        raise


def insert_object_crud(cur, params):
    try:
        for table_name, table_data in AUDIT_TABLES.items():
            params.update({
                'table_name': table_name,
                'id_field': table_data.get('id_field', 'id'),
                'select_expr': table_data.get('select_expr', 'name'),
                'app_name_expr': table_data.get('app_name_expr', 'NULL'),
                'app_id_expr': table_data.get('app_id_expr', 'NULL'),
                'join_to': table_data.get('join_to', table_name),
            })

            sql = """
            INSERT INTO audit_report
            (SELECT ca.ts_ms, ca.account_name, ca.account_id, ca.user_name, ca.user_security_provider_type,
                ca.user_id, ca.object_name, ca.object_id, $app_name_expr, $app_id_expr,
                ca.action, ca.execution_time_ms,
                $select_expr
            FROM controller_audit ca
            JOIN $join_to t ON ($id_field = ca.object_id)
            WHERE LOWER(ca.account_name) = LOWER('$acct')
              AND LOWER(ca.object_name) = '$table_name'
              AND ca.action LIKE 'OBJECT%'
              AND ca.object_name NOT IN ('AGENT_CONFIGURATION')
              AND ca.user_name NOT IN ($users_to_ignore)
              AND ca.ts_ms BETWEEN $start_ts AND $end_ts
            ORDER BY ca.ts_ms)
        """
            sql = Template(sql).substitute(params)
            cur.execute(sql)
    except:
        print("*** ERROR EXECUTING SQL: ", sql, file=sys.stderr)
        raise


def insert_agent_configuration_crud(cur, params):
    try:
        for entity_type, entity_data in ENTITY_TYPES.items():
            params.update({
                'entity_type': entity_type,
                'app_name_expr': entity_data.get('app_name_expr', 'NULL'),
                'app_id_expr': entity_data.get('app_id_expr', 'NULL'),
                'display_name': entity_data.get('display_name', entity_type)
            })
            sql = """
        INSERT INTO audit_report
        (SELECT ca.ts_ms, ca.account_name, ca.account_id, ca.user_name, ca.user_security_provider_type,
               ca.user_id, ca.object_name, ca.object_id, $app_name_expr, $app_id_expr, ca.action, ca.execution_time_ms,
               CONCAT('$display_name', ' ', t.name) AS display_name
                FROM controller_audit ca
                JOIN agent_configuration ac ON (ac.id = ca.object_id)
                JOIN $entity_type t ON (t.id = ac.entity_id)
                WHERE LOWER(ca.account_name) = LOWER('$acct')
                  AND LOWER(ca.object_name) = 'AGENT_CONFIGURATION'
                  AND ca.action LIKE 'OBJECT%%'
                  AND ca.user_name NOT IN ($users_to_ignore)
                  AND ca.ts_ms BETWEEN $start_ts AND $end_ts
                ORDER BY ca.ts_ms)
        """
            sql = Template(sql).substitute(params)
            cur.execute(sql)
    except:
        print("*** ERROR EXECUTING SQL: ", sql, file=sys.stderr)
        raise


def insert_logins(cur, params):
    try:
        sql = """
        INSERT INTO audit_report
        (SELECT ca.ts_ms, ca.account_name, ca.account_id, ca.user_name, ca.user_security_provider_type,
           ca.user_id, ca.object_name, ca.object_id, NULL, NULL, ca.action, ca.execution_time_ms,
           NULL AS display_name
            FROM controller_audit ca
            WHERE LOWER(ca.account_name) = LOWER('$acct')
              AND ca.action IN ($login_types)
              AND ca.user_name NOT IN ($users_to_ignore)
              AND ca.ts_ms BETWEEN $start_ts AND $end_ts
            ORDER BY ca.ts_ms)
    """
        sql = Template(sql).substitute(params)
        cur.execute(sql)
    except:
        print("*** ERROR EXECUTING SQL: ", sql, file=sys.stderr)
        raise


def select_results(cur):
    sql = """
    SELECT ts_ms, account_name, account_id, user_name, user_security_provider_type,
        user_id, object_name, object_id, application_id, action, execution_time_ms, object_desc
    FROM audit_report
    ORDER BY ts_ms
    """
    cur.execute(sql)


def generate_output(args, params):
    env = Environment(loader=FileSystemLoader(['templates', 'appd/reports/templates', '.']))
    template = env.get_template('audit.jinja.html')
    return template.render(params)


def populate_params(args):
    end_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_time = end_time + timedelta(-args.days)
    login_types = ['LOGIN_FAILED']
    if not args.ignore_logins:
        login_types.append('LOGIN')
    return {
        'end_time': end_time,
        'start_time': start_time,
        'start_ts': to_ts(start_time),
        'end_ts': to_ts(end_time),
        'acct': args.account,
        'users_to_ignore': ', '.join(["'" + x + "'" for x in args.ignore_users]),
        'login_types': ', '.join(["'" + x + "'" for x in login_types])
    }


def send_html_email(args, html):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = args.subject
    msg['From'] = args.sender
    msg['To'] = ', '.join(args.to)

    part1 = MIMEText('Please use an HTML email client to view this message.', 'plain')
    part2 = MIMEText(html, 'html', 'utf-8')
    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP(args.smtphost)
    if args.verbose:
        s.set_debuglevel(1)
    s.sendmail(args.sender, args.to, msg.as_string())
    s.close()


if __name__ == '__main__':

    args = parse_argv()
    params = populate_params(args)

    (conn, cur) = connect(args)

    create_temp_table(cur)
    insert_object_crud(cur, params)
    insert_agent_configuration_crud(cur, params)
    insert_logins(cur, params)
    select_results(cur)

    start_time = params['start_time']
    end_time = params['end_time']
    html = generate_output(args, locals())
    conn.close()

    if args.outfile:
        with open(args.outfile, 'w') as f:
            f.write(html)
    else:
        send_html_email(args, html)

