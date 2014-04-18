from distutils.version import StrictVersion
import seesaw
from seesaw.externalprocess import ExternalProcess
from seesaw.pipeline import Pipeline
from seesaw.project import Project
from seesaw.task import SimpleTask
import socket
import sys


if StrictVersion(seesaw.__version__) < StrictVersion("0.1.7"):
    raise Exception("This pipeline needs seesaw version 0.1.7 or higher.")


VERSION = "2014MMDD.XX"
TRACKER_HOST = 'TRACKER_HOSTNAME_HERE'


class CheckIP(SimpleTask):
    def __init__(self):
        SimpleTask.__init__(self, "CheckIP")
        self._counter = 0

    def process(self, item):
        if self._counter <= 0:
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


class UpdateSubmodule(ExternalProcess):
    def __init__(self):
        ExternalProcess.__init__(self, 'UpdateSubmoule',
            ['git', 'submodule', 'update', '--init', '--recursive']
        )


class RunScraper(ExternalProcess):
    def __init__(self):
        ExternalProcess.__init__(self, 'RunScraper',
            [sys.executable, 'scraper.py', TRACKER_HOST, VERSION,
                globals()['downloader'], globals().get('bind_address', '')]
        )


project = Project(
    title="URLTeam",
    project_html="""
    <img class="project-logo" alt=""
        src="http://archiveteam.org/images/9/97/Urlteam-logo.png" height="50"
    title="" />
    <h2><span class="links">
        <a href="http://urlte.am/">Website</a> &middot;
        <a href="http://%s/">Leaderboard</a></span></h2>
    <p><b>URLTeam</b>.</p>
    """ % (TRACKER_HOST)
)


tasks = [
    CheckIP(),
    RunScraper()
]

if globals().get('no_submodule'):
    print('Not updating submodule')
else:
    tasks.insert(0, UpdateSubmodule())


pipeline = Pipeline(*tasks)
