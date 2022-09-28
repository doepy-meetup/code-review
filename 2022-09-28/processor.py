from pathlib import Path
from re import compile as re_compile
from dataclasses import dataclass
from datetime import datetime
from collections import namedtuple

from pandas import read_csv, read_json, read_pickle, to_timedelta, Grouper

@dataclass(frozen=True)
class RawData:
    input      : Path
    output     : Path
    date       : datetime
    details    : str
    processors : (Processor := namedtuple('Processor', 'reader writer'))

    STEM_RE = re_compile(r'^(?P<type>results)\.(?P<date>\d{4}-\d{2}-\d{2})\.(?P<details>.+)')
    PROCESSORS = {
        '.json':   Processor(read_json,   lambda x: x.to_json),
        '.csv':    Processor(read_csv,    lambda x: x.to_csv),
        '.pickle': Processor(read_pickle, lambda x: x.to_pickle),
    }

    @classmethod
    def from_path(cls, path):
        if not (mo := cls.STEM_RE.fullmatch(path.stem)) or path.suffix not in cls.PROCESSORS:
            raise ValueError('invalid input file path')
        date, details = mo.group('date'), mo.group('details')
        date = datetime.strptime(date, '%Y-%m-%d')
        processors = cls.PROCESSORS[path.suffix]
        return cls(path, path.with_stem(f'processed.{date:%Y-%m-%d}.{details}'), date, details, processors)

if __name__ == '__main__':
    all_files = {
        RawData.from_path(p)
        for p in Path('/tmp/data').iterdir()
        if RawData.STEM_RE.fullmatch(p.stem) and p.suffix in {'.csv', '.json'}
    }

    skipped = {Path('results.2022-09-28.test-run.csv')}
    corrupt = {Path('results.2022-09-27.bad-run.csv')}

    to_process = {rd for rd in all_files if rd.input not in skipped | corrupt}
    for ent in to_process:
        data = (
            ent.processors.reader(ent.input)
            .assign(timestamp=lambda df: to_timedelta(df['time']) + ent.date)
            .drop('time', axis='columns')
            .set_index(['entity', 'timestamp'])
            .groupby(['entity', Grouper(level='timestamp', freq='H')]).max()
            .groupby('entity').transform(
                lambda g: g.rolling(3, min_periods=1, win_type='triang').mean()
            )
            .pipe(ent.processors.writer)(ent.output)
        )
