import click
import subprocess

from settings import save_settings


@click.command()
@click.option('--chunk-size', default=5, help='Number of chunks to divide article searching into.')
@click.option('--lazy-factor', default=1, help='Sleep times are multiplied by this number.')
@click.option('--alert-server-port', default=1111, help='Which port should the alert server run on?')
@click.option('--graphql-server-port', default=5001, help='Which port should graphql server run on?')
@click.option('--graphql-server-host', default='localhost', help='Which host is graphql server running on? (setting is consumed by React)')
def run(chunk_size, lazy_factor, alert_server_port, graphql_server_port, graphql_server_host):
    """This script runs whole ecosystem of this scraper on different screens."""
    # write settings to file
    save_settings(chunk_size, lazy_factor, alert_server_port, graphql_server_port, graphql_server_host)

    # actually run the bash script
    subprocess.call('./run.sh')

    print('Scraper is running. Screen instances are up.\nYou can check them out with screen -ls')


if __name__ == '__main__':
    run()
