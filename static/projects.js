var file_content = document.getElementById('file_content');
var projectId;

var setProjectId = function (newProjectId) {
  projectId = newProjectId;
};

var show_project = function () {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      file_content.innerHTML = this.responseText;
      document.getElementById('sharewith').addEventListener('keyup', function (e) {
        if (e.keyCode === 13) {
          e.preventDefault();
          add_collaborator(projectId);
        }
      });
      get_collaborators(projectId);
    }
  }
  xhttp.open('GET', '/get_files/' + projectId, true);
  xhttp.send();
};

var leave_project = function () {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      location.reload();
    }
  }
  xhttp.open('POST', '/leave_project', true);

  var fd = new FormData();
  fd.append('projectId', projectId);

  xhttp.send(fd);
};

var new_file = function () {

};

var show_new_project = function () {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      file_content.innerHTML = this.responseText;
    }
  }
  xhttp.open('GET', '/get_new_project', true);
  xhttp.send();
}

var get_collaborators = function () {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById('collaborators').innerHTML = this.responseText;
    }
  }
  xhttp.open('GET', '/get_collaborators/' + projectId, true);
  xhttp.send();
}

var add_collaborator = function () {
  console.log(projectId);
  var email = document.getElementById('sharewith').value;
  var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
  if (reg.test(email) == false) {
    alert('Invalid Email Address');
    return;
  }
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var r = this.responseText;
      if (r == 'bruh thats not a user!') {
        alert("User doesn't exist!");
      } else {
        document.getElementById('sharewith').value = "";
        console.log(projectId);
        get_collaborators(projectId);
        console.log(r);
      }
    }
  }
  var fd = new FormData();
  fd.append('email', email);
  fd.append('projectId', projectId);
  xhttp.open('POST', '/add_collaborator');
  xhttp.send(fd);
}

var add_file = function () {
  var filename = document.getElementById('filename').value;
  var reg = /\s/;
  if (reg.test(filename)) {
    alert('Invalid filename');
    return;
  }

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      location.reload();
    }
  }
  var fd = new FormData();
  fd.append('filename', filename);
  fd.append('projectId', projectId);
  xhttp.open('POST', '/add_file');
  xhttp.send(fd);
}
