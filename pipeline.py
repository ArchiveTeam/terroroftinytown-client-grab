from distutils.version import StrictVersion
import socket
import sys
import time

import seesaw
from seesaw.externalprocess import ExternalProcess
from seesaw.pipeline import Pipeline
from seesaw.project import Project
from seesaw.task import SimpleTask, ConditionalTask


if StrictVersion(seesaw.__version__) < StrictVersion("0.3.1"):
    raise Exception("This pipeline needs seesaw version 0.3.1 or higher.")


# This version covers only pipeline.py and scraper.py.
# It is known as the pipeline version. Do not confuse it with the
# version in the library
# Bump it whenever a non-cosmetic change is made
VERSION = '9'
USE_SSL = True

if USE_SSL:
    TRACKER_HOST = 'tracker.archiveteam.org:1338'
else:
    TRACKER_HOST = 'tracker.archiveteam.org:1337'

USER_AGENT = ("ArchiveTeam Warrior/%s (%s %s; pipeline %s)" % (
              seesaw.__version__,
              seesaw.runner_type,
              seesaw.warrior_build,
              VERSION,
              )
              ).strip()

SCHEME = 'https' if USE_SSL else 'http'


class CheckIP(SimpleTask):
    def __init__(self):
        SimpleTask.__init__(self, "CheckIP")
        self._counter = 0

    def process(self, item):
        if self._counter <= 0:
            item.log_output('Checking IP address.')
            ip_set = set()

            ip_set.add(socket.gethostbyname('twitter.com'))
            ip_set.add(socket.gethostbyname('facebook.com'))
            ip_set.add(socket.gethostbyname('youtube.com'))
            ip_set.add(socket.gethostbyname('microsoft.com'))
            ip_set.add(socket.gethostbyname('icanhas.cheezburger.com'))
            ip_set.add(socket.gethostbyname('archiveteam.org'))

            if len(ip_set) != 6:
                item.log_output('Got IP addresses: {0}'.format(ip_set))
                item.log_output(
                    'Are you behind a firewall/proxy? That is a big no-no!')
                raise Exception(
                    'Are you behind a firewall/proxy? That is a big no-no!')

        # Check only occasionally
        if self._counter <= 0:
            self._counter = 10
        else:
            self._counter -= 1


class MaybeUpdateSubmodule(ConditionalTask):
    def __init__(self):
        ConditionalTask.__init__(self, self.is_update_needed, UpdateSubmodule())
        self.last_update = 0

    def is_update_needed(self, item):
        time_ago = time.time() - 3600

        if self.last_update < time_ago:
            item.log_output('Submodule updated scheduled.')

            self.last_update = time.time()
            return True


class UpdateSubmodule(ExternalProcess):
    NEW_ARGS = ['git', 'submodule', 'update', '--init', '--remote',
                '--recursive']
    OLD_ARGS = ['git', 'submodule', 'update', '--init', '--recursive']

    def __init__(self):
        ExternalProcess.__init__(self, 'UpdateSubmodule', self.NEW_ARGS,
                                 max_tries=5, retry_delay=2)

    def handle_process_error(self, exit_code, item):
        self.args = self.OLD_ARGS
        item.log_output('Submodule could not be automatically updated.')
        item.log_output('* It is safe to ignore the following error. *')
        ExternalProcess.handle_process_error(self, exit_code, item)


class RunScraper(ExternalProcess):
    def __init__(self):
        env = {
            'PYTHONPATH': 'terroroftinytown'
        }

        ExternalProcess.__init__(self, 'RunScraper',
            [
                sys.executable, 'scraper.py', TRACKER_HOST, VERSION,
                globals()['downloader'], globals().get('bind_address', ''),
                USER_AGENT, SCHEME
            ],
            env=env
        )


project = Project(
    title="URLTeam 2",
    project_html="""
    <img class="project-logo" alt=""
        src="https://www.archiveteam.org/images/9/9d/Urlteam-logo-reasonable-size.png"
        height="50"
    title="url shortening was a fucking awful idea" />
    <h2>URLTeam 2
        <span class="links">
            <a href="http://urlte.am/">Website</a> &middot;
            <a href="http://%s/">Leaderboard</a> &middot;
            <a href="https://www.archiveteam.org/index.php?title=URLTeam">Wiki</a>
        </span>
    </h2>
    <p>The Terror of Tiny Town</p>
    """ % (TRACKER_HOST)
)


tasks = [
    CheckIP(),
    RunScraper()
]

if globals().get('no_submodule'):
    print('Not updating submodule')
else:
    tasks.insert(0, MaybeUpdateSubmodule())


pipeline = Pipeline(*tasks)
