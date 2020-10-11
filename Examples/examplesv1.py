from amortizationcalculator import AmortCalc

import matplotlib.pyplot as plt

import pandas as pd
pd.options.display.max_columns = 15

#%%

amort = AmortCalc(interestrate_yearly=0.03375, periods=12*30, balance_initial=200000, payment_period=884.19)
amort.continuecurrentpaymentstrategyuntilpaidoff()
fig, ax = amort.plot(color='k')
df_30 = amort.df_data

#%%

amort = AmortCalc(0.03125, 12*15, 200000, 1393.22)
amort.continuecurrentpaymentstrategyuntilpaidoff()
fig, ax = amort.plot(figandax=(fig, ax), color='b')
df_15 = amort.df_data

#%%

# because of the way amortization calculations work, if you had the same monthly payment, a onetime payment on
# the first day of the loan would be the same as taking out a smaller loan by that amount.
# therefore
#
# amort = AmortCalc(0.03125, 12*15, 200000, 1393.22)
# amort.adhocpayment(50000)
#
# is the same as
#
# amort = AmortCalc(0.03125, 12*15, 150000, 1393.22)
# amort.adhocpayment(0)

amort = AmortCalc(0.03125, 12*15, 200000, 1393.22)
amort.adhocpayment(50000)
amort.continuecurrentpaymentstrategyuntilpaidoff()
amort.plot(figandax=(fig, ax), color='r')

#%% a more custom payment strategy: a 10k payment after 3 months then normal payment to finish off.

amort = AmortCalc(0.03125, 12*15, 200000, 1393.22)
for index in range(3):
    amort.updatedataoneround()
amort.adhocpayment(10000)
amort.continuecurrentpaymentstrategyuntilpaidoff()
amort.plot()

#%% a more custom payment strategy: a 1k additional payment every year.

periods = 12*15
amort = AmortCalc(0.03125, periods, 200000, 1393.22)
for period in range(periods):
    for index in range(12):
        if amort.current_balance < 0:
            break
        amort.updatedataoneround()
    amort.adhocpayment(1000)
amort.plot()

#%%
# using recurring overpayment

amort = AmortCalc(interestrate_yearly=0.03375, periods=12*30, balance_initial=200000, payment_period=884.19,
                  recurringoverpayment=275)
amort.continuecurrentpaymentstrategyuntilpaidoff()
amort.plot(color='k')
df_30_overpayment = amort.df_data

#%%

fig, ax = plt.subplots()
df_30_overpayment['interest_cumulative'].plot(label='30_overpayment')
df_15['interest_cumulative'].plot(label='15')
df_30['interest_cumulative'].plot(label='30')
ax.grid()
ax.legend()
ax.set_ylabel('interest_cumulative')
fig.tight_layout()
fig.show()


