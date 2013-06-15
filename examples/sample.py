__author__ = 'Todd Radel <tradel@appdynamics.com>'


from appd.cmdline import parse_argv
from appd.request import AppDynamicsClient

args = parse_argv()
c = AppDynamicsClient(args.url, args.username, args.password, args.account, args.verbose)
for app in c.get_applications():
    metric_data = c.get_metrics('Overall Application Performance|*', app_id=app.id)
    art = metric_data.by_leaf_name(c.AVERAGE_RESPONSE_TIME).first_value()
    cpm = metric_data.by_leaf_name(c.CALLS_PER_MINUTE).first_value()
    epm = metric_data.by_leaf_name(c.ERRORS_PER_MINUTE).first_value()
    error_pct = round(float(epm) / float(cpm) * 100.0, 1) if cpm > 0 else 0
    print app.name, art, cpm, epm, error_pct
