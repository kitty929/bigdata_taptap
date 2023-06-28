# from flask import Flask, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS

from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# 连接 MySQL 数据库
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="20020929",
  database="taptap_analysis"
)

# 创建数据库表
cursor = db.cursor()

@app.before_request
def before_request():
    # 在此处连接到 MySQL 数据库
    global cnx, cursor
    cnx = mysql.connector.connect(user='root', password='20020929',
                                  host='localhost',
                                  database='taptap_analysis')
    cursor = cnx.cursor()

@app.after_request
def after_request(response):
    # 在此处关闭游标对象和数据库连接
    cursor.close()
    cnx.close()
    return response

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/1')
def chart1():
    # 获取数据库数据并渲染成 HTML 页面返回给用户
    return render_template('1.html')
@app.route('/2')
def chart2():
    # 获取数据库数据并渲染成 HTML 页面返回给用户
    return render_template('2.html')
@app.route('/3')
def chart3():
    # 获取数据库数据并渲染成 HTML 页面返回给用户
    return render_template('3.html')
@app.route('/4')
def chart4():
    # 获取数据库数据并渲染成 HTML 页面返回给用户
    return render_template('4.html')
@app.route('/5')
def chart5():
    # 获取数据库数据并渲染成 HTML 页面返回给用户
    return render_template('5.html')
@app.route('/6')
def chart6():
    # 获取数据库数据并渲染成 HTML 页面返回给用户
    return render_template('6.html')
@app.route('/7')
def chart7():
    # 获取数据库数据并渲染成 HTML 页面返回给用户
    return render_template('7.html')

@app.route('/data')
def data():

    # 从数据库获取数据
    cursor.execute("SELECT app_title,fans_count FROM fans_app_top order by fans_rk")
    data = cursor.fetchall()
    # 格式化数据
    labels = []
    values = []
    for row in data:
        labels.append(row[0])
        values.append(int(row[1]))
    # 返回 JSON 格式数据
    return jsonify({'labels': labels, 'values': values})

# 各游戏类型的游戏数
@app.route('/data2')
def data2():
    # 从数据库获取数据
    cursor.execute("SELECT tag_name,tag_number FROM number_tags where tag_number > 50")
    data2 = cursor.fetchall()
    # 格式化数据
    labels2 = []
    values2 = []
    for row in data2:
        labels2.append(row[0])
        values2.append({"name": row[0], "value": int(row[1])})

        cursor.execute('''
                       SELECT level, num
                       FROM
                           (SELECT *,
                               (CASE 
                                   WHEN tag_number <= 10 THEN '0-10'
                                   WHEN tag_number <= 50 THEN '10-50'
                                   WHEN tag_number <= 100 THEN '0-100'
                                   WHEN tag_number <= 200 THEN '100-200'
                                   WHEN tag_number <= 300 THEN '200-300'
                                   WHEN tag_number <= 400 THEN '300-400'
                                   WHEN tag_number <= 500 THEN '400-500'
                                   ELSE '>500'
                               END) AS level, count(*) AS num
                           FROM number_tags
                           GROUP BY level) AS t;
           ''')
        data2_2 = cursor.fetchall()
        # 格式化数据
        labels2_2 = []
        values2_2 = []
        for row in data2_2:
            labels2_2.append(row[0])
            values2_2.append({"name": row[0], "value": int(row[1])})

    # 返回 JSON 格式数据
    return jsonify({'labels': labels2, 'values': values2, 'labels2': labels2_2, 'values2': values2_2})
#
# @app.route('/data2_2')
# def data2_2():
#     # 从数据库获取数据
#     cursor.execute('''
#                 SELECT level, num
#                 FROM
#                     (SELECT *,
#                         (CASE
#                             WHEN tag_number <= 10 THEN '0-10'
#                             WHEN tag_number <= 50 THEN '10-50'
#                             WHEN tag_number <= 100 THEN '0-100'
#                             WHEN tag_number <= 200 THEN '100-200'
#                             WHEN tag_number <= 300 THEN '200-300'
#                             WHEN tag_number <= 400 THEN '300-400'
#                             WHEN tag_number <= 500 THEN '400-500'
#                             ELSE '>500'
#                         END) AS level, count(*) AS num
#                     FROM number_tags
#                     GROUP BY level) AS t;
#     ''')
#     data2_2 = cursor.fetchall()
#     # 格式化数据
#     labels2 = []
#     values2 = []
#     for row in data2_2:
#         labels2.append(row[0])
#         values2.append({"name": row[0], "value": int(row[1])})
#     # 返回 JSON 格式数据
#     return jsonify({'labels': labels2, 'values': values2})


