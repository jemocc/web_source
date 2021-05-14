var bus = new Vue();

Vue.component('component-a',{
    template: '<button @click="handleEvent()">传递事件</button>',
    methods: {
        handleEvent: function(){
            bus.$emit('on-message','来自组件 component-a 的内容');
        }
    }
})

var app = new Vue({
    el: '#app',
    data: {
        message: "123"
    },
    mounted: function(){
        var _this = this;
        bus.$on('on-message',function(mes){
            _this.message = mes;
        })
    }
})