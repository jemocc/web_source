var app = new Vue({
    el: '#app',
    data: {
        list: [
            {
                id: 1,
                name: 'iPhone 7',
                price: 6188,
                count: 1,
                selected: false
            },{
                id: 2,
                name: 'iPad Pro',
                price: 5888,
                count: 1,
                selected: false   
            },{
                id: 3,
                name: 'MacBook Pro',
                price: 21488,
                count: 2,
                selected: false
            }
        ],
        selectedTotalPrice: 0
    },
    computed: {
        ctotalPrice: function(){
            let tp = 0;
            if(this.selectedTotalPrice === 0){
                for(index in this.list){
                    let item = this.list[index];
                    tp += item.price * item.count;
                }
            } else {
                tp = this.selectedTotalPrice;
            }
            return tp.toString().replace(/\B(?=(\d{3})+$)/g, ',');
        }
    },
    methods: {
        handleReduce: function(index){
            //当更换HTML模板时，disabled属性对span,div等标签无效
            if(this.list[index].count === 1) return;
            this.list[index].count--;
        },
        handleAdd: function(index){
            this.list[index].count++;
        },
        handleRemove: function(index){
            this.list.splice(index, 1);
        },
        selectProd: function(index){
            let t = this.list[index];
            t.selected = t.selected ? false : true;
            if(t.selected){
                this.selectedTotalPrice += t.price * t.count;
            } else {
                this.selectedTotalPrice -= t.price * t.count;
            }
        }
    }
});