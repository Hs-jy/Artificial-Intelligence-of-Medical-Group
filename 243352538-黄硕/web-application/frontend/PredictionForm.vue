<template>
  <div id="vanta-background" class="vanta-container">
  <div class="container">

    <!-- 标题 -->
     <div class="title-style">
      <h1 v-if="language === 'English'" class="title">Subjective Tinnitus Online Diagnosis and Treatment System</h1>
      <h1 v-if="language === '中文'" class="title">原发性耳鸣在线诊疗系统</h1>
      <div class="config-box">
        <button @click="changeLanguage" class="config-change-language">{{ oppositeLanguage }}</button>
      </div>
     </div>

    <div class="content">
      <!-- 左侧：症状选择框 -->
      <div class="symptom-box">
        <h2 v-if="language === 'English'" class="subtitle">Please Select Symptoms:</h2>
        <h2 v-if="language === '中文'" class="subtitle">请选择您的症状:</h2>

        <div class="symptoms">
          <div
            v-for="feature in currentFeatures"
            :key="feature.id"
            class="symptom-item"
            :class="{ selected: feature.value === '1' }"
            @click="toggleFeature(feature)"
          >
            {{ feature.label }}
          </div>
        </div>
      </div>

      <!-- 右侧：诊断结果与音乐播放器 -->
      <div class="result-box">
        
        <p v-if="predictionText" class="prediction-text" v-html="predictionText"></p>

        <!-- <img :src="imgUrl" alt="" v-if="imgUrl"> -->

        <!-- <p v-if="audioUrl && language === 'English'" class="audio-label">Treatment Audio:</p>
        <p v-if="audioUrl && language === '中文'" class="audio-label">治疗音乐:</p> -->

        <!-- 音频播放器组件 -->
        <AudioPlayer :audioURL="audioUrl" v-if="audioUrl" />

        <button v-if="language === 'English'" @click="submitForm" class="submit-btn">Diagnose</button>
        <button v-if="language === '中文'" @click="submitForm" class="submit-btn">诊断</button>

      </div>
    </div>
  </div>
</div>
</template>

<script>
import axios from "axios";
import 'kursor/dist/kursor.css';
import Kursor from 'kursor';
import AudioPlayer from './AudioPlayer.vue'//导入AudioPlayer.vue组件
// import * as THREE from "three";
// import NET from "vanta/dist/vanta.net.min";
import { defineComponent } from 'vue';


