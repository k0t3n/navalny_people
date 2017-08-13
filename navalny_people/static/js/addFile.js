(function() {

  $('.input_file').each(function() {
    var $input = $(this),
        $label = $input.next('.js_labelFile'),
        labelVal = $label.html();

   $input.on('change', function(element) {
      var fileName = '';
      if (element.target.value) fileName = element.target.value.split('\\').pop();
      fileName ? $label.find('.js_fileName').html(fileName) : $label.html(labelVal);
   });
  });

})();