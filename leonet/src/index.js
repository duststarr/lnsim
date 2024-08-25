var Cesium = require('cesium/Cesium');
require('./css/main.css');
require('cesium/Widgets/widgets.css');
//var mqtt = require('mqtt');
Cesium.Ion.defaultAccessToken =
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJiYTg4MTUyNy0zMTA2LTRiMDktOGE1My05ZDA4OTRmOTE3YzciLCJpZCI6MTAzMjg1LCJpYXQiOjE2NTk0MDcyODB9.sfpT8e4oxun23JG--UmUN9ZD4SbQfU-Ljvh2MsPTTcY";
      
var viewer = new Cesium.Viewer('cesiumContainer');
viewer.clockViewModel.shouldAnimate = true;

setTimeout(() => {
    let dronePromise = Cesium.CzmlDataSource.load(
      "http://127.0.0.1:5000/leo/update"
    );
    dronePromise.then((dataSource) => {
      viewer.dataSources.add(dronePromise);
      // 通过ID选择需要轨迹的实体
      dataSource.entities._entities._array.forEach((ele) => {
        viewer.entities.add(ele);
        console.log(ele);
      }) 
    });   
  },3);