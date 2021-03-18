from . import date_range
from datetime import datetime
import glob
import pandas as pd

def get_csv_path(root, start, end):
    """
    ある期間内のcsvパスを取得
    """
    start_time = datetime.strptime(start, '%Y_%m_%d')
    end_time = datetime.strptime(end, '%Y_%m_%d')
    csv_path_list = []
    for date in date_range(start_time, end_time):
        path = root + '/{year}/{month:02}/{date}/*.csv'.format(
            year = date.year,
            month = date.month,
            date = date.strftime('%Y_%m_%d')
        )
        csv_path_list += glob.glob(path)
    return csv_path_list

def get_board_from_csv(root, start, end):
    """
    ある期間内の板情報のcsvを取得
    """
    csv_path_list = get_csv_path(root, start, end)
    df_list = []
    for path in csv_path_list:
        df_list.append(pd.read_csv(path, index_col = 0))

    df = pd.concat(df_list)
    df.reset_index(drop = True, inplace = True)
    return df
