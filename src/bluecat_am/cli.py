import re
import click

from click import group, pass_context, option, argument
from click import Context
from bluecat_am import util, config


def validate_fqdn(ctx, param, value):
    pattern = '[\w]+(\.[\w]+)+'
    if not re.match(pattern, value):
        raise click.BadParameter('Value must be in the form: hobo.utoronto.ca')
    return value


def validate_value(ctx, param, value):
    return value


@group()
@option(
    '-s', '--silent',
    is_flag=True,
    help='Minimize the output from commands. Silence is golden',
)
@option(
    '-v', '--verbose', '--debug', 'verbose',
    is_flag=True,
    help='Show what is going on for debugging purposes'
)
@option(
        '-U', '--url',
        envvar='BAM_API_URL',
        help='Add URL on the command line',
)
@option(
        '-u', '--user',
        envvar='BAM_USER',
        default='ralph',
        help='Add Username on the command line',
)
@option(
        '-p', '--pw', '--pass', 'password',
        envvar='BAM_PW',
        help='API password',
)
@pass_context
def run(ctx: Context, silent, verbose, url, user, password):
    """ Command line interface to BAM DNS System\n
    E.g.  $bamcli add bozo.uoft.ca A 3600 10.10.10.1 [TTL]
    """
    ctx.obj = dict()
    ctx.obj['SILENT'] = silent
    ctx.obj['DEBUG'] = verbose
    config.Silent = silent
    config.Debug = verbose

    if verbose:
        click.echo('action: {}'.format(ctx.invoked_subcommand))
        click.echo('URL: {} User: {} Pw: {}'.format(url, user, password))

    util.bam_init(url, user, password)

# Define common options to share between subcommands
fqdn = argument(
    'fqdn',
    type=click.STRING,
    required=True,
    callback=validate_fqdn,
)
SUPPORTED_RR_TYPES = ['A', 'MX', 'CNAME', 'TXT', 'defRR']
rr_type = argument(
    'rr_type',
    type=click.Choice(SUPPORTED_RR_TYPES),
    default='defRR',
)
value = argument(
    'value',
    type=click.STRING,
    default='defVAL',
    callback=validate_value,
)
ttl = argument(
    'ttl',
    type=click.STRING,
    default='86400',
)
# @run commands: add, replace, delete, view, find

@run.command()
@pass_context
@fqdn
@rr_type
@value
@ttl
def add(ctx, fqdn, rr_type, value, ttl):
    """Add a new Resource Record to the BlueCat DNS system"""
    if ctx.obj['DEBUG']:
        click.echo('    fqdn: {} rr_type: {} value: {}\n'.format(fqdn, rr_type, value))

    if rr_type == 'defRR' or value == 'defVAL':
        print('Not enough RR information given')
        print('Format: bamcli {} fqdn RR_type value [ttl]'.format(ctx.command.name))
    elif rr_type == 'A':
        ips = value.split(',')
        for ip in ips:
            util.add_rr(fqdn, rr_type, ip, ttl)
    else:
        util.add_rr(fqdn, rr_type, value, ttl)


@run.command()
@pass_context
@fqdn
@rr_type
@value
@ttl
def update(ctx, fqdn, rr_type, value, ttl):
    """Update a Resource Record in the BlueCat DNS System"""
    if ctx.obj['DEBUG']:
        click.echo('    fqdn: {} rr_type: {} value: {}\n'.format(fqdn, rr_type, value))

    if rr_type == 'defRR' or value == 'defVAL':
        print('Not enough RR information given')
        print('Format: bamcli {} fqdn RR_type value'.format(ctx.command.name))
    else:
        util.update_rr(fqdn, rr_type, value, ttl)


@run.command()
@pass_context
@fqdn
@rr_type
@value
@ttl
def replace(ctx, *args, **kwargs):
    """Alias for the 'update' command"""
    ctx.forward(update)


@run.command()
@pass_context
@fqdn
@rr_type
@value
def delete(ctx, fqdn, rr_type, value):
    """Delete a Resource Record in the BlueCat DNS System"""
    if ctx.obj['DEBUG']:
        click.echo('    fqdn: {} rr_type: {} value: {}\n'.format(fqdn, rr_type, value))
    if rr_type == 'defRR':
        print('No RR type information given')
    elif rr_type == 'CNAME':
        util.delete_rr(fqdn, rr_type)
    elif value != 'defVAL':
        if rr_type == 'A':
            for val in value.split(','):
                util.delete_rr(fqdn, rr_type, val)
        else:
            util.delete_rr(fqdn, rr_type, value)
    else:
        print('Not enough RR information given')
        print('Format: bamcli {} fqdn RR_type value'.format(ctx.command.name))


@run.command()
@pass_context
@fqdn
@rr_type
@value
def remove(ctx, *args, **kwargs):
    """Alias for the 'delete' command"""
    ctx.forward(delete)


@run.command()
@pass_context
@fqdn
@rr_type
@value
def view(ctx, fqdn, rr_type, value):
    """View a Resource Record in the BlueCat DNS System"""
    if ctx.obj['DEBUG']:
        click.echo('    fqdn: {} rr_type: {} value: {}\n'.format(fqdn, rr_type, value))

    if rr_type == 'defRR':
        util.view_rr(fqdn)
    elif value == 'defVAL':
        util.view_rr(fqdn, rr_type)
    else:
        util.view_rr(fqdn, rr_type, value)


# Set custom command name so that function name doesn't override python builtin `list` function
@run.command('list')
@pass_context
@fqdn
@rr_type
@value
def list_rr(ctx, *args, **kwargs):
    """Alias for the 'view' command"""
    ctx.forward(view)


@run.command()
@pass_context
@fqdn
@rr_type
@value
def find(ctx, fqdn, rr_type, value):
    """Find a Resource Record in the BlueCat DNS System"""
    if ctx.obj['DEBUG']:
        click.echo('    fqdn: {} rr_type: {} value: {}\n'.format(fqdn, rr_type, value))

    if rr_type == 'defRR':
        ids = util.find_rr(fqdn)
    elif value == 'defVAL':
        ids = util.find_rr(fqdn, rr_type)
    else:
        ids = util.find_rr(fqdn, rr_type, value)
    print(ids)


if __name__ == '__run__':
#   run(['add', 'alex.utoronto.ca', 'A', '10.128.30.40'])
    run()