export default defineComponent({
  name: 'PredictionForm',
  data() {
    return {
      language:'English',
      features:this.getDaultFeatures(),
      features_zh:this.getFeaturesZh(),
      predictionText: "",
      audioUrl:"", //存储音频url
      vantaEffect:null, // 用于存储 Vanta.js 实例
      imgUrl:"",
    };
  },
  computed:{
    currentFeatures() {
      return this.language === 'English' ? this.features : this.features_zh;
    },
    oppositeLanguage(){
      return this.language === 'English' ? '中文版' : 'English Version';
    }
  },
  methods: {
    toggleFeature(feature) {
      feature.value = feature.value === "0" ? "1" : "0";
    },
    getDaultFeatures(){
      return [
        {id: 'feature1', label: 'Tinnitus like cicada calls worsens at night', value: '0'},
        {id: 'feature2', label: 'Low pitched tinnitus occurred within one month', value: '0'},
        {id: 'feature3', label: 'History of cold or chronic rhinitis', value: '0'},
        {id: 'feature4', label: 'Tinnitus sounds like roaring wind or tide', value: '0'},
        {id: 'feature5', label: 'Restless insomnia with early morning awakening', value: '0'},
        {id: 'feature6', label: 'Irritability insomnia and vivid dreams', value: '0'},
        {id: 'feature7', label: 'Lower back pain and nocturnal emission', value: '0'},
        {id: 'feature8', label: 'Impulsive and irritable personality', value: '0'},
        {id: 'feature9', label: 'Heaviness in the head bitter or bland taste in the mouth', value: '0'},
        {id: 'feature10', label: 'Sensation of emptiness in the ear', value: '0'},
        {id: 'feature11', label: 'Ear fullness and blockage causing breathlessness', value: '0'},
        {id: 'feature12', label: 'Worsens when standing up', value: '0'},
        {id: 'feature13', label: 'Worsens after exertion', value: '0'},
        {id: 'feature14', label: 'Thin tongue coating', value: '0'},
        {id: 'feature15', label: 'Greasy tongue coating', value: '0'},
        {id: 'feature16', label: 'Yellow tongue coating', value: '0'},
        {id: 'feature17', label: 'Floating pulse', value: '0'},
        {id: 'feature18', label: 'Wiry pulse', value: '0'},
        {id: 'feature19', label: 'Slippery pulse', value: '0'},
        {id: 'feature20', label: 'Thin pulse', value: '0'}
        ]
    },
    getFeaturesZh(){
      return [
        {id: 'feature1', label: '耳鸣如蝉鸣，夜间加重', value: '0'},
        {id: 'feature2', label: '耳鸣声低沉，耳鸣发作一月内', value: '0'},
        {id: 'feature3', label: '有感冒史，或素有鼻炎', value: '0'},
        {id: 'feature4', label: '耳鸣轰轰如风声、潮声', value: '0'},
        {id: 'feature5', label: '虚烦失眠，晨起早醒', value: '0'},
        {id: 'feature6', label: '烦躁失眠，多梦', value: '0'},
        {id: 'feature7', label: '腰酸，遗精', value: '0'},
        {id: 'feature8', label: '性格急躁、易怒', value: '0'},
        {id: 'feature9', label: '头昏沉重，口苦或口淡', value: '0'},
        {id: 'feature10', label: '耳内空虚感', value: '0'},
        {id: 'feature11', label: '耳胀，耳闭塞憋气', value: '0'},
        {id: 'feature12', label: '站起时加重', value: '0'},
        {id: 'feature13', label: '劳作后加重', value: '0'},
        {id: 'feature14', label: '薄（苔）', value: '0'},
        {id: 'feature15', label: '腻（苔）', value: '0'},
        {id: 'feature16', label: '黄（苔）', value: '0'},
        {id: 'feature17', label: '浮（脉）', value: '0'},
        {id: 'feature18', label: '弦（脉）', value: '0'},
        {id: 'feature19', label: '滑（脉）', value: '0'},
        {id: 'feature20', label: '细（脉）', value: '0'}
        ]
    },
    changeLanguage(){
      this.language = this.language == 'English' ? '中文' : 'English';
      //将输出结果和音频还回默认
      this.predictionText = '';
      this.audioUrl = '';
      this.imgUrl = '';
      //每次点击换语言就将特征还原回默认
      this.features = this.getDaultFeatures();
      this.features_zh = this.getFeaturesZh();
    },
    submitForm() {
      const features = this.language === 'English' ? this.features.map((f) => parseInt(f.value)) : this.features_zh.map((f) => parseInt(f.value));
      const language = this.language;
      this.predictionText = "Loading...";
      this.audioUrl = "";
      this.imgUrl = "";

      axios
        //.post("http://localhost:5000/predict", { features, language })
        // .post("http://121.4.79.250/api/predict", { features, language })
        // .get("http://localhost:5000/api/predict", { 
        .get("http://47.101.189.188:5000/api/predict", { 
          params:{
            features: JSON.stringify(features), 
            language: language,
            timestamp: Date.now() 
          },
          headers: {'Content-Type': 'application/json'}})
        .then((response) => {
          const data = response.data;
          if(language == 'English'){
            this.predictionText = `
            <h2 class="subtitle">Diagnosis Result</h2>
            <span class="large-text">Likely class: <span style="color: red;">${data.prediction}</span></span><br>
            <span class="medium-text">Probability for each class:</span><br>
            ${data.probabilities
              .sort((a, b) => b.probability - a.probability) // 按概率从高到低排序
              .map((p) => `<span class="medium-text">${p.class}: ${(p.probability*100).toFixed(0)}%</span>`)
              .join("<br>")}
            <br>
            <a href="${data.img_url}?timestamp=${Date.now()}" target="_blank">
            <img src="${data.img_url}?timestamp=${Date.now()}" alt="SHAP Plot" class="result-image" />
            </a>
            <p class="tips">click on the image to view details</p>
            <span class="large-text">Treatment Music: <span style="color: red;font-size=40">${data.treatment}</span></span>`;
          }
          else{
            this.predictionText = `
            <h2 class="subtitle">诊断结果</h2>
            <span class="large-text">症型判别: <span style="color: red;">${data.prediction}</span></span><br>
            <span class="medium-text">每种症型的可能性:</span><br>
            ${data.probabilities
              .sort((a, b) => b.probability - a.probability) // 按概率从高到低排序
              .map((p) => `<span class="medium-text">${p.class}: ${(p.probability*100).toFixed(0)}%</span>`)
              .join("<br>")}
            <br/>
            <a href="${data.img_url}?timestamp=${Date.now()}" target="_blank">
            <img src="${data.img_url}?timestamp=${Date.now()}" alt="SHAP Plot" class="result-image" />
            </a>
            <br/>
            <p class="tips">点击图片查看详情</p>
            <span class="large-text">治疗方案: <span style="color:red;">${data.treatment}</span></span>`;
          }
          this.audioUrl = data.audio_url; //设置从接口获取音频的URL
          this.imgUrl =  `${data.img_url}?timestamp=${Date.now()}`; // 添加时间戳 ,设置shap_waterfall_plot图
          // this.imgUrl = data.img_url; //设置从接口获取图片的URL,设置shap_waterfall_plot图
        })
        .catch((error) => {
          this.predictionText = `<span class="medium-text" style="color: red;">Error: ${error.response.data.error}</span>`;
        });
        // console.log(features);
        // console.log(language);
    },
  },
  async mounted(){
      document.title = 'Tinnitus Online Diagnosis';
      //初始化kursor
      new Kursor({ 
        type: 2,
        color:'#F59F9F'
      });
      // 初始化 Vanta.js
      // if(window.innerWidth > 768){
      //   this.vantaEffect = NET({
      //     el: "#vanta-background",
      //     mouseControls: true,
      //     touchControls: true,
      //     gyroControls: false,
      //     minHeight: 200.0,
      //     minWidth: 200.0,
      //     scale: 1.0,
      //     scaleMobile: 1.0,
      //     backgroundColor: 0xf3f3f4,
      //     maxDistance: 13.0,
      //     spacing: 13.0,
      //     THREE, // 必须传递 Three.js 依赖
      //     vertexColors: false, // 添加 vertexColors 参数
      //   });
      // }
    },
  beforeDestroy() {
    if (this.vantaEffect && typeof this.vantaEffect.destroy === "function") {
      this.vantaEffect.destroy();
      this.vantaEffect = null;
    }
  },
    // 将组件在 components 配置项中进行注册
  components: {
    AudioPlayer,
  },
});
</script>

