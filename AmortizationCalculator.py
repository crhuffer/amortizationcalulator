# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 14:18:53 2020

@author: crhuf
"""

import pandas as pd
import datetime

import matplotlib.pyplot as plt

#%%

class AmortCalc():

    def __init__(self, interestrate_year, periods, balance_initial,
                 payment_period,
                 periodsperyyear=12,
                 date_initial=None,
                 recurringoverpayment=False
                 ):
        self.interestrate_year = interestrate_year
        self.periods = periods
        self.current_period = 0
        self.balance_initial = balance_initial
        self.periodsperyyear = periodsperyyear
        self.payment_period = payment_period
        self.recurringoverpayment = recurringoverpayment

        self.interestrate_period = self.interestrate_year/self.periodsperyyear

        if date_initial is None:
            self.datetime_initial = datetime.datetime.now()

        self.date_initial = self.datetime_initial.date().strftime('%Y-%m-%d')
#        self.datetime_initial = datetime.datetime.now().strptime(self.date_initial, format='%Y-%m-%d')
        self.interest_cummulative = 0
        self.prinicple_cummulative = 0
        self.current_balance = balance_initial
        self.datetime_current = self.datetime_initial

        self.list_columns = ['period', 'current_balance', 'date_current',
                        'interest_cumulative', 'principle_cumulative',
                        'interest_period', 'principle_period']
        self.df_data = pd.DataFrame(columns=self.list_columns)

    @property
    def getinterestfornextperiod(self):
        return self.current_balance*self.interestrate_period

    @property
    def getprinciplefornextperiod(self):
        return self.payment_period - self.getinterestfornextperiod

    @property
    def date_current(self):
        return datetime.datetime.strftime(self.datetime_current, format='%Y-%m-%d')

    def adhocpayment(self, amount):
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

        if self.datetime_current.month != 12:
            self.datetime_current = datetime.datetime(self.datetime_current.year,
                                                   self.datetime_current.month+1,
                                                   1)
        else:
            self.datetime_current = datetime.datetime(self.datetime_current.year+1,
                                                   1,
                                                   1)

        list_temp = [self.current_period, self.current_balance, self.date_current,
                     self.interest_cummulative, self.prinicple_cummulative,
                     interest_period, principle_period]

        #print(list_temp)
        #self.df_data = self.df_data.append(list_temp)
        df_temp = pd.DataFrame(list_temp, index=self.list_columns).T
        df_temp = df_temp.set_index('period')
        if len(self.df_data) == 0:
            self.df_data = df_temp.copy()
        else:
            self.df_data = pd.concat([self.df_data, df_temp], axis=0)

    def updatedatanrounds(self, n):
        for index in range(n):
            self.updatedataoneround()

    def updateuntilpaidoff(self):
        for index in range(1000):
            self.updatedataoneround()
            if self.current_balance <= 0:
                break

    def plot(self):
        fig, axes = plt.subplots(1, 2, figsize=(10,10))

        ax=axes[0]
        self.df_data.loc[:, ['current_balance', 'interest_cumulative',
                              'principle_cumulative']].plot(ax=ax)
        ax.grid()

        ax=axes[1]
        self.df_data.loc[:, ['interest_period', 'principle_period']].plot(ax=ax)
        ax.grid()

#%%

amort = AmortCalc(0.02275, 12*8, 103350, 1300)
amort.updateuntilpaidoff()
amort.plot()

#%%

amort = AmortCalc(0.02275, 12*8, 103350, 1300)
amort.adhocpayment(50000)
amort.updateuntilpaidoff()
amort.plot()

#%%

amort = AmortCalc(0.0375, 12*8, 133000, 1100)
amort.updateuntilpaidoff()
amort.plot()

#%%

amort = AmortCalc(0.0375, 12*8, 133000, 1100,
                  recurringoverpayment=275)
amort.updateuntilpaidoff()
amort.plot()

#%%

amort = AmortCalc(0.0375, 12*8, 133000, 1100)
amort.adhocpayment(50000)
amort.updateuntilpaidoff()
amort.plot()

#%%
amort = AmortCalc(0.02275, 12*8, 103350, 1300)

##%%
#
#amort.updatedataoneround()
#
##%%
#
#amort.updatedatanrounds(15)

#%%

amort.updateuntilpaidoff()


#%%

list_columnstoplot = ['current_balance', 'interest_cumulative',
                      'principle_cumulative',
                      'interest_period', 'principle_period']

#%%

fig, axes = plt.subplots(1, 2, figsize=(10,10))

ax=axes[0]
amort.df_data.loc[:, ['current_balance', 'interest_cumulative',
                      'principle_cumulative']].plot(ax=ax)
ax.grid()

ax=axes[1]
amort.df_data.loc[:, ['interest_period', 'principle_period']].plot(ax=ax)
ax.grid()

#%%

amort.getprinciplefornextperiod

#%%

amort.getinterestfornextperiod
