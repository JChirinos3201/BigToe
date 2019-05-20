var file_content = document.getElementById('file_content')

var show_project = function (projectId) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      file_content.innerHTML = this.responseText;
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