# 各游戏类型的游戏数
@app.route('/data1')
def data1():
    # 从数据库获取数据
    cursor.execute("SELECT tag_name,popular_score_total * 100 as total FROM popular_tags order by popular_score_total desc limit 30")
    data1 = cursor.fetchall()
    # 格式化数据
    labels2 = []
    values2 = []
    for row in data1:
        labels2.append(row[0])
        values2.append({"name": row[0], "value": int(row[1])})
        # 关闭游标对象
    cursor.close()
    # 返回 JSON 格式数据
    return jsonify({'labels': labels2, 'values': values2})

@app.route('/data1_2')
def data1_2():
    # 从数据库获取数据
    cursor.execute("SELECT tag_name,popular_score_total FROM popular_tags order by popular_score_total desc")
    data1_2 = cursor.fetchall()
    # 格式化数据
    labels2 = []
    values2 = []
    for row in data1_2:
        labels2.append(row[0])
        values2.append(float(row[1]))
        # 关闭游标对象
    cursor.close()
    # 返回 JSON 格式数据
    return jsonify({'labels': labels2, 'values': values2})

# 各游戏类型的游戏数
@app.route('/data3')
def data3():
    # 从数据库获取数据
    cursor.execute('''select tag_name, tag_percent*100
        from popular_tags_percent
        where tag_percent >= 0.01''')
    data3 = cursor.fetchall()
    # 格式化数据
    labels3 = []
    values3 = []
    for row in data3:
        labels3.append(row[0])
        values3.append({"name": row[0], "value": int(row[1])})
    # 返回 JSON 格式数据
    return jsonify({'labels': labels3, 'values': values3})


# 游戏下载排行榜
@app.route('/data4')
def data4():
    # 从数据库获取数据
    cursor.execute("SELECT app_title,hits_total FROM hits_app_top order by hits_rk limit 20")
    data4 = cursor.fetchall()
    # 格式化数据
    labels = []
    values = []
    for row in data4:
        labels.append(row[0])
        values.append(int(row[1]))
    # 返回 JSON 格式数据
    return jsonify({'labels': labels, 'values': values})

@app.route('/data4_2')
def data4_2():
    # 从数据库获取数据
    cursor.execute("SELECT app_title,hits_total FROM hits_app_top order by hits_rk")
    data4 = cursor.fetchall()
    # 格式化数据
    labels = []
    values = []
    for row in data4:
        labels.append(row[0])
        values.append(int(row[1]))
    # 返回 JSON 格式数据
    return jsonify({'labels': labels, 'values': values})


# 游戏关注排行榜
@app.route('/data5')
def data5():
    # 从数据库获取数据
    cursor.execute("SELECT app_title,fans_count FROM fans_app_top order by fans_rk limit 20")
    data = cursor.fetchall()
    # 格式化数据
    labels = []
    values = []
    for row in data:
        labels.append(row[0])
        values.append(int(row[1]))
    # 返回 JSON 格式数据
    return jsonify({'labels': labels, 'values': values})


# 游戏关注排行榜
@app.route('/data5_2')
def data5_2():
    # 从数据库获取数据
    cursor.execute("SELECT app_title,fans_count FROM fans_app_top order by fans_rk")
    data = cursor.fetchall()
    # 格式化数据
    labels = []
    values = []
    for row in data:
        labels.append(row[0])
        values.append(int(row[1]))
    # 返回 JSON 格式数据
    return jsonify({'labels': labels, 'values': values})




# 游戏关注排行榜
@app.route('/data6_1')
def data6_1():
    # 从数据库获取数据
    cursor.execute('''SELECT app_title,star_score FROM stars_app_top order by star_rk''')
    data6_1 = cursor.fetchall()
    # 格式化数据
    labels = []
    values = []
    for row in data6_1:
        labels.append(row[0])
        values.append(float(row[1]))
    # 返回 JSON 格式数据
    return jsonify({'labels': labels, 'values': values})

@app.route('/data7')
def data7():
    # 从数据库获取数据
    cursor.execute("SELECT tag_name,tag_id FROM stars_tags order by star_score_average limit 50")
    data7 = cursor.fetchall()
    # 格式化数据
    labels = []
    values = []
    for row in data7:
        labels.append(row[0])
        values.append(int(row[1]))
    # 返回 JSON 格式数据
    return jsonify({'labels': labels, 'values': values})



if __name__ == '__main__':
    app.run(debug=True)