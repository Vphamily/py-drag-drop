
$(document).ready(function () {

  var uploadBtn = $('#upload-btn');
  uploadBtn.hide();
  $('input[type=file]').change(function () {
    var f = this.files;
    var el = $('#file-info');
    if (f.length > 1) {
      console.log(this.files, 1);
      el.html('<span class="mul"> Sorry, multiple files are not allowed </span>');
      uploadBtn.hide();
      return;
    }
    if (f[0].type !== 'text/csv') {
      el.html('<span class="smls">' + f[0].name + ' is not a CSV file</span>');
      uploadBtn.hide();
    }else{
      el.html('<span class="sml">' + f[0].name + " : " + 'type: ' + f[0].type + ', ' + Math.round(f[0].size / 1024) + ' KB</span>');
      uploadBtn.show();
    }
  });

  $('input[type=file]').on('focus', function () {
    $(this).parent().addClass('focus');
  });

  $('input[type=file]').on('blur', function () {
    $(this).parent().removeClass('focus');
  });

});
