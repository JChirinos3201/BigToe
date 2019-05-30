var file_content = document.getElementById('file_content');

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
      get_collaborators(projectId);
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
  xhttp.open('GET', '/get_new_project', true);
  xhttp.send();
}

var get_collaborators = function (projectId) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById('collaborators').innerHTML = this.responseText;
    }
  }
  xhttp.open('GET', '/get_collaborators/' + projectId, true);
  xhttp.send();
}

var add_collaborator = function (projectId) {
  var email = document.getElementById('sharewith').value;
  var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
  if (reg.test(email) == false) {
    alert('Invalid Email Address');
    return;
  }
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById('sharewith').value = "";
      get_collaborators(projectId);
      console.log(this.responseText);
    }
  }
  var fd = new FormData();
  fd.append('email', email);
  fd.append('projectId', projectId);
  xhttp.open('POST', '/add_collaborator');
  xhttp.send(fd);
}

var addFile = function (projectId) {
  var filename = document.getElementById('filename').value;
  var reg = /\s/;
  if (reg.test(filename)) {
    alert('Invalid filename');
    return;
  }

  var xhttp_add = new XMLHttpRequest();
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
