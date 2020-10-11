import pandas as pd
import datetime
import matplotlib.pyplot as plt


class AmortCalc:

    def __init__(self, interestrate_yearly: float, periods: int, balance_initial: float,
                 payment_period: float,
                 periodsperyyear: float = 12,
                 date_initial: str = None,
                 recurringoverpayment: float = False
                 ):

        self.interestrate_yearly = interestrate_yearly
        self.periods = periods
        self.current_period = 0
        self.balance_initial = balance_initial
        self.periodsperyyear = periodsperyyear
        self.payment_period = payment_period
        self.recurringoverpayment = recurringoverpayment

        self.interestrate_period = self.interestrate_yearly / self.periodsperyyear

        if date_initial is None:
            self.datetime_initial = datetime.datetime.now()
        self.date_initial = self.datetime_initial.date().strftime('%Y-%m-%d')

        self.interest_cummulative = 0
        self.prinicple_cummulative = 0
        self.current_balance = balance_initial
        self.datetime_current = self.datetime_initial

        self.list_columns = ['period', 'current_balance', 'date_current',
                             'interest_cumulative', 'principle_cumulative',
                             'interest_period', 'principle_period']
        self.df_data = pd.DataFrame(columns=self.list_columns)

    @property
    def getinterestfornextperiod(self) -> float:
        return self.current_balance * self.interestrate_period

    @property
    def getprinciplefornextperiod(self) -> float:
        return self.payment_period - self.getinterestfornextperiod

    @property
    def date_current(self) -> str:
        return self.datetime_current.strftime(format='%Y-%m-%d')

    def adhocpayment(self, amount: float):
        self.current_balance -= amount

    def updatedataoneround(self):
        self.current_period += 1

        interest_period = self.getinterestfornextperiod
        self.interest_cummulative += interest_period

        principle_period = self.getprinciplefornextperiod
        self.prinicple_cummulative += principle_period

        self.current_balance -= principle_period

        if self.recurringoverpayment is not False:
            self.adhocpayment(self.recurringoverpayment)

        # calculate the datetime of the next period, handle december (month=12) separately.
        if self.datetime_current.month != 12:
            self.datetime_current = datetime.datetime(self.datetime_current.year,
                                                      self.datetime_current.month + 1,
                                                      1)
        else:
            self.datetime_current = datetime.datetime(self.datetime_current.year + 1,
                                                      1,
                                                      1)

        list_temp = [self.current_period, self.current_balance, self.date_current,
                     self.interest_cummulative, self.prinicple_cummulative,
                     interest_period, principle_period]

        df_temp = pd.DataFrame(list_temp, index=self.list_columns).T
        df_temp = df_temp.set_index('period')
        if len(self.df_data) == 0:
            self.df_data = df_temp.copy()
        else:
            self.df_data = pd.concat([self.df_data, df_temp], axis=0)

    def updatedatanrounds(self, n: int):
        for index in range(n):
            self.updatedataoneround()

    def continuecurrentpaymentstrategyuntilpaidoff(self):
        for index in range(1000):
            self.updatedataoneround()
            if self.current_balance <= 0:
                break

    def plot(self, figandax=None, color: str = None):

        if figandax is None:
            fig, axes = plt.subplots(1, 2, figsize=(10, 10))
        else:
            fig, axes = figandax

        ax = axes[0]
        if color is None:
            self.df_data['current_balance'].plot(ax=ax, style='-')
            self.df_data['interest_cumulative'].plot(ax=ax, style=':')
            self.df_data['principle_cumulative'].plot(ax=ax, style='-.')
        else:
            self.df_data['current_balance'].plot(ax=ax, style='-', color=color)
            self.df_data['interest_cumulative'].plot(ax=ax, style=':', color=color)
            self.df_data['principle_cumulative'].plot(ax=ax, style='-.', color=color)
        ax.grid()
        ax.legend()
        ax.set_ylabel('Dollars')

        ax = axes[1]
        if color is None:
            self.df_data['interest_period'].plot(ax=ax, style='-')
            self.df_data['principle_period'].plot(ax=ax, style=':')
        else:
            self.df_data['interest_period'].plot(ax=ax, style='-', color=color)
            self.df_data['principle_period'].plot(ax=ax, style=':', color=color)
        ax.grid()
        ax.legend()

        return fig, axes
