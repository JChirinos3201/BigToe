function showReqs() {
  document.getElementById("reqs").innerHTML = "Requirements: <ul><li>Least 1 Capital Letter</li><li>Least 1 lowercase letter</li><li>Least 1 number</li><li>Length at least 6</li></ul>"
}

var password = document.getElementById('password');
var password_verify = document.getElementById('password-verify');
var top_eye = document.getElementById('topEye');
var bottom_eye = document.getElementById('bottomEye');

var show_hide_password = function () {
  if (password.type == 'password') {
    password.type = 'text';
    top_eye.innerHTML = '<i class="fas fa-eye-slash"></i>';
  } else {
    password.type = 'password';
    top_eye.innerHTML = '<i class="fas fa-eye"></i>';
  }
}

var show_hide_password_verify = function () {
  if (password_verify.type == 'password') {
    password_verify.type = 'text';
    bottom_eye.innerHTML = '<i class="fas fa-eye-slash"></i>';
  } else {
    password_verify.type = 'password';
    bottom_eye.innerHTML = '<i class="fas fa-eye"></i>';
  }
}
