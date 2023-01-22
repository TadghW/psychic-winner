let metric1 = document.getElementById('metric1');
let metric2 = document.getElementById('metric2');
let dataLocation = document.getElementById('location');
let from = document.getElementById('from');
let to = document.getElementById('to');
let resultSpace = document.getElementById('result-space');

metric1.addEventListener("change", updateResults, false);
metric2.addEventListener("change", updateResults, false);
dataLocation.addEventListener("change", updateResults, false);
from.addEventListener("change", updateResults, false);
to.addEventListener("change", updateResults, false);

function makeQuery(){
    let url = 'http://127.0.0.1:5000/query'
    let parameters = '?metric1=' + metric1.value + "&metric2=" + metric2.value + "&location=" + dataLocation.value + "&from=" + from.value +  "&to=" + to.value
    let query= url + parameters;
    let promise = new Promise(function (resolve, reject) {
        let req = new XMLHttpRequest();
        req.open("GET", query);
        req.onload = function () {
          if (req.status == 200) {
            let json = JSON.parse(req.response);
            resolve(json);
          } else {
            reject("Invalid response recieved");
          }
        };
        req.send();
    });
    return promise;
}

function updateResults(){
    let queryReturn = makeQuery();
    const consumer = () => {
        queryReturn.then(
            (result) => {
                resultSpace.innerHTML = result;
            },
            (error) => {
                console.log("Error: " + error);
            }
        )
    }
    consumer();
}

updateResults();



