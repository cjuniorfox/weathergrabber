from weathergrabber.use_case.statistics_uc import StatisticsUC

class StatisticsTTY:
    def __init__(self, statistics_uc: StatisticsUC):
        self.statistics_uc = statistics_uc

    def execute(self):
        data = self.statistics_uc.execute()
        # Implement statistics display logic here
        print("Displaying weather statistics...")
        for key, value in data.items():
            print(f"{key}: {value}")