let state = true;
let anomalyDetected = false;
let script = true;
let isTimerOn = true;
let prev_content = 'Normal';

function dataExtract() {
  console.log('I just called');
  fetch("http://localhost:3000/")
    .then(function (response) {
      return response.json();
    })
    .then(function (myJson) {
      if(myJson.data === "Normal") {
        document.querySelector('.second').style.backgroundColor = "#7CF000";
        document.querySelector('.a').classList.remove('form-control');
        document.querySelector('.a').classList.remove('detected');
        document.querySelector('.a').textContent = null;
        isTimerOn = true;
        document.querySelector('#script-run').disabled = true;
      } else if(myJson.data === "Video Finished"){
        isTimerOn = false;
      } else {
        // stopTimerButton();
        console.log('I am here');
        domManipulation(myJson);
        anomalyDetected = true;
        setTimeout(() => {
          if(script === true && prev_content !== myJson.data) {
            prev_content = myJson.data;
            scriptRun();
          } else {

          }
        }, 10000);
        isTimerOn=true;
        //setTimeout(commandPrompt, 3000);
        // commandPrompt();
      }
    })
    .catch(function (error) {
      console.log("Error: " + error);
    });
}

function scriptNotRunning() {
  script = false;
}


function domManipulation(myJson) {
  document.querySelector('.second').style.backgroundColor = "#F32013";
  document.querySelector('.a').classList.add('form-control');
  document.querySelector('.a').classList.add('detected');
  document.querySelector('.a').textContent = myJson.data;
  document.querySelector('#script-run').disabled = false;
}


function commandPrompt() {
  let ask =  prompt('Do you want to inform authorities?Yes or No');
        if(ask === "yes" || ask == "1") {
          stopTimerButton();
          scriptRun();
        }
}

// const stopTimerButton = () => {
//     state = !state;
//     if(state) {
//       console.log("Timer Started!!!");
//       myTimer = setInterval(dataExtract, 1000);
//       document.querySelector('#start-stop').textContent = "Stop Processing";
//     } else {
//       console.log("Timer Stopped");
//       clearInterval(myTimer);
//       document.querySelector('#start-stop').textContent = "Start Processing";
//     }
// }

function scriptRun() {
  console.log("Script Function Called!!!");
  fetch("http://localhost:3000/script")
    .then(function (response) {
      return response.json();
    })
    .then(function (myJson) {
      
    })
    .catch(function (error) {
      console.log("Error: " + error);
    });
};


async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function starthere(){
  // infinitely run the script till video ends.
  while (true) {
    // Try to read file with data.
      try{
      let myTimer = setTimeout(dataExtract, 30);     // Check for any new data every 30 ms.
      await sleep(700);                              // Sleep the whole process for 700ms.
      // console.log(myTimer);
      if (isTimerOn === false) {
        break;
      }
    }
    //  Prevents read failure if file is already open in the other script.
      catch{
          await sleep(3);
      }
  }
}

//  Main function
starthere();