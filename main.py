
from src.start_analysis import get_messages
from src.generate_plots import plot_messages_per_chat, plot_activity_over_time, plot_activity_over_day


def main():
    print('Welcome to my program.')
    print('Processing your data...')
    data_frame = get_messages()
    print('Generating plots...')
    plot_messages_per_chat(data_frame, 10)
    plot_activity_over_time(data_frame, 6)
    plot_activity_over_day(data_frame)


if __name__=="__main__":
    main()