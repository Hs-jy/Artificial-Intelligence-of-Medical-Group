<template>
    <div class="container">
      <div class="audio-container">
        <div class="left">
          <span class="icon" v-if="isPlay == false" @click="play">
            <i class="fa fa-play play-icon" aria-hidden="true"></i>
          </span>
          <span class="icon" v-if="isPlay == true" @click="pause">
            <i class="fa fa-pause pause-icon" aria-hidden="true"></i>
          </span>
        </div>
        <div class="right">
          <div class="words flex-between">
            <div class="time">{{ formatCurrentTime }} / {{ formatTotalTime }}</div>
          </div>
          <div class="duration">
            <input type="range" ref="range" @input="onChange" @change="onChange" min="0" max="360" value="0">
          </div>
        </div>
        <!-- 音量控制 -->
        <div class="volume" 
          @mouseenter="onMouseEnterVolume" 
          @mouseleave="onMouseLeaveVolume"
          @click.stop="toggleVolumeControl">
          <span class="icon">
            <i class="fa" :class="isMuted ? 'fa-volume-mute' : 'fa-volume-up'" aria-hidden="true"></i>
          </span>
          <!-- 音量滑块 -->
          <div v-show="showVolumeControl" class="volume-slider-container">
            <input
              type="range"
              ref="volumeRange"
              @input="onVolumeChange"
              min="0"
              max="1"
              step="0.01"
              :value="volume"
              class="volume-slider"
            />
            </div>
        </div>
      </div>
      <audio style="display: none" :src="audioURL" ref="audio" controls @timeupdate="update" @canplay="loadingFinish"></audio>
    </div>
  </template>
  
  <script>
  import 'font-awesome/css/font-awesome.css';

  export default {
    name: 'AudioPlayer',
    components: {},
    props: {
      audioURL: { //定义了一个 prop，用于接收父组件传递的音频 URL
        type: String,
        default: '',
        Required:true,
      },
    },
    data() {
      return {
        isPlay: false, // 控制icon切换
        totalTime: 0, // 播放总时间--秒
        currentTime: 0, // 当前播放时间--秒
        // five_music: ['gong','shang','jue','zhi','yu'],
        volume: 0.5,
        isMuted: false,
        showVolumeControl:false,
        volumeTimer: null, // 定时器
      }
    },
    computed: {
      formatTotalTime() {
        return this.formatTime(this.totalTime)
      },
      formatCurrentTime() {
        return this.formatTime(this.currentTime)
      },
      // 音频名称
      audioName() {
        return this.getFilename(this.audioURL)// 使用传递过来的 audioURL 来获取文件名
      },

    },
    mounted() {
      if (this.audioURL) {
        this.$refs.audio.src = this.audioURL;  // 在 mounted 中设置 audio 的 src 属性
        setTimeout(() => {
          this.$refs.range.value = 0;
        }, 1);
      }
    },
    methods: {
      // 控制音乐播放
      play() {
        const audio = this.$refs.audio
        audio.play()
        this.isPlay = true
      },
      // 控制音乐暂停
      pause() {
        const audio = this.$refs.audio
        audio.pause()
        this.isPlay = false
      },
      // 音乐缓存完毕，获取时间
      loadingFinish() {
        const totalTime = this.$refs.audio.duration
        this.totalTime = totalTime
      },
      // range--拖动进度条得到的回调
      onChange() {
        let value = this.$refs.range.value
        const persentage = ((value / 360) * 100).toFixed(1) + '%'
        this.$refs.range.style.backgroundSize = `${persentage} 100%`
        // 控制音频播放
        const timeToGo = (value / 360) * this.totalTime
        const audio = this.$refs.audio
        audio.currentTime = timeToGo
      },
      // audio--进度变化的时候的回调--改变文字
      update() {
        const audio = this.$refs.audio
        const currentTime = audio.currentTime // 当前播放时间
        this.currentTime = currentTime
        // 改变进度条的值
        const range = this.$refs.range
        range.value = ((this.currentTime / this.totalTime) * 360).toFixed(1)
        // 进度条的值改变的时候，颜色也跟着变化
        const persentage = ((this.currentTime / this.totalTime) * 100).toFixed(1) + '%'
        this.$refs.range.style.backgroundSize = `${persentage} 100%`
      },
  
      //辅助函数，将秒变成分秒的形式--用在计算属性中
      formatTime(value) {
        let second = 0
        let minute = 0
        minute = parseInt(value / 60)
        second = parseInt(value % 60)
        // 补0
        minute = minute < 10 ? '0' + minute : minute
        second = second < 10 ? '0' + second : second
        return minute + ':' + second
      },
      // 通过url获取filename
      getFilename(url) {
          const arr = url.split('/')
          return arr[arr.length - 1] // 获取音频文件名
        },
      // 鼠标进入：显示音量滑块
      onMouseEnterVolume() {
        this.showVolumeControl = true;
        if (this.volumeTimer) {
          clearTimeout(this.volumeTimer); // 清除之前的隐藏定时器
          this.volumeTimer = null;
        }
      },
      // 鼠标离开：1.5秒后隐藏音量滑块
      onMouseLeaveVolume() {
        this.volumeTimer = setTimeout(() => {
          this.showVolumeControl = false; // 隐藏滑块
        }, 1500);
      },
        // 音量滑块：显示
      showVolumeSlider() {
        this.showVolumeControl = true; // 立即显示滑块
        if (this.volumeTimer) {
          clearTimeout(this.volumeTimer); // 清除隐藏的定时器
          this.volumeTimer = null;
        }
      },
      // 音量调节
      onVolumeChange() {
        const audio = this.$refs.audio;
        this.volume = this.$refs.volumeRange.value;
        audio.volume = this.volume;
        this.isMuted = this.volume === '0';
      },
      // 静音和取消静音
      toggleMute() {
        const audio = this.$refs.audio;
        this.isMuted = !this.isMuted;
        audio.muted = this.isMuted;
      },
      // 点击切换音量滑块显示状态
      toggleVolumeControl() {
        this.showVolumeControl = !this.showVolumeControl;
        if (this.showVolumeControl && this.volumeTimer) {
          clearTimeout(this.volumeTimer); // 清除定时器
        }
      },
    },
  }
  </script>
  
  <style scoped>
  .container{
    width: 300px;
    background-color: #f9f9f9;
    display: flex;
    flex-direction: column;
    gap:20px;
  }
  .audio-container {
    padding: 8px 8px;
    width: 100%;
    background: hsl(140, 18%, 90%);
    border-radius: 5px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: -60px;
    margin-left: 50px;
  }
  .left {
    margin-right: 16px;
  }
  /* 播放暂停按钮 */
  .icon {
    display: inline-block;
    width: 28px;
    height: 28px;
    border: 2px solid #10a9ff;
    border-radius: 50%;
    
    text-align: center;
    font-size: 16px;
    line-height: 28px;
  
    color: #76B2ED;
  }
  .icon:hover {
    cursor: pointer;
  }
  .play-icon {
    position: relative;
    left: 2px;
  }
  .flex-between {
    display: flex;
    justify-content: space-between;
    align-content: center;
  }
  .right {
    flex: 1;
  }
  .words {
    margin-bottom: -1px;
  }
  .name {
    font-size: 14px;
    color: #333333;
    line-height: 14px;
  }
  .time {
    font-size: 14px;
    color: #666666;
    line-height: 14px;
  }

  .volume {
    position: relative;
    display: flex;
    align-items: center;
    margin-left: 16px;
    cursor: pointer;
  }

  .volume .icon {
    font-size: 18px;
    color: #76B2ED;
  }

  .volume-slider-container {
    position: absolute;
    bottom: 45px; /* 控制滑块的显示位置 */
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .volume-slider {
    writing-mode: bt-lr; /* 设置滑块为上下方向 */
    direction: rtl; /* 反转数值方向，让向上增加音量 */
    transform: rotate(90deg); /* 将滑块旋转90度，使其变为上下滑动 */
    width: 100px;
    height: 10px;
    margin-top: 10px;
  }

  .volume:hover .volume-slider-container {
    display: block;
  }

  /* 控件 */
  input[type='range'] {
    outline: none;
    appearance: none; /*清除系统默认样式*/
    width: 100% !important;
    background: -webkit-linear-gradient(#10a9ff, #76B2ED) no-repeat, #dddddd; /*背景颜色，俩个颜色分别对应上下*/
    background-size: 0% 100%; /*设置左右宽度比例，这里可以设置为拖动条属性*/
    height: 2px; /*横条的高度，细的真的比较好看嗯*/
  }
  /*拖动块的样式*/
  input[type='range']::-webkit-slider-thumb {
    -webkit-appearance: none; /*清除系统默认样式*/
    height: 10px; /*拖动块高度*/
    width: 3px; /*拖动块宽度*/
    background: #10a9ff; /*拖动块背景*/
  }
  @media (max-width: 768px){
    .audio-container{
      margin:auto;
    }
  }
  </style>
  