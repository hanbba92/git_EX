from datetime import datetime


def result_logger(common, dates, conditions, results, points):
    date_log_str = 'dates='
    for index, date in enumerate(dates):
        s_date = str(date)
        o_date = datetime.strptime(s_date, '%Y%m%d%H').strftime('%Y-%m-%d %H:%M:%S')
        if index == 0:
            date_log_str = f'{date_log_str}{o_date}'
        else:
            date_log_str = f'{date_log_str}/{o_date}'
    common.logger.info(date_log_str)
    for i in range(points.shape[0]):
        for index, date in enumerate(dates):
            s_date = str(date)
            o_date = datetime.strptime(s_date, '%Y%m%d%H').strftime('%Y-%m-%d %H:%M:%S')
            common.logger.info(f'{points[i]}/{conditions[index][i]}/{results[index][i]}/{o_date}')

