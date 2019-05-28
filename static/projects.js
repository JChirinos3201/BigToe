var file_content = document.getElementById('file_content');
var collaborators = [];

var show_project = function (projectId) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      file_content.innerHTML = this.responseText;
      document.getElementById('sharewith').addEventListener('keyup', function (e) {
        if (e.keyCode === 13) {
          e.preventDefault();
          add_collaborator();
        }
      });
    }
  }
  xhttp.open('GET', '/get_files/' + projectId, true);
  xhttp.send();
};

var show_new_project = function () {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      file_content.innerHTML = this.responseText;
    }
  }
  xhttp.open('GET', '/get_new_project')
  xhttp.send();
}

var add_collaborator = function () {
  var email = document.getElementById('sharewith').value;
  var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
  if (reg.test(email) == false) {
    alert('Invalid Email Address');
    return;
  }
  collaborators.push(email)
  var sharegroup = document.getElementById('sharegroup');
  sharegroup.innerHTML = sharegroup.innerHTML + '<button type="button" id="remove' + email + '" onclick="remove_collaborator(\'' + email + '\')" class="btn btn-default">' + email + ' &times;</button>';
  document.getElementById('sharewith').value = "";
}

var remove_collaborator = function (email) {
  var index = collaborators.indexOf(email);
  if (index > -1) {
    collaborators.splice(index, 1);
  }
  var element = document.getElementById('remove' + email);
  element.parentNode.removeChild(element);
}
