def visualisation_heatmap():
    import numpy as np
    from influxdb import InfluxDBClient
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    width = 800
    height = 600

    dbname = 'arkanoid'
    dbuser = 'arkanoid_publisher'
    dbuser_password = '1'
    query = 'select object, x_coord, y_coord from coordinates;'
    client = InfluxDBClient(host='172.17.0.2', port=8086, database=dbname)
    client.switch_user(dbuser, dbuser_password)

    df = pd.DataFrame(client.query(query).get_points())
    print(df.head())
    ball_heatmap_data = np.zeros((int(height/20), int(width/20)))
    paddle_heatmap_data = np.zeros((int(height/20), int(width/20)))
    x_coords = df['x_coord'].tolist()
    y_coords = df['y_coord'].tolist()
    obj = df['object'].tolist()
    for k in range(len(obj)):
        if obj[k] == 'paddle':
            j = round(y_coords[k]/20) -1
            for count in range(5):
                i = round(x_coords[k]/20) + count -1
                paddle_heatmap_data[-j][i] += 1
        else:
            j = round(y_coords[k] / 20) -1
            i = round(x_coords[k] / 20) -1
            ball_heatmap_data[j][i] += 1

    xtick_label1 = np.arange(0, int(width/20), 2)
    xtick_label2 = np.arange(0, width, 40)
    ytick_label1 = np.arange(0, int(height/20), 2)
    ytick_label2 = np.arange(height, 0, -40)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax = sns.heatmap(ball_heatmap_data, ax=ax)
    plt.xticks(xtick_label1, xtick_label2)
    plt.yticks(ytick_label1, ytick_label2)
    plt.show()

    fig, ax = plt.subplots(figsize=(10, 10))
    ax = sns.heatmap(paddle_heatmap_data, ax=ax)
    plt.xticks(xtick_label1, xtick_label2)
    plt.yticks(ytick_label1, ytick_label2)
    plt.show()
    return