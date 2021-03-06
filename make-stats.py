import sys, argparse, collections

import database, mask

from utils import *
from units import *
from tzone import *
from localization import *
from gazetteer import *
from mlutils import *
from mlhtml import *

YEARS = [1,2,5]

ReportStruct = collections.namedtuple('ReportStruct', 'logged verified unverified males females men women sugar_pups sugar_babies sugar_daddies sugar_mommas avg_age_males avg_age_females avg_age_men avg_age_women avg_age_sugar_pups avg_age_sugar_babies avg_age_sugar_daddies avg_age_sugar_mommas white black latino indian asian mixed other active messages')

parser = argparse.ArgumentParser(description='Generate Static Pages.')
parser.add_argument('-s', metavar='title', nargs=1, help='title of page')
args = parser.parse_args()

BASE_DIR = os.path.dirname(__file__)

db = database.Database(MISS_LOOPY_DB)

now = datetime.datetime.utcnow()

years = {}
for year in YEARS:
  sql = """
    SELECT * FROM reports WHERE logged > %s ORDER BY logged
  """
  db.execute(sql, (now-datetime.timedelta(weeks=year*52),))
  years[year] = [ReportStruct(report[0].strftime('%Y-%m-%d'),*report[1:]) for report in db.fetchall()]

d = {'title':'Statistics', 'years':years}

print RenderY('stats.html', d)