<style>
.vanta-container {
  margin: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
/* 全局样式 */
.container {
  font-family: Arial, sans-serif;
  padding: 20px;
  width: 80%;
  max-width: 1300px;
  height: 90%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  /* background-color:beige; */
  /* box-sizing: border-box; */
}
.title {
  text-align: center;
  font-size: 35px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}
.title-style{
  position: relative;
  width: 100%;
  text-align: center;
  flex-direction: row;
  justify-content: center;
  margin-bottom: 5px;
}
.subtitle{
  font-size: 30px;
  margin-bottom: 20px;
  margin-top: auto;
}
/* 内容区域 */
.content {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  align-items: flex-start;
  height: 100%;
}

/* 左侧症状框 */
.symptom-box {
  flex: 3;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  height: 100%;
  width: 90%;
}
.symptoms {
  display: grid;
  grid-template-columns: repeat(3,1fr);
  grid-gap:15px;
  grid-auto-rows: 100px;
}
.symptom-item {
  display: flex;
  background: #e0e0e0;
  padding: 20px;
  border-radius: 10px;
  align-items: center;
  text-align: center;
  justify-content: center;
  font-size: 20px;
  cursor: pointer;
  transition: box-shadow 0.3s ease;
  min-height: 60px;
}
.symptom-item.selected {
  /* box-shadow: 0 0 8px #4caf50; */
  background-color: rgb(100, 167, 169);
}

/* 右侧结果框 */
.result-box {
  flex: 1;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  height: 100%;
  min-height: 500px;
  min-width: 380px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}
.prediction-text {
  margin-bottom: 15px;
  /* padding: 10px; */
  /* text-align: left; */
}
.submit-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 20px 30px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 18px;
  margin-top: auto;
}
.submit-btn:hover {
  background-color: #45a049;
}
.large-text{
  font-size: 30px;
  margin-top: auto;
  margin-bottom: 8px;
}
.medium-text{
  font-size: 25px;
}
.small-text{
  font-size: 20px;
}
.tips{
  font-size: 15px;
  color: #45a049;
}
/* 音乐播放器 */
.music-player {
  margin-top: 20px;
}
.controls {
  display: flex;
  align-items: center;
  gap: 10px;
}
.progress-container,
.volume-container {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.progress-bar,
.volume-bar {
  flex: 1;
  cursor: pointer;
  height: 5px;
}

/* 音频标签样式 */
.audio-label {
  font-size: 25px;
  color: #333;
  margin-top: 15px;
}

/* 音频播放器样式 */
.audio-player {
  width: 100%;
  margin-top: 5px;
}
.result-image {
  width: 100%;

}
/* 配置面板 */
.config-box {
  position: absolute;
  right: 0;
  bottom: 0;
  /* right: 25.2vw;
  top:110px; */
}
.config-change-language {
  background-color: #f9f9f9;
  color: black;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 16px;
  margin-top: auto;
  border-style: none;
}
@media (max-width: 768px){
  .content {
    flex-direction: column;
    align-items: stretch;
  }
  .symptoms {
    grid-template-columns: repeat(1,1fr);
    grid-auto-rows: auto;
  }
  .symptom-item {
    font-size: 20px;
    min-height: auto;
  }
  .symptom-box,
  .result-box {
    height: auto;
    width: 100%;
    flex: none;
    min-width: 350px;
  }
  .result-box{
    min-width: auto;
    min-height: auto;
  }
  .config-change-language{
    font-size: 12px;
    padding: 8px 15px;
    margin: auto;
  }
  .title{
    font-size: 30px;
  }
  .subtitle {
    font-size: 25px;
  }
  .title-style{
    min-width: 350px;
  }
}
/* @media (min-width: 769px) and (max-width: 1025px) {
  .symptom-item{
    font-size: 15px;
  }
  .symptom-box{
    min-width: 600px;
  }
  .subtitle {
    font-size: 20px;
  }
  .large-text,.audio-label{
    font-size: 20px;
  }
  .medium-text{
    font-size: 15px;
  }
  .result-box{
    min-width: 250px;
  }
} */
</style>