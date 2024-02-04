const getOptionChart = async()=>{
    try {
        const response = await fetch('https://app-de-peso.onrender.com/api/')
        return await response.json()
    } catch(e){
        alert(e)
    }
}

const initChart = async ()=>{
    const myChart = echarts.init(document.getElementById('chart'))

    myChart.setOption(await getOptionChart())

    myChart.resize()
      
};

window.addEventListener('load', async()=>{
    await initChart();
})