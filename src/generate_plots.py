import pandas as pd
import seaborn as sns
import datetime
import os
import time

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from .parameters import getParam

user = getParam('user')
sns.set()


def plot_messages_per_chat(data, chats: int):
    noGroup = data
    plotDataSeries = noGroup["chat_with"].value_counts()[:chats]

    plotData = pd.DataFrame(plotDataSeries)
    plotData["person"] = plotData.index
    plotData["messages_number"] = plotData["chat_with"]
    ax = sns.barplot(x=plotData["messages_number"],
                     y=plotData["person"], orient="h")
    ax.grid(True)
    ax.set_title("Chats with the most messages")
    ax.set_ylabel('Participant')
    ax.set_xlabel('Total messages count')

    path = "plot1.png"
    ax.figure.savefig(path, bbox_inches='tight')


def plot_activity_over_time(data, order=6):
    chat = data
    chat['sent_by_user'] = chat['sender_name'].apply(lambda x: True if x == user else False)
    by_dates = chat.groupby(['date', 'sent_by_user'], as_index=True).agg('count')
    plotting = by_dates.reset_index()
    plotting["messages_per_day"] = plotting["sender_name"]

    plotting["datetime"] = plotting["date"].astype(str).apply(
        lambda dstr: time.mktime(time.strptime(dstr, r"%Y-%m-%d")))

    plotting["date_float"] = plotting["datetime"].values.astype(float)

    plotting["Message direction"] = plotting["sent_by_user"].apply(
        lambda x: "Sent" if x else "Received")

    g = sns.lmplot(data=plotting, x="date_float", y="messages_per_day",
                   hue="Message direction", scatter=False, order=order, legend_out=False, aspect=1.7, palette="Set1")

    g.set(xlim=(plotting["date_float"].min(), plotting["date_float"].max()))
    g.set(ylim=(0, None))

    plt.subplots_adjust(top=0.9)
    g.fig.suptitle("Average messages number over time")

    g.axes[0, 0].yaxis.set_major_locator(plt.MaxNLocator(10))
    g.axes[0, 0].xaxis.set_major_locator(plt.MaxNLocator(10))

    g.axes[0, 0].set_xlabel('Time')
    g.axes[0, 0].set_ylabel('Messages per day')

    xticks = g.axes[0, 0].get_xticks()
    xticks_dates = [datetime.datetime.fromtimestamp(x).strftime('%m-%Y') for x in xticks]

    g.axes[0, 0].set_xticklabels(
        xticks_dates, rotation=45, horizontalalignment='right')

    path = "plot2.png"
    g.savefig(path, bbox_inches='tight')


def plot_activity_over_day(data):
    chat = data
    data["sent_by_user"] = data["sender_name"] == user

    plotting = data.groupby(
        ["hour", "sent_by_user"]).agg("count").reset_index()

    number_of_hours = len(pd.period_range(min(data["date"]), max(data["date"])))

    plotting["avg_messages_per_hour"] = plotting["sender_name"]/number_of_hours

    plotting["message_direction"] = plotting["sent_by_user"].apply(
        lambda x: 'Sent' if x else 'Received')

    plotting["hour_num"] = plotting["hour"].astype(int)

    g = sns.lmplot(data=plotting, x="hour_num", y="avg_messages_per_hour",
                   hue="message_direction", scatter=False, order=4, legend_out=False, aspect=1.7, palette="Set1")

    g.axes[0, 0].xaxis.set_major_locator(
        MultipleLocator(2))
    g.set(xlim=(0, 23))
    g.set(ylim=(0, None))

    g.ax.legend(loc=2)

    plt.subplots_adjust(top=0.9)
    g.fig.suptitle("Average messages number over day")
    g.axes[0, 0].set_xlabel('Hour')
    g.axes[0, 0].set_ylabel('Number of messages')

    path = "plot3.png"
    g.savefig(path, bbox_inches='tight')

