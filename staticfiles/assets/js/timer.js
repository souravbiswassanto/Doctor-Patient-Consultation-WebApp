function startTimer() {
    var totalSeconds = 1600;
    var countDownDate = new Date().getTime() + (totalSeconds * 1000);
    var x = setInterval(function() {
      var now = new Date().getTime();
      var distance = countDownDate - now;
      
      var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      var seconds = Math.floor((distance % (1000 * 60)) / 1000);
      document.getElementById("timer").innerHTML = hours + ":" + minutes + ":" + seconds;
      if (distance < 0) {
        clearInterval(x);
        document.getElementById("timer").innerHTML = "EXPIRED";
      }
    }, 1000);
  }
  