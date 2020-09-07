

var video = document.getElementById("lecture_video");
var timeStarted = -1;
var timePlayed = 0;
var duration = 0;
var checkLecture = 0;
var learner = $("#lecture_video").data('user'); 
var lecture = $("#lecture_video").data('lecture'); 
var watcher = undefined;
var playAlert = undefined;

$(document).ready(function(){
    if(video.readyState > 0){
        getDuration.call(video);
    }
    //If metadata not loaded, use event to get it
    else{
        video.addEventListener('loadedmetadata', getDuration);
    }
    attachEvent();
})

// 기존 속성값 이전
function setAttributes(datas){
  timePlayed = datas.ls_learning_time || 0;
  console.log("수강 시간 : "+timePlayed);
}

function attachEvent(){
    video.addEventListener("play", videoStartedPlaying);
    video.addEventListener("playing", videoPlaying);
    video.addEventListener("ended", videoEnd);
    video.addEventListener("pause", videoStoppedPlaying);
    // watcher = setInterval(checkFinishLecture, 1000);
}

function checkFinishLecture(evt){
  if (!video.paused) timePlayed += 1;
  console.log(timePlayed);
  if (timePlayed >= duration){
    videoStoppedPlaying();
    // video.removeEventListener("timeupdate", checkFinishLecture);
  }
}
// remember time user started the video
function videoStartedPlaying() {
  timeStarted = new Date().getTime()/1000;
  alertMsg();
}

function videoPlaying(){
  timeStarted = new Date().getTime()/1000;
}

function alertMsg(){
  checkLecture = parseInt(duration/300);
  if(parseInt(timePlayed/300) < checkLecture){
    playAlert = setInterval(function(){
      video.pause();
      videoStoppedPlaying();
      console.log(typeof playAlert);
      alert("강의를 계속 진행하려면 확인 버튼을 눌러 주세요.");
      video.play();
      videoStartedPlaying();
    }, 300000); 
  }
}

function outpage(){
  videoStoppedPlaying();
}

function videoStoppedPlaying(event) {
  if(timeStarted > 0) {
    var playedFor = new Date().getTime()/1000 - timeStarted;
    timeStarted = -1;
    timePlayed += playedFor;
  }
  clearInterval(playAlert);
  send_to_server();
}

function videoEnd(event){
  if(timePlayed>=duration /* && event.type=="ended" */) {
    if (watcher) clearInterval(watcher);
    clearInterval(playAlert);
    alert("수강 완료 되었습니다.");
  }
  send_to_server();
}

function getDuration() {
  duration = video.duration;
  console.log("lecture duration : ", duration);
}


function send_to_server(){
    $.ajax({
        url : '/convergence/lecture/do',
        type : 'post',
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify({
            'learner' : learner,
            'lecture' : lecture,
            'start_time' : timeStarted,
            'played_time' : timePlayed,
            'duration' : duration,
        })
    }).done(function(res){
        console.log(res);
    }).fail(function(err){
        console.log(err);
    })
}

