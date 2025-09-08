import joblib
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import shap
from matplotlib import pyplot as plt
import os

app = Flask(__name__,static_url_path='/static')
CORS(app, resources={r"/api/*": {"origins": "http://47.101.189.188:8000"}})  # 允许跨域请求

# 加载训练好的模型
model = joblib.load(open("Machine_best_model_18.pkl", "rb"))

# 假设类标签列表
treatmusic = ["Gong", "Shang", "Jue", "Zhi", "Yu"]
classes = ["WSS", "LFBU", "PFSI", "WFAI", "KED"]

treatmusic_zh = ["宫乐", "商乐", "角乐", "徵乐", "羽乐"]
classes_zh = ["脾胃虚弱", "肝火上扰", "痰火郁结", "风热侵袭", "肾精亏损"]

@app.route("/")  # 根路由
def home():
    return "Flask server is running."

# @app.route("/predict", methods=["POST"])  # 处理预测请求
@app.route("/api/predict", methods=["GET"])  # 处理预测请求
def predict():
    try:
        # 获取用户输入的特征，并将其转换为整数
        # data = request.json #request.json是一个字典对象
        # int_features = data['features']
        # front_language = data['language']
        # print(front_language)
        # final_features = np.array(int_features).reshape(1, -1)  # 将特征数据转化为二维数组供模型输入

        # 从查询参数中获取 features 和 language
        features = request.args.get('features')
        front_language = request.args.get('language')
    
        print(f'get{features}')

        if features is None or front_language is None:
            return jsonify({"error": "Missing 'features' or 'language' parameter"}), 400

        # 尝试将 features 从字符串转换为 JSON 对象
        int_features = json.loads(features)  # 确保 features 是一个有效的 JSON 字符串

        final_features = np.array(int_features).reshape(1, -1)  # 将特征数据转化为二维数组供模型输入

        # 如果模型期望有18个特征，且我们收到的输入特征少于18个，可以填充剩余的特征为0
        if final_features.shape[1] < 18:
            final_features = np.pad(final_features, ((0, 0), (0, 18 - final_features.shape[1])), 'constant')

        print(final_features)
        # 使用模型进行预测
        prediction = model.predict(final_features)
        prediction_proba = model.predict_proba(final_features)

        # 获取预测结果的类别
        output = prediction[0]
        print(output)
    
        if front_language == 'English':
            feature_names_en = [
                'Low pitched tinnitus occurred within one month',
                'History of cold or chronic rhinitis',
                'Tinnitus sounds like roaring wind or tide',
                'Restless insomnia with early morning awakening',
                'Irritability insomnia and vivid dreams',
                'Lower back pain and nocturnal emission',
                'Impulsive and irritable personality',
                'Heaviness in the head bitter or bland taste in the mouth',
                'Sensation of emptiness in the ear',
                'Ear fullness and blockage causing breathlessness',
                'Worsens when standing up',
                'Worsens after exertion',
                'Greasy tongue coating',
                'Yellow tongue coating',
                'Floating pulse',
                'Wiry pulse',
                'Slippery pulse',
                'Thin pulse']

            #shap预测
            explainer = shap.TreeExplainer(model,feature_names=feature_names_en)
            shap_values = explainer(final_features)

            print(shap_values.shape)
            print(shap_values)

            # 生成SHAP Waterfall图
            shap_fig = shap.plots.waterfall(shap_values[0,:,output],show = False)
            fig = plt.gcf()
            ax = plt.gca()

            fig.set_size_inches(10,7)
            plt.title(f'Waterfall plot for {classes[output]}',fontsize = 14)
            plt.tight_layout()
            plt.savefig(f'static/waterfall_plot_en.png',dpi = 300)
            plt.close()
        else:
            # 保存当前的 rcParams 设置
            original_rcParams = plt.rcParams.copy()
            # 临时设置中文字体
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
            plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

            feature_names_zh = [
                '耳鸣声低沉，耳鸣发作一月内',
                '有感冒史，或素有鼻炎',
                '耳鸣轰轰如风声、潮声',
                '虚烦失眠，晨起早醒',
                '烦躁失眠，多梦',
                '腰酸，遗精',
                '性格急躁、易怒',
                '头昏沉重，口苦或口淡',
                '耳内空虚感',
                '耳胀，耳闭塞憋气',
                '站起时加重',
                '劳作后加重',
                '腻（苔）',
                '黄（苔）',
                '浮（脉）',
                '弦（脉）',
                '滑（脉）',
                '细（脉）']
            #shap预测
            explainer = shap.TreeExplainer(model,feature_names=feature_names_zh)
            shap_values = explainer(final_features)

            print(shap_values.shape)
            print(shap_values)

            # 生成SHAP Waterfall图
            shap_fig = shap.plots.waterfall(shap_values[0,:,output],show = False)
            fig = plt.gcf()
            ax = plt.gca()

            fig.set_size_inches(10,7)
            plt.title(f'{classes_zh[output]}的SHAP瀑布图',fontsize = 14)
            plt.tight_layout()
            plt.savefig(f'static/waterfall_plot_zh.png',dpi = 300)
            plt.close()
            # 恢复原来的 rcParams 设置
            plt.rcParams.update(original_rcParams)

        probabilities = [{"class": cls, "probability": prob} for cls, prob in zip(classes, prediction_proba[0])]
        probabilities_zh = [{"class": cls, "probability": prob} for cls, prob in zip(classes_zh, prediction_proba[0])]

        audio_url = f"http://47.101.189.188:5000/static/music/{output}.mp3"
        img_url_en = f"http://47.101.189.188:5000/static/waterfall_plot_en.png"
        img_url_zh = f"http://47.101.189.188:5000/static/waterfall_plot_zh.png"

        print(classes_zh[output])
        print(treatmusic_zh[output])
        response = {
            "prediction": classes[output] if front_language == 'English' else classes_zh[output],
            "treatment":treatmusic[output] if front_language == 'English' else treatmusic_zh[output],
            "probabilities":probabilities if front_language == 'English' else probabilities_zh,
            "audio_url":audio_url,
            "img_url":img_url_en if front_language == 'English' else img_url_zh,
        }

        return jsonify(response)

    except Exception as e:
        # 捕获异常并返回错误信息
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
